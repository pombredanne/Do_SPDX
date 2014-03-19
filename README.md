Do_SPDX
=======
A configurable SPDX generator module for python.

Introduction
------------

The Do_SPDX project looks to extract the spdx generation from the yocto project into an object oriented, flexible, and configurable module in python. The project looks to achieve this through a sleek command line interface, configurable database caching, and implementing the do_spdx functionality in a Python class.

Installation
------------

Assumptions: The user has both mySQL and Python 2.7.6 installed. 
You can download the Python 2.7.6 installer [here](https://www.python.org/download/releases/2.7.6/ "Python 2.7.6 download").  
The mySQL installer can be found [here for linux](http://dev.mysql.com/doc/refman/5.1/en/linux-installation.html "MySQL Linux Installation") and [here for windows](http://dev.mysql.com/doc/refman/5.1/en/windows-installation.html "MySQL Windows Installation").  

To install Do_SPDX, clone [this](https://github.com/chaughawout/Do_SPDX) git repo. Everything should be ready to go from there!

Usage
-----

There are two ways to configure your runtime for Do_SPDX. The first way involves the do_spdx.cfg config file, the other requires a user to supply the values in the config file as arguments on the command line. I recommend using do_spdx.cfg for simplicity and clarity's sake.  

The do_spdx.cfg file contains the current required arguments and their types under the [Setting Schema] section. Use this as a template for your customized cfg file. For a more in depth description of how each argument is used, read the Process section of this README.

To run Do_SPDX, simply execute it with python, e.g.:  
`python do_spdx.py mypackage.tar.gz -c do_spdx.cfg`  
or  
`python do_spdx.py mypackage.tar.gz -o -f /example/output/path.txt -a "John Smith" -t Fossology -pn "Apache" -pv 3 -sv 1.2 -d "MIT" -sd "/tmp/path"`

Obviously it is much nicer to use the configuration file over the raw command line interface. There are more plans in the work to expand upon the options in the configuration file, such as database parameters, scanner parameters, etc. This README will be updated as these are implemented.

Overview
--------




Contributing
------------

To contribute to this project, please Fork this repo and begin making pull-requests. Any bugs should be reported to this repo's bug tracker. You may also contact the owner directly at `corbin.haughawout@gmail.com`

Troubleshooting
---------------



Licensing
---------

This software is licensed under the Apache License, Version 2.0.

