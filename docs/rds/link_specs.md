# RDS Link Specifications

This document defines what a Link is in the Resource Distribution System (RDS) and how it operates in abstract terms. Any system that meets these requirements can function as a Link.

## What's a Link

If you don't know what a Link is, you can find a introductory explanation [*here*](/docs/rds/rds_overview.md#-link).

## Abstract Definition

A Link is the infrastructure needed to physically transport a Package from a source location to a end location. Every Link design is based around a Package transportation technology, which in turn is highly coupled to the choosen Package technology. For example, for ShulkerBox based Packages, any technology capable of transporting items can be a valid Link technology; For ChestMinecart based Packages, any tecnhology capable of moving Minecarts (mainly, rails) can be a valid Link technology. 

Links uniquely connect two and *only* two points. In a graph, a Link is therefore a single segment, which cannot contain any branches or junctions (that's what a Router is for). Generally, a Link is always directed, meaning that it can only move Package in one direction (e.g. from A → B); in this case, the Link is called **half-duplex**. However, a design may also conveniently implement a simmetric structure that allows for travel in both directions (e.g. A ⇔ B). In such a case, the Link is called **full-duplex**. 

Unlike Routers, Links do not make routing decisions. Their sole responsibility is handling the physical movement of Packages.
Links are also tipically protocol-agnostic, as their only job is to transfer the Package container, not to inspect/interact with its payload. This means that the same Link design can be used for networks that use the same Package technology but not the same protocol *(see more about protocols [here](./rds_protocols.md))*.

Links mainly perform the following two-point connections:

- Terminal → Router
- Router → Router
- Router → Terminal

Each complete transfer from the origin point to the destination point a Link performs is called a **Hop**. The complete journey of a Package from source to destination consists of multiple Hops performed by different Links, possibly using different technologies.

Different Link technologies may be combined within the same network. For example, one Hop might use water streams while another uses minecarts. This flexibility allows designs to adapt to environmental constraints and performance requirements.

### Working Principle

The general workflow of a Link is as follows:

1. Receive a Package from a input *gate*
2. Move the Package
3. Release the Package into a output *gate*

Routing logic and destination decisions are handled by Routers. Transports simply execute movement once a routing decision has been made.

> By ***gate*** we simply refer to anything that marks the boundary between a Link and a Router/Terminal. For example, a Router's Output Port is the *input gate* of a Link, and a Router's Input port is the *output gate* of a Link.




### High-Importance Hops and Transport Security

Some Hops in an RDS network carry greater importance than others. For example, connections between layer-1 Routers form backbone routes on which valuable resources might travel, meaning that they require stronger guarantees of reliability and security. In these situations, Transport design should consider the risk of item loss, interference, or malicious tampering by players. While automated systems are the foundation of the RDS, high-importance routes might benefit from active player surveillance to prevent unauthorized interaction.

It is also worth acknowledging that human-based transports — where players physically move Packages or supervise their movement — may be a viable solution for critical backbones or high-security links in servers where an economy/job system exists.
