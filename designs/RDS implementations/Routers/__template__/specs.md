
<!-- Insert here the name of your Router -->
# Router Name

## Description

Provide a short and clear presentation of the router:

- What the router does  
- What problem it solves  
- Its original design goals (performance, compactness, scalability, simplicity, etc.)  
- Optional: links to videos, images, or demonstrations  

If more detailed technical explanations are required, create separate documentation files (e.g. `documentation.md`) files and reference them in here.

---

## Specifications

> **Note**: *Physical* Input Ports refer to the amount of physical input Link connections the router has. The number of *Logical* ports for a Router is **1**, unless specified.

<!--
If the Router has more that one logical input port, for example, if it's capable of source-port-based routing (discussed in router_specs.md), add the following entry below the "Physical Ports (I/O)":
| Logical Ports (I/O)   | #in_p
>


<!-- 
Conventionally, N represents the number of ports for scalable designs that can be expanded to any number of ports.  
It can be used in formulas below (for example in footprint expression).
Uncomment the line below if your are using N.  
> `N` represents the number of Output Ports. 
-->

<!--
Package Technology must reference an existing specification file
located under implementations/Packages.

Do NOT write a free-text name only.
Always link to the corresponding spec file of the implementation.

If the technology you are using does not yet exist in
implementations/Packages, create and document the new Package
Technology there first, then reference it here.
-->


|  Specification   | Value |
|----------------------|-------|
| Design Version    | 1.0
| Minecraft Version     | <Java / Bedrock / Both> and version id (e.g. 1.21.2) 
| Component Class       | [RDS Router](/docs/router_specs.md) 
| Package Technology    | <e.g. [ChestMinecart](/implementations/Packages/ChestMinecart/specs.md) / Other>
| Protocol              | <e.g [Standard RDS Protocol](/docs/rds_protocols.md#the-standard-rds-protocol) / Other>  
| Physical Ports (I/O)             | #in_p -> N (#in_p is the number of input ports, e.g. 1 -> 4) 
| Footprint (Area)      | <e.g. 20×(20 + 2N)> 
| Height                | <e.g. 32>
| Works in Nether       | <Yes / No>
| Chunkloading Included | <Yes / No> 
| Package Queue Included        | <Yes / No>
| Empty Package Safe    | <Yes / No>  If it can handle empty packages without breaking, which can happen by error 
| Throughput            | <e.g. 15 Pkg/min> 
| Survival-friendliness  | <High / Moderate / Low>

---

## Notes

Add any additional implementation notes, limitations, quirks, or build guides can be written or referenced here.

If there are other implementations that work well with this Router, reference them here.

If this router is part of a larger suite (a group of implementations designed to work together and possibly requiring shared external documentation):

- Provide a slightly description of the suite.
- Link to the official suite documentation, which must be located in `docs/user-contributed/your-custom-suite/`.

## Changelog

Only add this if you are updating versions