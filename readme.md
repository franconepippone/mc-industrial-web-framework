# The Minecraft Industrial Web Framework
### Overview
The MC industrial web framework is a set of architectural principles, protocols and ideas aimed at providing a structured and organized way
for creating an efficient and fully automated network of factories in vanilla minecraft. It defines ways on how factories 
located all across the map can share resources on demand fully automatically, implementing common architectural patters like service-client or
point-to-point resource transfer.   
The framework's backbone is the **Resource Distribution System (RDS)**, which is a layered system designed for automated 
and efficient point to point resource sharing, inspired by the workings of real Internet networks. The goal of the Resource Distribution System is to automate the delivery of a payload from a generic point A to point B of the world, based on a destination tag attached to the payload iteself.

## Core entities of the Resource Distribution System (RDS)
### Terminal
A terminal is an endpoint for the Resource Distribution system (RDS); it's a point where resources can be sent or recevied from the network. A resource is any quantity of items that we are interesetd in transferring from one terminal to another. Resources are boundled into "packages", which are the actual resource containers that physically travel across the network.   
As it's probably easy to guess, the best MC item that suites this purpose is the Shulker Box; therefore, in the RDS, the ONLY things that actually travel are shulker boxes containing the desired items as payload. The first slot of the shulker box is reserved for the *destination tag*, which is as an item renamed with the package's destination's unique identifier (address); this item will be used by the routers to properly forward the package to its intended destination.

### Router
A router is the second core element of the RDS. It's inspired directly by Internet routers, and follows the same working principles. It's a node in the web, were multiple edges meet and where travelling packages can be rerouted to the appropriate direction based on their attached destination tag. A RDS Router generally has only ONE input port where all inbound packages enter, making no intrinsic dinstinction from the incoming package origin. A router can have any amount of edges connected to it, and to each edge correspond a "port", which is just an ending container where outbound packages are termporarily placed once the appropriate routing decision has been made. Each outbound direction/edge maps to a specific port in a router, and a port can simply be any container that can termporarily hold packages.  
To make routing decisions, a router stores a routing table, which maps each possible destination to the respective port on which to forward the package. When a package arrives at the router, the routing table is checked to see if there are any ports mapped to the package's requested destination; if there are, the package is forwarded to that port. After a package has been succesfully transfered to the appropriate outbound port, the router's job is over; it's now the underlying transport's job to physically move the package (NB.: Routers *DO NOT* move packages, they only make routing decisions; they move packages from the *inbound* port to one of their *outbond* ports).
> Note that, although a Router and a Terminal are conceptually different entities, they can physically coexist in the same place, meaning that nothing stops you from building a router that also acts like a terminal and vice versa.

### Transport 
A transport is any minecraft technlogy capable of moving items from point A to point B. In the context of the RDS, a transport system has the rensponsability of "hopping" the package across the network: it needs to be capable of moving a package (shulker box) from Terminal to Router, from Router to Router or from Router to Terminal. A route consists of multiple hops, the ones needed to succesfully reach a destination terminal from a origin terminal.     
There are a lot of tecnhologies available in minecraft that fulfill this role, and each of them comes with its stregths and weaknesses. It's up to the designer to choose which technology best suites the scenario. Also note that, since routers and terminals are transport-agnostic, a mix of techonologies can be used depending on which one is more convenient for a given hop across the network. Some examples of techonologies are flowing water "conveyor belts", or minecart with chest and rails.


#### Recapping: a package journey through the RDS
Say that we want to transfer a large quantity of oak logs from the oak farm (Terminal1) to the industrial smelter (Terminal2). First of all, a destination tag needs to be created; an item is renamed with the unique destination identifier of the industrial smelter terminal (for example "smlter-2"), and it is placed in the first slot (upper-left) of the shulker box. All the other slots of the shulker box are available payload slots, and are filled with oak logs. After the package is ready, it's passed to the terminal, which immediately handles it to the underlying transport system responsible for moving the shulker box from this terminal to the nearest router.
> Note that in this phase, the shulker box preparation can either be manual or automated, as we will see later on. 

