# Minecraft Industrial Web Framework

<figure style="text-align: center;">
  <img src="graphics/r.gif" width="500" alt="Directory tree">
  <figcaption>Figure 1 — Directory tree structure</figcaption>
</figure>

The MC Industrial Web Framework is a set of architectural principles, protocols, and ideas aimed at providing a structured and organized way to create an efficient and fully automated network of factories in vanilla Minecraft. It defines standardized methods for how factories located across the world can share resources on demand, fully automatically.

The backbone of the framework is the **Resource Distribution System (RDS)**, a layered system designed for automated and efficient point-to-point resource sharing, inspired by the structure and behavior of real-world Internet networks. 

## Documentation

- [Overview (high-level description)](overview.md)  
- [Router specification](router_specs.md)  
- [Transport specification](transports_specs.md)

Advanced:

- [Hierarchical routing](hierarchical_routing.md)  

---

## Contributing / Using This Spec

This repository is a specification and design reference for building systems using the Industrial Web Framework. If you want to create your own implementation, simply follow the rules described in the documentation. Any machine that respects the specifications is compatible with the RDS network.

If you are new to the project, start with **overview.md**. For deeper technical details, consult the router and transport specifications.

Contributions are very welcome — whether they focus on theoretical ideas, redstone implementations, or documentation improvements. Pull requests and suggestions help refine the framework and make it more useful for everyone.