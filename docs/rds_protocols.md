# RDS Protocols

In order for Packages to succesfully traverse a RDS network, all the devices involved in the routing of the Package (Routers, Links, Terminals) must agree on the rules on *how* the Address Stamp and resources are carried. For a quick reminder, in order to be correctly routed, a Package needs to be marked with a Address Stamp, that encodes a unique identifier for its destination.

In general, there are many valid ways of achieving this. The RDS supports only on one implementation, called the **Standard RDS Protocol**. Throughout this documentation, this protocol is assumed by default unless explicitly stated otherwise. Any network or device that follows it is considered **RDS‑compliant**.

Devices operating under different protocols are considered **non‑RDS‑compliant**, and while they can coexist within an RDS‑compliant environment, their integration requires the considerations described in the [dedicated section](#support-for-custom-protocols).


## The Standard RDS Protocol

This protocol is the official protocol adopted by the Resource Distribution System, meaning that every device that operates in a RDS-compliant network *must* be compatible with it.

#### Address Stamp
In the **Standard RDS Protocol**, the Address Stamp is an **Item**, potentially renamed, that acts as a unique identifier for a Destination. Any 64-stackable item can be a valid Address Stamp; however, conventionally, a single item type is choosen (e.g. Paper) and renamed according to the destination it uniquely identifies.

The Address Stamp Item is stored in the **first non-empty slot** of the Package inventory. This means that when the Package is handed to an item extractor (mainly, a hopper) the Address Stamp must be the first item that comes out. On the other side, when the Address Stamp item is automatically inserted inside the Package inventory (with droppers, hoppers), it must, again, still occupy the first non-empty slot of the container. 

The conventional slot used for an Address Stamp is the first slot (top-left) of the Package Inventory, as this maximizes the amount of payload that can be carried.

#### Payload
Anything that follows the Address Stamp inside the Package Inventory is considered payload, and this can be any minecraft item/s. Payload is generally not touched by the Routers and Links of a RDS network, and might only be handled by Terminals if they implement some kind of automatic Package filling/emptying system.




## Support for Custom Protocols

Custom protocols can be designed and adopted when they offer advantages for specific use cases. However, all reference designs and implementations provided in this repository are built around the **Standard RDS Protocol**. Introducing a different protocol generally requires developing new components or re‑implementing the existing RDS entities from the ground up, since their behavior is tightly coupled to the adopted protocol.

When a non‑RDS‑compliant network must interoperate with an RDS‑compliant one, dedicated **Protocol Adapters** are required. These components, typically placed at the link level, translate Address Stamps, routing semantics, and resource‑handling rules between the two protocols. This makes mixed‑protocol environments technically feasible, but significantly increases system complexity. Unless external constraints mandate the use of a custom protocol, relying on the Standard RDS Protocol remains the recommended approach.
