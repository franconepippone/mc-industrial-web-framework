# Minecraft Industrial Web Framework

The MC Industrial Web Framework (MCIWF) is a set of architectural principles, designs, standards and ideas aimed at providing a structured and organized way to create an efficient and fully automated network of factories in 
**Vanilla Minecraft**.

It defines standardized methods for how factories located across the world can share resources on demand, fully automatically, by implementing common architectural patterns such as service–client and point-to-point resource transfer.  

The backbone of the framework is the **Resource Distribution System (RDS)**, a layered and highly customizable system designed for automated point-to-point resource sharing (both of entities and items/blocks), inspired by the inner workings and behavior of real-world Internet networks. 

### Motivations

The Minecraft ecosystem of redstone inventions aimed at constructing automatic industrial networks is vast and complex. The aim of this project is to define some universal standards that redstone designs can adhere to, in order to create a vast and unified library of designs that can be used by players to build 

The purpose of this repo is:
-  to contain extensive documentation aimed at providing a solid theoretical foundation to all ideas related to the Minecraft Industrial Web Framework principles.
- to create a web library of redstone designs, where redstoners can publish their designs and where players can look for for a design that best suites their needs.


## Documentation Index

- [About this repo](docs/repo_structure.md) 

- [The Resource Distribution System](docs/rds/rds_overview.md)  
    - [Router specification](docs/rds/router_specs.md)  
    - [Link specification](docs/rds/link_specs.md)

        Advanced:

    - [Hierarchical routing](docs/rds/hierarchical_routing.md)  
    - [Custom protocols](docs/rds/rds_protocols.md#support-for-custom-protocols)  

---

## Contributing to the project

This repository is a specification and design reference for building systems using the Industrial Web Framework. If you want to create your own implementation, simply follow the rules described in the [contributing](/docs/repo_structure.md#contributing) section.

If you are new to the project and want to know what it's about, start with **Overview** to get started. For deeper technical details, consult the techincal *specs.md files.

Contributions and pull requests are very welcome — whether they focus on theoretical ideas, redstone implementations, or documentation improvements!
