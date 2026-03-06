## Goal of this repository

This repository is structured to host both high‑level abstract documentation and concrete implementations of all the devices and entities involved in the **Minecraft Industrial Web Framework**. 
The documentation contains abstract specifications, design references, and architectural guides. These materials are stored in the /docs folder, and they indexed through `readme.md` to be easily navigated.

All implementations are collected under the `/implementations` directory. Each individual implementation resides in a folder named after the abstract class of the device it realizes (Router, Link, Package, Terminal). Contributors may add their own custom implementations, which will be organized following the same directory structure.

## Contributing
If you are a redstone engineer / creator, and would like to contribute by providing your own redstone implementation of a RDS entity, feel free to fork and clone the repo, and add your design by making a pull request!

To add a new implementation, refer to the implementation entry **template** folder, located in each respective Entity folder under `/implementations`. Fill all the required specifications information for your creation, and follow the guidelines suggested in the template's *specs.md* file itself to create a good documentation for your creation.

You can also contribute by improving or adding newer documentation. If the documentation you are adding is tighly RDS-coupled, then it makes sense for it to live near all the other official documentation files, inside the `/docs` folder.  
If the documentation you are adding is related to your specific project or system (for example, if you are working on an implementation *suite*), place it in a custom folder inside `/docs/user-contributed`.