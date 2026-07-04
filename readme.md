# Minecraft Industrial Web Framework

The MC Industrial Web Framework (MCIWF) is a set of architectural principles, designs, standards and ideas aimed at providing a structured and organized way to create an efficient and fully automated network of factories in 
**Vanilla Minecraft**.

It defines standardized methods for how factories located across the world can share resources, periodically or on demand, fully automatically, adopting common networking patterns such as service–client and point-to-point transfer.  

The backbone of the framework is the **Resource Distribution System (RDS)**, a layered and highly customizable system designed for automated point-to-point resource sharing across the Minecraft world (both of entities and items/blocks), inspired by the inner workings and behavior of real-world Internet networks. 

### Motivations

The Minecraft ecosystem of automated redstone transportation systems has grown vast, diverse, and largely uncoordinated. Countless creators have built their own systems, each solving the same core problem in a different, often incompatible way. This project aims to formalize a set of universal standards so that redstone designs can interoperate, ultimately forming a unified, extensible library for players constructing automated transport networks.

The purpose of this repo is:
- to contain extensive documentation providing a solid theoretical foundation to all ideas and principles related to the Minecraft Industrial Web Framework.
- to create a web library of detailed redstone designs, where redstoners can publish their designs and where players can look for for a design that best suites their needs (using a custom search engine, to navigate designs more easily).


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

If you are a creator and you want to publish your own design of a component or system to the library, simply follow the rules described in the [contributing](/docs/repo_structure.md#contributing) section.

If you are new to the project and want to know what it's about, start with **Overview** to get started. For deeper technical details, consult the techincal *specs.md* files.

Contributions and pull requests are very welcome — whether they focus on theoretical ideas, redstone implementations, or documentation improvements!
