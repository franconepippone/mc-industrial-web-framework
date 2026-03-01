# Hierarchical Routing for the Resource Distribution System

One very evident constraint of the baseline RDS routing architecture (described in *overview.md*) is that, in large networks with many Routers, adding or removing a Terminal requires updating the routing tables of **all** Routers in the network. This is manageable for small or medium-sized networks, where only a handful of Routers exist. However, the approach quickly reveals two major drawbacks:

- **Maintenance cost**: Updating the routing table of every Router in empire-sized networks — potentially with 15+ Routers — is simply not realistic. In networks of that scale, new Terminals are likely being added or modified frequently, making constant global updates impractical.
- **Network administration**: When multiple players are involved, the situation becomes even more complex. Each player may own their own Routers and Terminal addresses, effectively forming independent “local” network domains. In order to allow resource transfers across these domains, every Router in the global network must know the location of every Terminal in every local domain. This means that if a single player makes a small change within their own network, all Routers in the global infrastructure must be updated to reflect it.
There is also a naming conflict issue. If all Terminals share the same global network, duplicate addresses are not allowed. This implies that whenever a player wants to create or rename a Terminal, they must first verify with every other player that the chosen address is globally available. This process is tedious, inefficient, and highly prone to mistakes or conflicts.


## Quick fixes

There are ways to mitigate some of these issues without introducing entirely new systems.

### - Include network ownership prefix in the address

If we agree on prefixing each address with a network ownership identifier — for example, the name of the player who owns that domain (e.g., *MyPlayerName:smelter*) — the naming conflict problem is effectively solved. As long as this convention is respected, each player can freely manage their own local network without requiring global "name availability" checks.

However, this solution does not solve the scalability issue: every Router in the global network still needs to be updated whenever a new Terminal is added. It is therefore only a partial fix. The next idea addresses this limitation.

### - Using default routes to handle unknown destinations  

In *readme.md*, it is specified that whenever a router does not find a match between its routing table and the destination address of an incoming package, it can choose between a set of actions, such as: drop the packet / store it / send it to a default port.  

The key idea here is to formalize this “default port” behavior into what we can call a **default route**. Instead of treating the default port as a simple fallback output, we intentionally configure it to forward all packets with unknown destinations toward a specific router that acts as an exit point from the local network. In other words, the default port becomes a deterministic path that handles every non-local address.

By configuring routers in this way, packets with known destinations continue to be routed normally inside the local network, while packets whose destinations are not found in the local routing tables are automatically forwarded along the default route. This effectively allows them to leave the local domain and reach an external router that can handle them.

Routers configured to serve this purpose will be referred to as **Border Routers**, since they act as the *border* or *frontier* between a local network domain and the rest of the global network.

Some examples clarify how this works.

#### 1) Two-sided network

Consider a scenario with two network domains, A and B. Each domain consists of multiple Terminals and at least one Border Router. (Note that additional Routers may exist internally, as long as their default routes allow unknown Packages to exit toward the Border Router.)

Within each domain, local traffic behaves normally. When a Package is destined for a Terminal in the other domain, the default route inside domain A can be configured to forward packages with unknown destinations to its Border Router, which in turns sends them to domain B's Border Router, and vice versa.

This solution is simple and effective for connecting exactly two domains. But what happens when more than two domains must be interconnected?

#### 2) Circular networks

To interconnect multiple local domains, we can extend the default route concept by forming a closed loop between Border Routers. In such a configuration, unknown Packages are forwarded in a circular chain that eventually passes through every Border Router in the global network.

For example, with domains A, B, C, D, and E, the loop would look like:

A → B → C → D → E → A → ...

Local traffic within each domain still functions normally, and any Package destined for a foreign domain is guaranteed to eventually reach the correct one.

For small global networks of three or four domains, this solution works well. However, as the number of domains increases, several limitations become apparent:

