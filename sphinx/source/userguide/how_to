How to start with a new model/laboratory?
=========================================

This section aims at giving a few tips to start with the use of dr2xml with a new model/laboratory.

First, from where to start?
---------------------------

The first step is to have XIOS working in the targetted model.
One it is the case, that's means that you have many of the initialized files needed (fields, grids...).

Then, the simplest way to start with dr2xml is to use an existing configuration and to adapt it.
The notebook `DR2xml.ipynb` or the script `examples/DR2xml.py` are good starting points as long as unitary tests.

Deal with a new laboratory
--------------------------

The short name of the new laboratory is specified in the lab_and_model_settings.py using the `institution_id` key.
It is used to get information from outer sources (including CVs for CMIP6) to determine metadada and also to determine
which variables should be output or not following lab grid policy. Lab grid policy can be seen as a first set of
filtering on grids on which variables are output.

For CNRM-CERFACS, the file is already included in the repository under `dr2xml.laboratories.CNRM-CERFACS.py`.
For other groups, this file must be created (can be a copy of the CNRM-CERFACS one's with the new lab's name) and adapted if needed.
The location of this file should be added in lab_and_model_settings.py using key `laboratory_used`).
It can also be integrated in the repository.

Other keys such as `contact` will have to be updated (but it is not mandatory at this stage).

Creating ping files
-------------------

Ping files are used to make the link between the names defined in the fields definitions (i.e. the 'model' names) and the names defined in the data request.
Example of ping files are in tests/common/xml_files directory.

To create ping files, you can use the notebook `create_ping_files.ipynb` or adapt the tests under tests/test_pingfiles_*.

Deal with a new model
---------------------

Then, the next step is to define the model within the lab_and_model_settings.py file.

First, the different grids of the model (if several, list all), must defined in `grids` and `sizes` for each context as
long as the sampling timestep in `sampling_timestep`. You must also defined the list of mips associated with each grid
in `mips` (can be a void set if no filtering should be applied).

Then, for each model id, you must provide:
   - the grid associated with this model `grid_choice` (if a model is associated with several grids, you must provide two different ids)
   - the types of sources associated with each model using `source_types`
   - for child simulations, the start year in parent simulation must be provided in `branching`
   - the `configuration` should also be updated

And then?
---------

You should now be able to start playing with dr2xml for your model.

Keep in mind that dr2xml will try to take into account all the requirements you give but may fail and just set a
warning if it does not manage to find everything.