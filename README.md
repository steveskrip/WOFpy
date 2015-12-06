
# WOFpy

WOFpy is a Python package that implements [CUAHSI's](http://his.cuahsi.org) WaterOneFlow Web service.  WaterOneFlow is a Web service with methods for querying time series of water data at point locations, and which returns data in WaterML format, providing standardized access to water data.   

WOFpy reads data from a Data Access Object (DAO) and translates the data into WaterML.  DAOs can represent a variety of data sources, including databases, text files, and Web sites or services.  You can view example DAOs in the examples folder, or write your own based on the BaseDao class in wof/dao.py.

WOFpy uses Python version 2.7.

Documentation
-------------

Extensive documentation is available at http://pythonhosted.org/WOFpy/

Installation
------------

Follow the steps below for Basic installation on a Windows computer.

1. Install **Python 2.7**.  The 32-bit installer is recommended.
2. Add the **Python** folder to your **Path** environment variable.
3. Install **setuptools**. This allows the setup script to be run.
4. Add the **Python/scripts** folder to your **Path** environment variable.
5. Open a command window (run cmd), navigate to the WOFpy folder (with setup.py
   in it), and enter this command: ``python setup.py install``

The wof package (in the subfolder named wof) is now accessible from any directory.

Note: If you edit code in the **wof** folder, you may need to run setup.py again to apply the changes to your system.

ODM2 and ODM1 Instructions
--------------------------
This is new material that is up to date. The sections "Running the Examples" and "Publishing Your Data", below, *might* be out of date.
- [ODM2](https://github.com/ODM2/WOFpy/blob/master/docs/Sphinx/ODM2Services.rst)
- [ODM1](https://github.com/ODM2/WOFpy/blob/master/docs/Sphinx/ODM1Services.rst)

Running the Examples
--------------------

Example services are included with WOFpy.  Each example consists of data, Data
Access Objects (DAOs), models, and the service definition.  The examples are
located in the **examples** folder.  See the documentation for more information.  

Publishing Your Data
--------------------

Follow the general steps below to publish your data with WOFpy.

1. Write a new DAO class based on wof.dao.BaseDao; the methods should return objects as defined in wof.models.  This class helps WOFpy read your data. 
2. Write a new config file like those found in the examples, e.g. examples/swis/swis_config.cfg. This file contains static descriptors of your Web service such as the name of your water observations network.
3. Write a new runserver script to use the new DAO you implemented.  See files named runserver_*.py in the examples folder for examples.
4. To test, open a command window, navigate where your runserver file is located, and use Python to run the script, e.g., python runserver.py.

Unit Tests
----------

After everything is installed, open a command window and navigate to your WOFpy/test/ folder.  Type "nosetests -v" to run the included tests.  If they all pass, then congratulations!