- **Fixed direction of travel**: If a Package originates in A and is destined for B, it may reach B immediately. However, if a Package originates in B and is destined for A, it may need to traverse the entire loop before returning to A. This is inefficient, especially when domains are physically close but logically distant in the loop.
- **Trapped Packages**: If a Package with a globally unknown destination is injected into the loop, it will circulate indefinitely. Such a Package becomes effectively “trapped.” Depending on the loop size, locating and removing it may be difficult. Trapped Packages can result in resource loss, unnecessary traffic, and increased server load.

For medium-sized networks (four to five domains), these solutions may be sufficient and are often worth implementing. For truly large-scale, world-spanning architectures, however, a more scalable and robust approach is required.


## The ideal solution: Hierarchical Routing

#### How does the Internet do it?

The Internet is not a single flat network where every router knows every endpoint. If it were, it would face the same scalability issues described above. Instead, it is organized into multiple hierarchical layers. Each layer routes traffic not between individual end devices, but between entire sub-networks belonging to a lower layer.  

By grouping routes together in this way, the size and maintenance cost of routing tables are drastically reduced.


### General Idea

We can adopt the same principle within the RDS.

The standard RDS Routers, which route Packages between Terminals, belong to the lowest layer — **layer 0**. For convenience, we will refer to a layer-0 network as a **district**. A district is therefore a collection of Routers and Terminals forming a small or medium-sized local network.

To allow communication with external districts, each district must include one **Border Router**, which is the only Router in the district responsible for interfacing with the higher-layer network (layer 1).

> *Insight*: From a layer-1 perspective, a district’s Border Router plays a role analogous to a Terminal in a layer-0 network. In other words, the “endpoints” of a layer-1 network are precisely the Border Routers of layer-0 districts.

When a Package destined for an external district is sent from a Terminal into a layer-0 network, it is routed internally to the district’s Border Router. The Border Router forwards it to a layer-1 Router. From that point onward, the Package travels within the layer-1 network, where it is routed toward the destination district.

Once it reaches the Border Router of the target district, the Package re-enters layer 0. Internal routing within that district then delivers it to the final destination Terminal.

This concept can, in principle, be extended to any additional layers. For practical RDS implementations, however, two layers should be sufficient.


### Handling multi-layered Addressing

In the baseline RDS architecture, each Package carries a single destination address used by Routers for routing decisions. In a hierarchical system, a single address is no longer sufficient.

A Package must now carry:

- The layer-1 address (the destination district).
- The layer-0 address (the destination Terminal within that district).

Additionally, we must ensure that the origin district ignores the layer-0 Terminal address while the Package is being routed externally, and that the layer-0 Terminal address becomes the effective destination only after the Package has reached the correct district.

### Practical Implementation

Although multi-layer addressing may seem complex to implement in Minecraft, it integrates naturally with the existing RDS design, requiring only minor adjustments to Router behavior and protocol conventions.

Currently, the destination address is encoded as a renamed item placed in the first (top-left) slot of the Shulker Box Package. The remaining slots are used for payload. We have also already introduced the concept of default routes, which forward unknown destinations outward.

To enable hierarchical routing, we configure each district’s default route to point toward its Border Router and from there to the nearest layer-1 Router, similarly to what has been done in the previous fixes. 

The first slot of the Shulker Box can now safely contain the **layer-1 district address**. Since this address does not match any layer-0 Terminal inside the origin district, the default route automatically forwards the Package to the Border Router, which passes it to layer 1. Within layer 1, Routers recognize the district address and correctly route the Package toward the destination district.

So far, no structural modification has been required.

The remaining challenge is enabling correct routing within the destination district. For this, the layer-0 Terminal address must also be carried inside the Package. This can be stored safely in the second slot of the Shulker Box, as it is treated as generic payload by higher layers.

Upon entering the destination district, the layer-1 address must no longer be used for routing. This is achieved by having the final layer-1 Router **not reinsert** the layer-1 address into the Shulker Box when forwarding the Package to the destination Border Router. As a result, the first slot becomes empty, and the layer-0 Terminal address in the second slot becomes the first non-empty slot.

