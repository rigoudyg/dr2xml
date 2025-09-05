Configuring dr2xml
==================

The configuration of dr2xml is related to several aspects:
   - several settings given as arguments to dr2xml
   - the Data Request used
   - the reference project
   - the settings associated the with lab and the model
   - the settings associated with the simulation

Let's review those different elements before describing the ones available.

Settings provided to dr2xml as arguments
----------------------------------------
The main function of dr2xml is :func:`dr2xml.generate_file_defs`.
Its arguments can be used to make general configuration of dr2xml (i.e. not related to a specific experiment).

.. autofunction:: dr2xml.generate_file_defs

The Data Request used and the Controlled Vocabulary associated
--------------------------------------------------------------
The Data Request is one base of dr2xml.
It is the place where the variables to be output are defined.
The Data Request can be very complicated (as for CMIP6) and associated with a specific Controlled Vocabulary where
default values can be found.

Currently, three types of Data Request can be used in dr2xml:
   - the CMIP6 Data Request (default one)
   - a C3S seasonal forecast kind of Data Request (json-like file with defined entries)
   - no Data Request (in this case, the definitions of the variables are given through json-like tables and everything
     must be defined)

The reference project
---------------------
The reference project define the settings that are available (and needed for some).
It also describe the way of getting the values and the default, if any.
The project define also the attributes of the XIOS related object (metadata, attributes) and the structure of the name
of the output files.

All the projects inherit from the :module:`dr2xml.projects.basics` one, which is built on
:module:`dr2xml.projects.dr2xml`.
Beside those projects, the ones available currently for "real" usage are:
   - :module:`dr2xml.projects.CMIP6` (default) for CMIP6 kind' usages
   - :module:`dr2xml.projects.CORDEX` for CORDEX-CMIP5 kind' usages
   - :module:`dr2xml.projects.CORDEX-CMIP6` for CORDEX-CMIP6 kind' usages
   - :module:`dr2xml.projects.C3S-SF` for C3S seasonal forecast kind' usages

The settings defined in the projects are splitted in three categories (determined in this order):
   - the internal settings which are required to run dr2xml
   - the common settings which are used after having be read once at the launch of dr2xml
   - for each XIOS-related object, the settings associated with this object (attributes and meta-data)
That means that a setting in the common list can be defined from an other one in the internal list but not the reverse.

The lab and model settings
--------------------------
More specific than the project settings, the lab and model settings aims at defining all the parameters that are common
for a laboratory and a model.
The idea is to have a single file that can be used for all the simulations made with one model in one laboratory.

The simulation settings
-----------------------
The simulation settings is the more specific one. It is adapted to a single simulation and give, in a way, the elements
which are different from the lab and model settings or which are too specific to be defined at an other level.