The transport layer physically moves the shulker box around the world, until it reaches the first Router. The package enters the router from the inboud port, and is processed (depending on traffic requriements, an inbound package queue could be needed inside the router, meaning that the package might not be processed immediately). The destination tag is extracted from the shulker box and matched against the routing table, then it's re-inserted inside the shulker box in the same slot. If a port mapped to that destination was found, the shulker box is placed it the respective outbound buffer (if no port was found, it's up to the designer to decide what to do: fallback port? store for later?). Once the package has reached the outbound buffer, it's the transport's job to hop the package from the current location to the next one. Depending on the complexity of the network, the next hop location could either be another router, where exactly the same process happens, or simply be the destination terminal. In this case, we assume it's the destination terminal "smlter-2".

The package has therefore been succesfully moved around the world, and is handed to the destination terminal by the transport which places it in a final container, where it can be later be gathered by players or machines.


## Implementing full industrial automation using the RDS

We have seen how the RDS is capable of dinamically moving a package full of resources from a point A to a point B of a minecraft world. Although this could theoretically be used as-is by players to help out in resource transfer, realistically, there are more practical way to move large quantities of items around, such as using elytras and rockets. However, since the RDS is fully automatic, we can use it to connect any amount of factories togheter in a fully automatic way. Factories can dinamically share resources between each other even across potentially large distances in the world; not only that, but the RDS already provides a standardized interconnected web-like transportation infranstructure that is able to fullfill all possible dependencies needs the factories might require.
For example, if factory A and B are both dependent of outputs of factory C, the RDS already achieves the goal of allowing items to move both from C to A and from C to B, without having to build a specialized point-to-point transportation system for each pair of interested endpoints. As another example, say factory C also depends on the products of factory E and F; again, the RDS naturally allows for item transportation from E and F to C with ease. It's now clear how this can be used for large scale industrial automation projects.

### Service-Client pattern
This architectural pattern is used whenever there is an entity providing some kind of service, which multiple clients can ask for. In general, if a client wants to use that service, it makes a request to the service host, and the host answers back with the requested material from the client.  
In our context, this could be useful in creating factories that require periodic resource refills. For example there could be a cake factory that produces cakes. To do so, it needs to have a storage of all the needed resources (eggs, wheat, sugar, milk). In an automation context, we can image that, whenever those resources run low, the cake factory can automatically make a request to the factories it depends on (eggs farm, wheat farm etc..) to obtain a resource refill. How can we implement this using the RDS?  

A way to approach this would be to send two packages: one for the request, only containing information, and one for the response, containing the actual asked resource.  
For basic material requests, a request package needs to carry two crucial informations:
- Source address: The address from which the request is originating from; or, in other words, where to send the response back (tipically the sender's address)
- Request type: what kind of action is requested.

These two informations can easily be shared using two renamed items carried in the package payload (in the 2nd and 3rd slots of the shulker box, leaving the rest empty). Of course, the service host requires some additional redstone mechanism to parse the request automatically, execute the requested action, and then construct a response package and send it to the specified client address by the client. The details and technology of this process could be standardized, but it's not a strict requirements as long as the service host follows the described protocol.  
In the previous example of the cake factory, the origin information can be stored in a ready-to-use RDS destination tag named for example "cake-fact" and the request type could be encoded in another renamed item, for example "EGG-REFILL-qt10" (somehow indicating that we want to refill 10 stacks of eggs). On the egg farm side, the response package is constructed using the provided "cake-fact" destination tag as a destination, to send the resources back to the client (the cake farm).

### ...Some more ideas:
#### Centralized Storage
Instead of having resources move from one factory to another, a large central item-sorter and storage building could be created, where all resources are automatically moved to. This way, instead of contacting directly the required factory for a refill, factories could just ask the the storage for material. 

#### Usage of nether
All the infranstructure of the RDS could easily be constructed on the nether roof, allowing generally faster transportation times due to the nether to overworld distances ratio of 1:8, although it has to be noted that some transport tecnhologies might be unvaiablable in the nether, such as water conveyor belts.


## State of Tech
As of now, the RDS *Router* and *Terminal* entities do have viable redstone implementations, although they might not be optimal in terms of speed and volume. It the current state, each Router can differentiate up to 54 different destinations PER port. If more are needed, two ports can just be wired together to the same underlying transport. Each added port adds 2 blocks to the lenght of the building, making it 2blocks tilable. Routers have a process time (time for each package) of a 5+ seconds, that linearly increases by about 0.5s with each added port.  
Terminals as of now offer no abstraction over the underlying transport layer, since they just expose places to put/pick up packages to and from the network (in the tests only the water "conveyor belt" transport has been used, so the terminals are literally just holes where shulker boxes can be dropped into the network / received from the network).

As of now there is no redstone implementation for the service-client pattern.