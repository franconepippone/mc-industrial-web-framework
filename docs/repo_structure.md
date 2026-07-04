## Goal of this repository

This repository is structured to host both theoretical documentation and concrete redstone designs of all the entities and systems involved in the **Minecraft Industrial Web Framework**. 
The documentation contains abstract specifications for systems and devices, interoperability protocols that allow networks of different nature to work together, and networking architectural guides for constructing networks of every scale. These materials are stored in the /docs directory, and they are indexed through `readme.md` to be easily navigated.

All redstone designs are collected under the `/designs` directory. Designs are organized in subdirectories usually named after the class of the implemented device.  Each individual design is then organized in its own folder, and follows a standardized file layout. Contributors may add their own custom implementations, which must be organized according to the standard layout.

## Contributing
If you are a redstone engineer / creator, and would like to contribute by providing your own redstone implementation of a device, feel free add your design by making a pull request!

To add a new implementation, refer to the implementation entry **__template__** folder, located in each leaf folder under `/design`. Fill all the required specifications information for your creation, and follow the guidelines suggested in the template's *specs.md* file itself to create a good documentation for your creation.

You can also contribute by improving or adding newer documentation. If the documentation you are adding is tightly coupled to the MIWF, then it makes sense for it to live near all the other official documentation files, inside the `/docs` folder.  
If the documentation you are adding is related to your specific project or system (for example, if you are working on an implementation *suite*, providing a collection of designs that work well togheter), place it in a custom folder inside `/docs/user-contributed`, for example: `/docs/user-contributed/my-custom-docs`. You can later reference these docs inside the specification files of your designs, making navigation for the user easier.
