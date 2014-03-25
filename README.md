Do_SPDX
=======

A configurable SPDX generator module for python.

Overview
--------

The Do_SPDX project looks to extract the spdx generation from the yocto project into an object oriented, flexible, and configurable module in python. The project looks to achieve this through a sleek command line interface, configurable database caching, and implementing the do_spdx functionality in a Python class.

Version
-------

Version 0.9; Changelog can be found [here](https://github.com/chaughawout/Do_SPDX/blob/master/CHANGELOG.md "do_spdx changelog").

License
-------

This software is licensed under the Apache License, Version 2.0. Which can be found [here](https://github.com/chaughawout/Do_SPDX/blob/master/LICENSE.md "Apache 2.0 License").

Copyright
---------

Copyright 2014 Corbin Haghawout, Joe Meyer, Ethan Harner under the Apache License, Version 2.0.

Technical Specs
---------------

Assumptions: The user has both mySQL and Python 2.7.6 installed. 
You can download the Python 2.7.6 installer [here](https://www.python.org/download/releases/2.7.6/ "Python 2.7.6 download").  
The mySQL installer can be found [here for linux](http://dev.mysql.com/doc/refman/5.1/en/linux-installation.html "MySQL Linux Installation") and [here for windows](http://dev.mysql.com/doc/refman/5.1/en/windows-installation.html "MySQL Windows Installation").

System Design
-------------

To follow Unix standards, all output will be assumed to go to stdout unless output is clarified in the configuration file they provide.

An image showing a data flow diagram (DFD) of this module can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/img/DFD.jpg). The decomposition for this DFD can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/documentation/dfd/DFD.md)

Installation
------------  

To install Do_SPDX, clone [this](https://github.com/chaughawout/Do_SPDX) git repo. Everything should be ready to go from there!

For detailed use cases, a command line installation use case can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/documentation/use%20cases/Command%20line%20install.md) and installing for use within a project can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/documentation/use%20cases/Instantiation%20install.md)

Usage
-----

There are two ways to configure your runtime for Do_SPDX. The first way involves the do_spdx.cfg config file, the other requires a user to supply the values in the config file as arguments on the command line. I recommend using do_spdx.cfg for simplicity and clarity's sake.  

The do_spdx.cfg file contains the current required arguments and their types under the [Setting Schema] section. Use this as a template for your customized cfg file. For a more in depth description of how each argument is used, read the Process section of this README.

To run Do_SPDX, simply execute it with python, e.g.:  
`python do_spdx.py mypackage.tar.gz -c do_spdx.cfg`  
or  
`python do_spdx.py mypackage.tar.gz -o -f /example/output/path.txt -a "John Smith" -t Fossology -pn "Apache" -pv 3 -sv 1.2 -d "MIT" -sd "/example/tmp/path"`

Obviously it is much nicer to use the configuration file over the raw command line interface. There are more plans in the work to expand upon the options in the configuration file, such as database parameters, scanner parameters, etc. This README will be updated as these are implemented.

For detailed use cases, a command line execution use cases can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/documentation/use%20cases/Run%20from%20command%20line.md) and an instantiation execution use case can be found [here] (https://github.com/chaughawout/Do_SPDX/blob/master/documentation/use%20cases/Run%20from%20instantiated%20object.md)

Communities of Interest
-----------------------

This project is most closely involved with the SPDX community but is open to anybody who is looking to automate the creation and validation of SPDX documents. Companies who consume or distribute products with open source might be interested in this project as a means to document their licensing for legal reasons. Since this project is licensed under Apache 2.0, any company may do as they wish with the source and tailor a solution from it for their needs.

Communication
-------------

To contribute to this project, please Fork this repo and begin making pull-requests. Any bugs should be reported to this repository's bug tracker so that a developer can pick it up and starting implementing a fix. You should contact the owner at `corbin.haughawout@gmail.com` if you find a potentially devestating problem.

Code Management
---------------

Source will be released in iterative cycles, with milestones set up by priority. The priority of different tasks fall in this order, from highest to lowest:
1. System critical bug-fixes and Failure in Security
   An error in the runtime or execution of the software that causes the system to fail or a security vulnerability is exposed. System dependent errors and configuration problems do not fall under this category. 
2. System critical feature additions
   Features that are required for the software to execute, i.e. a command line parser, or a database configuration process.
3. Non system critical bug-fixes
   An error in the software that results in unexpected behavior or output, i.e. improperly connecting to the database
4. New Feature additions
   New features are sections of code that provide entirely new functionality to the software.
5. Feature improvements
   As the lowest priority of tasks, users won't often see this rolling out in a version on it's own until the project is mature and well developed. These are improvements to already existing features, i.e. optimizations, re-implementation of existing code so that it is more efficient, cleaner to read, etc.

All changes and tasks should be documented in the issue tracker at the time of completion. Please document any code you are submitting a pull-request for so that it is easier for the community to read and understand what you're addition is doing. 

>Thanks
