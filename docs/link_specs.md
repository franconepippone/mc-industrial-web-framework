# RDS Transport Specifications

This document defines what a Transport is in the Resource Distribution System (RDS) and how it operates in abstract terms. Any system that meets these requirements can function as an RDS Transport.

> NOTE: In the RDS implementation, a Package is a Shulker Box. Transports move these Packages between locations.


## Abstract Definition

### Purpose

A Transport is any mechanism capable of moving Packages from one location to another.

Unlike Routers, Transports do not make routing decisions. Their sole responsibility is physical movement.

The Transport Layer connects:

- Terminal → Router
- Router → Router
- Router → Terminal

Each movement between two nodes is called a **Hop**. A complete journey from source to destination consists of multiple Hops performed by Transports.


### Working Principle

Transports operate as carriers. They:

1. Receive a Package from a source buffer
2. Move the Package to a destination buffer
3. Do not inspect or modify the Package contents

Routing logic and destination decisions are handled by Routers. Transports simply execute movement once a routing decision has been made.


### Technology Neutrality

Any Minecraft technology capable of moving items qualifies as a Transport, provided it satisfies the movement requirement.

Examples include:

- Flowing water conveyor systems
- Minecart with Chest on rails
- Item streams using hoppers or similar mechanisms

Different technologies may be combined within the same network. For example, one Hop might use water streams while another uses minecarts. This flexibility allows designs to adapt to environmental constraints and performance requirements.


---

## Requirements

To function as a valid Transport in an RDS network, an implementation must:

- Move Packages between buffers
- Not alter or inspect Package contents
- Operate independently of routing logic
- Support movement in one or more Hops
- Allow interoperability with other Transport types

If these requirements are met, the system qualifies as an RDS Transport.

### High-Importance Hops and Transport Security

Some Hops in an RDS network carry greater importance than others. For example, connections between layer-1 Routers form backbone routes on which valuable resources might travel, meaning that they require stronger guarantees of reliability and security. In these situations, Transport design should consider the risk of item loss, interference, or malicious tampering by players. While automated systems are the foundation of the RDS, high-value routes might benefit from additional safeguards such as restricted access areas, protected conveyor paths, or player guard mechanisms that monitor and prevent unauthorized interaction.

It is also worth acknowledging that human-based transports — where players physically move Packages or supervise their movement — may be used for critical backbones or high-security links.