> NOTE: RDS Routers always extract the item in the first non-empty slot of the Shulker Box and interpret it as the destination address. Therefore, if the first slot is empty and the second slot contains an item, the second slot item will be used for routing.

From this point onward, the district’s internal Routers naturally route the Package to the correct Terminal.

This mechanism generalizes to any number of layers by storing addresses in order, starting from the highest layer in slot 0 and descending layer by layer. For example, in a five-layer network, a Package would look like:

| addr-4 | addr-3 | addr-2 | addr-1 (district) | addr-0 (terminal) | ... payload ... |

Importantly, this system remains fully compatible with the simpler single-layer architecture. Local traffic within a district still requires only a single destination address.


#### Recap: Package journey through a 2-layer RDS network

Suppose we want to transfer stacks of iron from a local Iron Farm to a remote construction site in a developing Minecraft city. The destination district address is `"district:oasis-city"` and the destination Terminal is `"construction-site-1"`.

We rename two items accordingly and place them respectively in the first and second slots of the Shulker Box. The remaining slots are filled with iron.

After sending the Package through a local Terminal, the origin district does not recognize `"district:oasis-city"` as a local layer-0 address. The Package therefore follows the default route toward the Border Router and enters the layer-1 network.

Layer-1 Routers recognize the district address in the first slot and route the Package through the layer-1 network until it reaches the Router connected to Oasis City’s Border Router.

On the final layer-1 hop, the Router does **not** reinsert the district address into the Shulker Box. The first slot is now empty, and the second slot contains the layer-0 Terminal address, meaning that any other router that will process the Package will now use the item in the second slot for routing (which, in this case, is the `"construction-site-1"` address).

Once the Package enters the Oasis City Border Router, internal routing within the district delivers it to `"construction-site-1"`, where its payload becomes available to machines or players.


#### Some caveats

- **Diminished Payload**: The more addressing layers are stored in the Shulker Box, the fewer slots remain available for payload. For two-layer networks, this is usually negligible, but it should be considered for deeper hierarchies.
- **Naming conflicts across layers**: For hierarchical routing to function correctly, higher-layer addresses must not collide with lower-layer addresses. In practice, this means no Terminal should use a name that matches a district-level address. This is easily avoided by prefixing higher-layer addresses with a reserved sequence such as `"district:<name>"`, leaving full flexibility for Terminal naming.


### District "Firewall"

In a layered system, all inbound and outbound traffic between a district (layer 0) and the higher-layer network (layer 1) passes through a pair of elements: the Border Router (layer 0) and a connected layer-1 Router.

If a Package reacheing a layer-0 Border Router has an unknown local destination address, the Border Router bounces it right back to the connected layer-1 Router via its default route. At this stage, the layer-1 district address has already been removed (as described earlier), so the layer-1 Router no longer finds a matching route. The Package is therefore dropped, stored, or forwarded elsewhere according to layer-1 default behavior.

This naturally creates a form of “firewall”: invalid or erroneous traffic does not propagate into the internal district network.

However, there may be cases where we still want to capture such Packages — for inspection, debugging, or specific design requirements. There is a clean solution for this. 
Instead of using a single Border Router for both directions, we can split the concept into two half-duplex links. One router is exposed to layer-1 and acts as the district’s visible entry point — this is where layer-1 sends Packages destined for the district. The second router is invisible to layer-1 and is used only for outbound traffic from the district toward layer-1. We then configure the district’s default route to forward external traffic through the invisible outbound router, while incoming traffic from layer-1 arrives through the visible inbound router. This separation allows us to filter and inspect incoming Packages before they reach the internal district, while still maintaining a clear path for outbound traffic.

For example, a Package leaving the district follows: Terminal → internal routers → invisible outbound router → layer-1 network. Conversely, a Package arriving from layer-1 enters through the visible inbound router and is then passed to the district’s internal network for delivery to its target Terminal. Because the two links are distinct, unknown or suspicious Packages can be captured and inspected on the inbound side without immediately bouncing them back to layer-1.
