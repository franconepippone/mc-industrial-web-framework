# RDS Router Specifications

This document defines exactly what an RDS Router is and how it operates in abstract terms. Every physical implementation of a Router MUST follow the requirements described here in order to function correctly inside an RDS network. Any machine that implements these working principles can be used as an RDS Router.

> NOTE: In the current RDS implementation, a Package is a **Shulker Box**. The terms might be used interchangeably.

## Abstract Definition

### 1-Input, N-Outputs

An RDS Router can be understood as a system with **one input** and **multiple outputs**. Inputs receive inbound Packages, while outputs emit outbound Packages.

In practical terms, inputs and outputs are buffers (containers) that temporarily store Packages before they are processed or forwarded. Each output buffer is also called an **output port**.

The Router itself does not transport Packages. It only makes routing decisions, moving them between buffers.


### Destination Addresses

A destination address is any item that can be compared with others for equality (usually a renamed stackable item, since that works with most filtering systems).

Packages follow this structure:

- The first non-empty slot of the Package is the destination address.
- All subsequent slots are payload and may contain anything.

When a Router receives a Package, it must extract the first available item (the first non-empty slot) and use it as the destination address.

> NOTE: The first available item is the one found by scanning slots from left to right and top to bottom of the container (Shulker Box).


### Routing Table

Each Router maintains an internal **Routing Table**, that is an internal configurable mapping that each Router needs to store. This table maps destination addresses to output ports.
- One destination address maps to exactly one output port.
- One output port may be associated with multiple destination addresses.

The Routing Table is the decision mechanism used by the Router to determine where a Package should be forwarded.


### Working Principle

The goal of the RDS Router is to move Packages from the input buffer to an appropriate output buffer based on the destination address.

It is important to note that the Router **only makes the routing decision**. Physical transportation of Packages is handled by other systems (Transports, see *trasport_specs.md*).

The general flow of Router operation is:

1. A Package is available in the input buffer.
2. The destination address is extracted from the first occupied slot.
3. The Routing Table is consulted to determine which output port matches the address.
4. The destination address is placed back into the Package so it remains the first occupied slot.
5. The Package is moved to the chosen output port buffer.
6. If the input buffer still contains Packages, return to step 1.

> NOTE: the algorithm above implies that packages are processed sequentially. However, packages might also be processed in parallel.


## Variations

Routers may implement variations of the baseline architecture to satisfy specific requirements.


### Hierarchical Routing Support

As described in *hierarchical_routing.md*, routers operating in layer-1 or above networks must implement a small modification.

When forwarding a Package to a network of an inferior layer, the Router **must not** reinsert the destination address into the Package. For example, when a layer-1 Router forwards a Package to a layer-0 Router (and this rule applies to any layer transition), the address is omitted so that the lower-layer Router can use the next available address for routing (often stored in the second slot).

This slight modification can be made by optionally ignoring step 4 of the general operational flow described above, depending on which output port is choosen in step 3.

> NOTE: A Router that supports this behavior can work in networks of any layer. The distinction between layer-x and layer-y Routers comes from the way they are configured and arranged inside a network, not from fundamentally different designs.


### Multiple Inputs

In some designs, it can be useful to allow the source of a Package (at the port level, not address level) influence routing decisions — for example, to choose different default routes when the destination address is unknown.

The baseline Router specification is source-agnostic: it does not differentiate between input ports when making routing decisions. However, implementations may provide **multiple input buffers**, each corresponding to a distinct input port.

If multiple input buffers exist, additional routing logic may consider the source port as part of the decision process (for example, selecting a different default route based on the input port). This capability is optional.

Even with multiple inputs, the core routing rule remains unchanged: decisions are based primarily on destination addresses.