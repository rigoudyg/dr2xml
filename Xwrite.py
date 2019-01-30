#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
XIOS writing files tools.
"""
from Xparse import id2gridid, idHasExprWithAt
from cfsites import cfsites_domain_id, add_cfsites_in_defs
from config import get_config_variable
from dict_interface import get_variable_from_lset_with_default, get_variable_from_lset_without_default, \
    get_variable_from_sset_with_default, get_source_id_and_type, get_variable_from_sset_without_default, \
    get_variable_from_sset_else_lset_with_default, is_key_in_lset, is_key_in_sset
from dr2xml import ping_alias, conventions, version, warnings_for_optimisation
from dr_interface import get_DR_version
from grids import change_domain_in_grid, change_axes_in_grid, get_grid_def_with_lset
from postprocessing import process_vertical_interpolation, process_zonal_mean, process_diurnal_cycle
from settings import DRgrid2gridatts, analyze_cell_time_method, freq2datefmt, longest_possible_period, \
    Cmip6Freq2XiosFreq
from split_frequencies import split_frequency_for_variable
from utils import dr2xml_error
from vars import get_simplevar
from vars_selection import get_sc, endyear_for_CMORvar


def wr(out, key, dic_or_val=None, num_type="string", default=None):
    global print_wrv
    if not print_wrv: return
    """
    Short cut for a repetitive pattern : writing in 'out' 
    a string variable name and value
    If dic_or_val is not None 
      if  dic_or_val is a dict, 
        if key is in value is dic_or_val[key], 
        otherwise use default as value , except if default is False
      otherwise, use arg dic_or_val as value if not None nor False,
    otherwise use value of local variable 'key'
    """
    val = None
    if type(dic_or_val) == type({}):
        if key in dic_or_val:
            val = dic_or_val[key]
        else:
            if default is not None:
                if default is not False: val = default
            else:
                print 'error : %s not in dic and default is None' % key
    else:
        if dic_or_val is not None:
            val = dic_or_val
        else:
            print 'error in wr,  no value provided for %s' % key
    if val:
        if num_type == "string":
            # val=val.replace(">","&gt").replace("<","&lt").replace("&","&amp").replace("'","&apos").replace('"',"&quot").strip()
            val = val.replace(">", "&gt").replace("<", "&lt").strip()
            # CMIP6 spec : no more than 1024 char
            val = val[0:1024]
        if num_type != "string" or len(val) > 0:
            out.write('  <variable name="%s"  type="%s" > %s ' % (key, num_type, val))
            out.write('  </variable>\n')


def write_xios_file_def(sv, year, table, lset, sset, out, cvspath,
                        field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, file_defs,
                        dummies, skipped_vars_per_table, actually_written_vars,
                        prefix, context, grid, pingvars=None, enddate=None,
                        attributes=[], debug=[]):
    """
    Generate an XIOS file_def entry in out for :
      - a dict for laboratory settings
      - a dict of simulation settings
      - a 'simplifed CMORvar' sv
      - which all belong to given table
      - a path 'cvs' for Controlled Vocabulary

    Lenghty code, but not longer than the corresponding specification document

    1- After a prologue, attributes valid for all variables are
    written as file-level metadata, in the same order than in
    WIP document;
    2- Next, field-level metadata are written
    3- For 3D variables in model levels or half-levels, also write the auxilliary
    variables requested by CF convention (e.g. for hybrid coordinate, surface_pressure field
    plus AP and B arrays and their bounds, and lev + lev_bnds with formula attribute)
    """
    #
    # If list of included vars has size 1, activate debug on the corresponding variable
    inc = get_variable_from_lset_with_default('included_vars', [])
    if len(inc) == 1: debug = inc

    # gestion des attributs pour lesquels on a recupere des chaines vides (" " est Faux mais est ecrit " "")
    # --------------------------------------------------------------------
    # Put a warning for field attributes that shouldn't be empty strings
    # --------------------------------------------------------------------
    # if not sv.stdname       : sv.stdname       = "missing" #"empty in DR "+get_DR_version()
    if not sv.long_name:
        sv.long_name = "empty in DR " + get_DR_version()
    # if not sv.cell_methods  : sv.cell_methods  = "empty in DR "+get_DR_version()
    # if not sv.cell_measures : sv.cell_measures = "cell measure is not specified in DR "+get_DR_version()
    if not sv.units:
        sv.units = "empty in DR " + get_DR_version()

    # --------------------------------------------------------------------
    # Define alias for field_ref in file-def file
    # - may be replaced by alias1 later
    # - this is not necessarily the alias used in ping file because of
    #   intermediate field id(s) due to union/zoom
    # --------------------------------------------------------------------
    # We use a simple convention for variable names in ping files :
    if sv.type == 'perso':
        alias = sv.label
    else:
        # MPM : si on a defini un label non ambigu alors on l'utilise comme alias (i.e. le field_ref)
        # et pour l'alias seulement (le nom de variable dans le nom de fichier restant svar.label)
        if sv.label_non_ambiguous:
            alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.label_non_ambiguous
        else:
            # 'tau' is ambiguous in DR 01.00.18 : either a variable name (stress)
            # or a dimension name (optical thickness). We choose to rename the stress
            if sv.label != "tau":
                alias = get_variable_from_lset_without_default("ping_variables_prefix") + sv.label
            else:
                alias = get_variable_from_lset_without_default("ping_variables_prefix") + "tau_stress"
        if (sv.label in debug):
            print "write_xios_file_def ... processing %s, alias=%s" % (sv.label, alias)

        # suppression des terminaisons en "Clim" pour l'alias : elles concernent uniquement les cas
        # d'absence de variation inter-annuelle sur les GHG. Peut-etre genant pour IPSL ?
        # Du coup, les simus avec constance des GHG (picontrol) sont traitees comme celles avec variation
        split_alias = alias.split("Clim")
        alias = split_alias[0]
        if pingvars is not None:
            # Get alias without pressure_suffix but possibly with area_suffix
            alias_ping = ping_alias(sv, pingvars)
    #
    # process only variables in pingvars
    if not alias_ping in pingvars:
        # print "+++ =>>>>>>>>>>>", alias_ping, " ", sv.label
        table = sv.mipTable
        if table not in skipped_vars_per_table: skipped_vars_per_table[table] = []
        skipped_vars_per_table[table].append(sv.label + "(" + str(sv.Priority) + ")")
        return
    #
    # --------------------------------------------------------------------
    # Set global CMOR file attributes
    # --------------------------------------------------------------------
    #
    project = get_variable_from_sset_with_default('project', "CMIP6")
    source_id, source_type = get_source_id_and_type()
    experiment_id = get_variable_from_sset_without_default('experiment_id')
    institution_id = get_variable_from_lset_without_default('institution_id')
    #
    contact = get_variable_from_sset_else_lset_with_default('contact', default=None)
    #
    # Variant matters
    realization_index = get_variable_from_sset_with_default('realization_index', 1)
    initialization_index = get_variable_from_sset_with_default('initialization_index', 1)
    physics_index = get_variable_from_sset_with_default('physics_index', 1)
    forcing_index = get_variable_from_sset_with_default('forcing_index', 1)
    variant_label = "r%di%dp%df%d" % (realization_index, initialization_index, \
                                      physics_index, forcing_index)
    variant_info_warning = ". Information provided by this attribute may in some cases be flawed. " + \
                           "Users can find more comprehensive and up-to-date documentation via the further_info_url global attribute."
    #
    # WIP Draft 14 july 2016
    mip_era = get_variable_from_lset_with_default(sv.mip_era)
    #
    # WIP doc v 6.2.0 - dec 2016
    # <variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc
    member_id = variant_label
    sub_experiment_id = get_variable_from_sset_with_default('sub_experiment_id', 'none')
    if sub_experiment_id != 'none':
        member_id = sub_experiment_id + "-" + member_id
    #
    # --------------------------------------------------------------------
    # Set grid info
    # --------------------------------------------------------------------
    if grid == "":
        # either native or close-to-native
        grid_choice = get_variable_from_lset_without_default('grid_choice', source_id)
        grid_label, target_hgrid_id, zgrid_id, grid_resolution, grid_description = \
            get_variable_from_lset_without_default('grids', grid_choice, context)
    else:
        if grid == 'cfsites':
            target_hgrid_id = cfsites_domain_id
            zgrid_id = None
        else:
            target_hgrid_id = get_variable_from_lset_without_default("ping_variables_prefix") + grid
            zgrid_id = "TBD : Should create zonal grid for CMIP6 standard grid %s" % grid
        grid_label, grid_resolution, grid_description = DRgrid2gridatts(grid)

    if table[-1:] == "Z":  # e.g. 'AERmonZ','EmonZ', 'EdayZ'
        grid_label += "z"
        # Below : when reduction was done trough a two steps sum, we needed to divide afterwards
        # by the nmber of longitudes
        #
        # if is_key_in_lset("nb_longitudes_in_model") and get_variable_from_lset_without_default("nb_longitudes_in_model", context):
        #     # Get from settings the name of Xios variable holding number of longitudes and set by model
        #     nlonz=get_variable_from_lset_without_default("nb_longitudes_in_model", context) # e.g.: nlonz="ndlon"
        # elif context_index.has_key(target_hgrid_id):
        #     # Get the number of longitudes from xml context_index
        #     # an integer if attribute of the target horizontal grid, declared in XMLs: nlonz=256
        #     nlonz=context_index[target_hgrid_id].attrib['ni_glo']
        # else:
        #     raise dr2xml_error("Fatal: Cannot access the number of longitudes (ni_glo) for %s\
        #                 grid required for zonal means computation "%target_hgrid_id)
        # print ">>> DBG >>> nlonz=", nlonz

    if "Ant" in table:
        grid_label += "a"
    if "Gre" in table:
        grid_label += "g"
    #
    with open(cvspath + project + "_experiment_id.json", "r") as json_fp:
        CMIP6_CV_version_metadata = json.loads(json_fp.read())['version_metadata']
        CMIP6_CV_latest_tag = CMIP6_CV_version_metadata.get('latest_tag_point', 'no more value in CMIP6_CV')
    #
    with open(cvspath + project + "_experiment_id.json", "r") as json_fp:
        CMIP6_experiments = json.loads(json_fp.read())['experiment_id']
        if not CMIP6_experiments.has_key(get_variable_from_sset_without_default('experiment_id')):
            raise dr2xml_error("Issue getting experiment description in CMIP6 CV for %20s" % sset['experiment_id'])
        expid = get_variable_from_sset_without_default('experiment_id')
        expid_in_filename = get_variable_from_sset_with_default('expid_in_filename', expid)
        if "_" in expid_in_filename:
            raise dr2xml_error("Cannot use character '_' in expid_in_filename (%s)" % expid_in_filename)
        exp_entry = CMIP6_experiments[expid]
        experiment = exp_entry['experiment']
        description = exp_entry['description']
        activity_id = get_variable_from_lset_with_default('activity_id', exp_entry['activity_id'])
        parent_activity_id = get_variable_from_lset_with_default('parent_activity_id', get_variable_from_lset_with_default('activity_id', exp_entry['parent_activity_id']))
        if type(parent_activity_id) == type([]):
            parent_activity_id = reduce(lambda x, y: x+" "+y, parent_activity_id)
        if is_key_in_sset('parent_experiment_id'):
            parent_experiment_id = get_variable_from_sset_with_default('parent_experiment_id')
        else:
            parent_experiment_id = reduce(lambda x, y: x+" "+y, exp_entry['parent_experiment_id'])
        required_components = exp_entry['required_model_components']  # .split(" ")
        allowed_components = exp_entry['additional_allowed_model_components']  # .split(" ")
    #
    # Check model components re. CV components
    actual_components = source_type.split(" ")
    ok = True
    for c in required_components:
        if c not in actual_components:
            ok = False
            print "Model component %s is required by CMIP6 CV for experiment %s and not present (present=%s)" % \
                  (c, experiment_id, `actual_components`)
    for c in actual_components:
        if c not in allowed_components and c not in required_components:
            ok = False or get_variable_from_sset_with_default('bypass_CV_components', False)
            print "Warning: Model component %s is present but not required nor allowed (%s)" % \
                  (c, `allowed_components`)
    if not ok: raise dr2xml_error("Issue with model components")
    #
    # --------------------------------------------------------------------
    # Set NetCDF output file name according to the DRS
    # --------------------------------------------------------------------
    #
    date_range = "%start_date%-%end_date%"  # XIOS syntax
    operation, detect_missing, foo = analyze_cell_time_method(sv.cell_methods, sv.label, table, printout=False)
    # print "--> ",sv.label, sv.frequency, table
    date_format, offset_begin, offset_end = freq2datefmt(sv.frequency, operation, table)
    #
    if "fx" in sv.frequency:
        filename = "%s%s_%s_%s_%s_%s_%s" % \
                   (prefix, sv.label, table, source_id, expid_in_filename, member_id, grid_label)
    else:
        varname_for_filename = sv.mipVarLabel
        if get_variable_from_lset_with_default('use_cmorvar_label_in_filename', False):
            varname_for_filename = sv.label
        # DR21 has a bug with tsland : the MIP variable is named "ts"
        if sv.label == "tsland":
            varname_for_filename = "tsland"
        # WIP doc v6.2.3 : a suffix "-clim" should be added if climatology
        # if False and "Clim" in sv.frequency: suffix="-clim"
        if sv.frequency in ["1hrCM", "monC"]:
            suffix = "-clim"
        else:
            suffix = ""
        filename = "%s%s_%s_%s_%s_%s_%s_%s%s" % \
                   (prefix, varname_for_filename, table, source_id, expid_in_filename,
                    member_id, grid_label, date_range, suffix)
    #
    if is_key_in_lset('mip_era'):
        further_info_url = "https://furtherinfo.es-doc.org/%s.%s.%s.%s.%s.%s" % (
            mip_era, institution_id, source_id, expid_in_filename,
            sub_experiment_id, variant_label)
    else:
        further_info_url = ""
    #
    # --------------------------------------------------------------------
    # Compute XIOS split frequency
    # --------------------------------------------------------------------
    sc = get_sc()
    resolution = get_variable_from_lset_without_default('grid_choice', source_id)
    split_freq = split_frequency_for_variable(sv, resolution, sc.mcfg, context)
    # Cap split_freq by setting max_split_freq (if expressed in years)
    if split_freq[-1] == 'y':
        max_split_freq = get_variable_from_sset_with_default('max_split_freq', None)
        if max_split_freq is None:
            max_split_freq = get_variable_from_lset_with_default('max_split_freq', None)
        if max_split_freq is not None:
            if max_split_freq[0:-1] != "y":
                dr2xml_error("max_split_freq must end with an 'y' (%s)" % max_split_freq)
            split_freq = "%dy" % min(int(max_split_freq[0:-1]), int(split_freq[0:-1]))
    # print "split_freq: %-25s %-10s %-8s"%(sv.label,sv.mipTable,split_freq)
    #
    # --------------------------------------------------------------------
    # Write XIOS file node:
    # including global CMOR file attributes
    # --------------------------------------------------------------------
    out.write(' <file id="%s_%s_%s" name="%s" ' % (sv.label, table, grid_label, filename))
    freq = longest_possible_period(Cmip6Freq2XiosFreq(sv.frequency, table), get_variable_from_lset_with_default("too_long_periods", []))
    out.write(' output_freq="%s" ' % freq)
    out.write(' append="true" ')
    out.write(' output_level="%d" ' % get_variable_from_lset_with_default("output_level", 10))
    out.write(' compression_level="%d" ' % get_variable_from_lset_with_default("compression_level", 0))
    if not "fx" in sv.frequency:
        out.write(' split_freq="%s" ' % split_freq)
        out.write(' split_freq_format="%s" ' % date_format)
        #
        # Modifiers for date parts of the filename, due to silly KT conventions.
        if offset_begin is not False:
            out.write(' split_start_offset="%s" ' % offset_begin)
        if offset_end is not False:
            out.write(' split_end_offset="%s" ' % offset_end)
        lastyear = None
        # Try to get enddate for the CMOR variable from the DR
        if sv.cmvar is not None:
            # print "calling endyear_for... for %s, with year="%(sv.label), year
            lastyear = endyear_for_CMORvar(sv.cmvar, expid, year, sv.label in debug)
            # print "lastyear=",lastyear," enddate=",enddate
        if lastyear is None or (enddate is not None and lastyear >= int(enddate[0:4])):
            # DR doesn't specify an end date for that var, or a very late one
            if get_variable_from_lset_with_default('dr2xml_manages_enddate', True):
                # Use run end date as the latest possible date
                # enddate must be 20140101 , rather than 20131231
                if enddate is not None:
                    endyear = enddate[0:4]
                    endmonth = enddate[4:6]
                    endday = enddate[6:8]
                    out.write(' split_last_date="%s-%s-%s 00:00:00" ' % (endyear, endmonth, endday))
                else:
                    out.write(' split_last_date=10000-01-01 00:00:00" ')
        else:
            # Use requestItems-based end date as the latest possible date when it is earlier than run end date
            if (sv.label in debug):
                print "split_last_date year %d derived from DR for variable %s in table %s for year %d" % (
                lastyear, sv.label, table, year)
            endyear = "%04d" % (lastyear + 1)
            if lastyear < 1000:
                dr2xml_error(
                    "split_last_date year %d derived from DR for variable %s in table %s for year %d does not make sense except maybe for paleo runs; please set the right value for 'end_year' in experiment's settings file" % (
                    lastyear, sv.label, table, year))
            endmonth = "01"
            endday = "01"
            out.write(' split_last_date="%s-%s-%s 00:00:00" ' % (endyear, endmonth, endday))
    #
    # out.write('timeseries="exclusive" >\n')
    out.write(' time_units="days" time_counter_name="time"')
    out.write(' time_counter="exclusive"')
    out.write(' time_stamp_name="creation_date" ')
    out.write(' time_stamp_format="%Y-%m-%dT%H:%M:%SZ"')
    out.write(' uuid_name="tracking_id" uuid_format="hdl:21.14100/%uuid%"')
    out.write(' convention_str="%s"' % conventions)
    # out.write(' description="A %s result for experiment %s of %s"'%
    #            (lset['source_id'],sset['experiment_id'],sset.get('project',"CMIP6")))
    out.write(' >\n')
    #
    if type(activity_id) == type([]):
        activity_idr = reduce(lambda x, y: x + " " + y, activity_id)
    else:
        activity_idr = activity_id
    wr(out, 'activity_id', activity_idr)
    #
    if contact and contact is not "": wr(out, 'contact', contact)
    wr(out, 'data_specs_version', get_DR_version())
    wr(out, 'dr2xml_version', version)
    #
    wr(out, 'experiment_id', expid_in_filename)
    if experiment_id == expid_in_filename:
        wr(out, 'description', description)
        wr(out, 'title', description)
        wr(out, 'experiment', experiment)
    #
    # Fixing cell_measures is done in vars.py
    #
    dynamic_comment = ""
    if "seaIce" in sv.modeling_realm and 'areacella' in sv.cell_measures and sv.label != "siconca":
        dynamic_comment = '. Due an error in DR01.00.21 and to technical constraints, this variable may have  attribute cell_measures set to area: areacella, while it actually is area: areacello'

    #
    # When remapping occurs to a regular grid -> CF does not ask for cell_measure
    # but CMIP6 do ask for it !
    # if grid_label[0:2]=='gr': sv.cell_measures=""
    # TBD : find a way to provide an areacella field for variables which are remapped to a 'CMIP6' grid such as '1deg'

    #
    # CF rule : if the file variable has a cell_measures attribute, and
    # the corresponding 'measure' variable is not included in the file,
    # it must be quoted as external_variable
    external_variables = ''
    if "area:" in sv.cell_measures:
        external_variables += " " + re.sub(".*area: ([^ ]*).*", r'\1', sv.cell_measures)
    if "volume:" in sv.cell_measures:
        external_variables += " " + re.sub(".*volume: ([^ ]*).*", r'\1', sv.cell_measures)
    if 'fx' in table:
        external_variables = ""
    if external_variables:
        wr(out, 'external_variables', external_variables)
    #
    #
    wr(out, 'forcing_index', forcing_index, num_type="int")
    wr(out, 'frequency', sv.frequency)
    #
    if further_info_url:
        wr(out, 'further_info_url', further_info_url)
    #
    wr(out, 'grid', grid_description);
    wr(out, 'grid_label', grid_label);
    wr(out, 'nominal_resolution', grid_resolution)
    comment = get_variable_from_lset_with_default('comment', '') + " " + get_variable_from_sset_with_default('comment', '') + dynamic_comment
    wr(out, 'comment', comment)
    wr(out, 'history', sset, default='none')
    wr(out, "initialization_index", initialization_index, num_type="int")
    wr(out, "institution_id", institution_id)
    if is_key_in_lset('institution'):
        inst = get_variable_from_lset_without_default('institution')
    else:
        with open(cvspath + project + "_institution_id.json", "r") as json_fp:
            try:
                inst = json.loads(json_fp.read())['institution_id'][institution_id]
            except:
                raise dr2xml_error("Fatal: Institution_id for %s not found " + \
                                   "in CMIP6_CV at %s" % (institution, cvspath))
    wr(out, "institution", inst)
    #
    with open(cvspath + project + "_license.json", "r") as json_fp:
        license = json.loads(json_fp.read())['license'][0]
    # mpmoine_cmor_update: 'licence' est trop long... passe pas le CMIP6-Checker => 'institution_id' au lieu de inst='institution'
    license = license.replace("<Your Centre Name>", institution_id)
    license = license.replace("[NonCommercial-]", "NonCommercial-")
    license = license.replace("[ and at <some URL maintained by modeling group>]",
                              " and at " + get_variable_from_lset_without_default("info_url"))
    wr(out, "license", license)
    wr(out, 'mip_era', mip_era)
    #
    if parent_experiment_id and parent_experiment_id != 'no parent' and parent_experiment_id != ['no parent']:
        wr(out, 'parent_experiment_id', reduce(lambda x, y: x + " " + y, parent_experiment_id))
        wr(out, 'parent_mip_era', sset, default=mip_era)
        wr(out, 'parent_activity_id', reduce(lambda x, y: x + " " + y, parent_activity_id))
        wr(out, 'parent_source_id', sset, default=source_id)
        # TBD : syntaxe XIOS pour designer le time units de la simu courante
        parent_time_ref_year = get_variable_from_sset_with_default('parent_time_ref_year', "1850")
        parent_time_units = "days since %s-01-01 00:00:00" % parent_time_ref_year
        wr(out, 'parent_time_units', sset, default=parent_time_units)
        wr(out, 'parent_variant_label', sset, default=variant_label)
        wr(out, 'branch_method', sset, default='standard')
        # Use branch year in parent if available
        if is_key_in_sset("branch_year_in_parent") and source_id in get_variable_from_lset_without_default('branching'):
            if experiment_id in get_variable_from_lset_without_default('branching', source_id) and \
                    get_variable_from_sset_without_default("branch_year_in_parent") not in get_variable_from_lset_without_default('branching', source_id, experiment_id, 1):
                dr2xml_error(
                    "branch_year_in_parent (%d) doesn't belong to the list of branch_years declared for this experiment %s" \
                    % (get_variable_from_sset_without_default("branch_year_in_parent"), get_variable_from_lset_without_default('branching', source_id, experiment_id, 1)))
            date_branch = datetime.datetime(get_variable_from_sset_without_default("branch_year_in_parent"), get_variable_from_sset_with_default("branch_month_in_parent", 1), 1)
            date_ref = datetime.datetime(int(parent_time_ref_year), 1, 1)
            nb_days = (date_branch - date_ref).days
            wr(out, 'branch_time_in_parent', "%d.0D" % nb_days, "double")
        else:
            wr(out, 'branch_time_in_parent', sset, "double")
        # Use branch year in child if available
        if is_key_in_sset("branch_year_in_parent"):
            date_branch = datetime.datetime(get_variable_from_sset_without_default("branch_year_in_child"), 1, 1)
            date_ref = datetime.datetime(get_variable_from_sset_without_default("child_time_ref_year"), 1, 1)
            nb_days = (date_branch - date_ref).days
            wr(out, 'branch_time_in_child', "%d.0D" % nb_days, "double")
        else:
            wr(out, 'branch_time_in_child', sset, "double")
    #
    wr(out, "physics_index", physics_index, num_type="int")
    wr(out, 'product', 'model-output')
    wr(out, "realization_index", realization_index, num_type="int")
    # Patch for an issue id DR01.0021 -> 01.00.24
    crealm = sv.modeling_realm
    if crealm == "ocnBgChem":
        crealm = "ocnBgchem"
    wr(out, 'realm', crealm)
    wr(out, 'references', lset, default=False)
    #
    try:
        with open(cvspath + project + "_source_id.json", "r") as json_fp:
            sources = json.loads(json_fp.read())['source_id']
            source = make_source_string(sources, source_id)
    except:
        if is_key_in_lset('source'):
            source = get_variable_from_lset_without_default('source')
        else:
            raise dr2xml_error("Fatal: source for %s not found in CMIP6_CV at" + \
                               "%s, nor in lset" % (source_id, cvspath))
    wr(out, 'source', source)
    wr(out, 'source_id', source_id)
    if type(source_type) == type([]):
        source_type = reduce(lambda x, y: x + " " + y, source_type)
    wr(out, 'source_type', source_type)
    #
    wr(out, 'sub_experiment_id', sub_experiment_id)
    wr(out, 'sub_experiment', sset, default='none')
    #
    wr(out, "table_id", table)
    #
    if not is_key_in_sset('expid_in_filename'):
        wr(out, "title", "%s model output prepared for %s / " % ( \
            source_id, project) + activity_idr + " " + experiment_id)
    else:
        wr(out, "title", "%s model output prepared for %s and " % ( \
            source_id, project) + activity_idr + " / " + expid_in_filename + " simulation")
    #
    # DR21 has a bug with tsland : the MIP variable is named "ts"
    if sv.label != "tsland":
        wr(out, "variable_id", sv.mipVarLabel)
    else:
        wr(out, "variable_id", "tsland")
    #
    variant_info = get_variable_from_sset_with_default('variant_info', "none")
    if variant_info != "none" and variant_info != "": variant_info += variant_info_warning
    if variant_info != "": wr(out, "variant_info", variant_info)
    wr(out, "variant_label", variant_label)
    for name, value in attributes: wr(out, name, value)
    non_stand_att = get_variable_from_lset_with_default("non_standard_attributes", dict())
    for name in non_stand_att: wr(out, name, non_stand_att[name])
    #
    # --------------------------------------------------------------------
    # Build all XIOS auxilliary elements (end_file_defs, field_defs, domain_defs, grid_defs, axis_defs)
    # ---
    # Write XIOS field entry
    # including CF field attributes
    # --------------------------------------------------------------------
    end_field = create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs,
                                           dummies, context, target_hgrid_id, zgrid_id, pingvars)
    out.write(end_field)
    if sv.spatial_shp[0:4] == 'XY-A' or sv.spatial_shp[0:3] == 'S-A':  # includes half-level cases
        # create a field_def entry for surface pressure
        # print "Searching for ps for var %s, freq %s="%(alias,freq)
        sv_psol = get_simplevar("ps", table, sv.frequency)

        if sv_psol:
            # if not sv_psol.cell_measures : sv_psol.cell_measures = "cell measure is not specified in DR "+get_DR_version()
            psol_field = create_xios_aux_elmts_defs(sv_psol, get_variable_from_lset_without_default("ping_variables_prefix") + "ps", table, field_defs,
                                                    axis_defs, grid_defs, domain_defs, scalar_defs, dummies, context,
                                                    target_hgrid_id, zgrid_id, pingvars)
            out.write(psol_field)
        else:
            print "Warning: Cannot complement model levels with psol for variable %s and table %s" % \
                  (sv.label, sv.frequency)

    #
    names = {}
    if sv.spatial_shp == 'XY-A' or sv.spatial_shp == 'S-A':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names = {"ap": "vertical coordinate formula term: ap(k)",
                 "ap_bnds": "vertical coordinate formula term: ap(k+1/2)",
                 "b": "vertical coordinate formula term: b(k)",
                 "b_bnds": "vertical coordinate formula term: b(k+1/2)"}
    if sv.spatial_shp == 'XY-AH' or sv.spatial_shp == 'S-AH':
        # add entries for auxilliary variables : ap, ap_bnds, b, b_bnds
        names = {"ahp": "vertical coordinate formula term: ap(k)",
                 "ahp_bnds": "vertical coordinate formula term: ap(k+1/2)",
                 "bh": "vertical coordinate formula term: b(k)",
                 "bh_bnds": "vertical coordinate formula term: b(k+1/2)"}
    for tab in names:
        out.write('\t<field field_ref="%s%s" name="%s" long_name="%s" operation="once" prec="8" />\n' % \
                  (get_variable_from_lset_without_default("ping_variables_prefix"), tab, tab.replace('h', ''), names[tab]))
    out.write('</file>\n\n')
    actually_written_vars.append((sv.label, sv.long_name, sv.mipTable, sv.frequency, sv.Priority, sv.spatial_shp))


def create_xios_aux_elmts_defs(sv, alias, table, field_defs, axis_defs, grid_defs, domain_defs, scalar_defs, dummies,
                               context, target_hgrid_id, zgrid_id, pingvars):
    """
    Create a field_ref string for a simplified variable object sv (with
    lab prefix for the variable name) and returns it

    Add field definitions for intermediate variables in dict field_defs
    Add axis  definitions for interpolations in dict axis_defs
    Use pingvars as the list of variables actually defined in ping file

    """
    # By convention, field references are built as prefix_<MIP_variable_name>
    # Such references must be fulfilled using a dedicated field_def
    # section implementing the match between legacy model field names
    # and such names, called 'ping section'
    #
    # Identify which 'ping' variable ultimatley matches the requested
    # CMOR variable, based on shapes. This may involve building
    # intermediate variables, in order to  apply corresponding operations

    # The preferred order of operation is : vertical interp (which
    # is time-dependant), time-averaging, horizontal operations (using
    # expr=@this)
    #
    # --------------------------------------------------------------------
    # Build XIOS axis elements (stored in axis_defs)
    # Proceed with vertical interpolation if needed
    # ---
    # Build XIOS auxilliary field elements (stored in field_defs)
    # --------------------------------------------------------------------
    ssh = sv.spatial_shp
    prefix = get_variable_from_lset_without_default("ping_variables_prefix")

    # The id of the currently most downstream field is last_field_id
    last_field_id = alias

    alias_ping = ping_alias(sv, pingvars)
    context_index = get_config_variable("context_index")
    grid_id_in_ping = id2gridid(alias_ping, context_index)
    last_grid_id = grid_id_in_ping
    # last_grid_id=None
    #
    grid_with_vertical_interpolation = None

    # translate 'outermost' time cell_methods to Xios 'operation')
    operation, detect_missing, clim = analyze_cell_time_method(sv.cell_methods, sv.label, table, printout=False)
    #
    # --------------------------------------------------------------------
    # Handle vertical interpolation, both XY-any and Y-P outputs
    # --------------------------------------------------------------------
    #
    # if ssh[0:4] in ['XY-H','XY-P'] or ssh[0:3] == 'Y-P' or \
    # must exclude COSP outputs which are already interpolated to height or P7 levels
    if (ssh[0:4] == 'XY-P' and ssh != 'XY-P7') or \
            ssh[0:3] == 'Y-P' or \
            ((ssh[0:5] == 'XY-na' or ssh[0:4] == 'Y-na') and
             prefix + sv.label not in pingvars and sv.label_without_psuffix != sv.label):  # TBD check - last case is for singleton
        last_grid_id, last_field_id = process_vertical_interpolation(sv, alias, pingvars, last_grid_id, field_defs,
                                                                     axis_defs, grid_defs, domain_defs, table)

    #
    # --------------------------------------------------------------------
    # Handle the case of singleton dimensions
    # --------------------------------------------------------------------
    #
    if has_singleton(sv):
        last_field_id, last_grid_id = process_singleton(sv, last_field_id, pingvars, field_defs, grid_defs, scalar_defs,
                                                        table)
    #
    # TBD : handle explicitly the case of scalars (global means, shape na-na) : enforce <scalar name="sector" standard_name="region" label="global" >, or , better, remove the XIOS-generated scalar introduced by reduce_domain
    #
    # --------------------------------------------------------------------
    # Handle zonal means
    # --------------------------------------------------------------------
    #
    if ssh[0:2] == 'Y-':  # zonal mean and atm zonal mean on pressure levels
        last_field_id, last_grid_id = \
            process_zonal_mean(last_field_id, last_grid_id, target_hgrid_id, zgrid_id, field_defs, axis_defs, grid_defs,
                               domain_defs, operation, sv.frequency)

    #
    # --------------------------------------------------------------------
    # Build a construct for computing a climatology (if applicable)
    # --------------------------------------------------------------------
    if clim:
        if sv.frequency == "1hrCM":
            last_field_id, last_grid_id = process_diurnal_cycle(last_field_id, \
                                                                field_defs, grid_defs, axis_defs)
        else:
            raise dr2xml_error("Cannot handle climatology cell_method for frequency %s and variable " % \
                               sv.frequency, sv.label)
    #
    # --------------------------------------------------------------------
    # Create intermediate field_def for enforcing operation upstream
    # --------------------------------------------------------------------
    #
    but_last_field_id = last_field_id
    last_field_id = last_field_id + "_" + operation
    field_defs[last_field_id] = '<field id="%-25s field_ref="%-25s operation="%-10s/>' \
                                % (last_field_id + '"', but_last_field_id + '"', operation + '"')
    #
    # --------------------------------------------------------------------
    # Change horizontal grid if requested
    # --------------------------------------------------------------------
    #
    if target_hgrid_id:
        # This does not apply for a series of shapes
        if ssh[0:2] == 'Y-' or ssh == 'na-na' or ssh == 'TR-na' or ssh == 'TRS-na' or ssh[
                                                                                      0:3] == 'YB-' or ssh == 'na-A':
            pass
        else:
            if target_hgrid_id == cfsites_domain_id:
                add_cfsites_in_defs(grid_defs, domain_defs)
            # Apply DR required remapping, either toward cfsites grid or a regular grid
            last_grid_id = change_domain_in_grid(target_hgrid_id, grid_defs, src_grid_id=last_grid_id)
    #
    # --------------------------------------------------------------------
    # Change axes in grid to CMIP6-compliant ones
    # --------------------------------------------------------------------
    #
    last_grid_id = change_axes_in_grid(last_grid_id, grid_defs, axis_defs)
    #
    # --------------------------------------------------------------------
    # Create <field> construct to be inserted in a file_def, which includes re-griding
    # --------------------------------------------------------------------
    #
    if last_grid_id != grid_id_in_ping:
        gref = 'grid_ref="%s"' % last_grid_id
    else:
        gref = ""

    rep = '  <field field_ref="%s" name="%s" %s ' % (last_field_id, sv.mipVarLabel, gref)
    #
    #
    # --------------------------------------------------------------------
    # Add offset if operation=instant for some specific variables defined in lab_settings
    # --------------------------------------------------------------------
    #
    if operation == 'instant':
        for ts in get_variable_from_lset_with_default('special_timestep_vars', []):
            if sv.label in get_variable_from_lset_without_default('special_timestep_vars', ts):
                xios_freq = Cmip6Freq2XiosFreq(sv.frequency, table)
                # works only if units are different :
                rep += ' freq_offset="%s-%s"' % (xios_freq, ts)
    #
    # --------------------------------------------------------------------
    # handle data type and missing value
    # --------------------------------------------------------------------
    #
    detect_missing = "True"
    missing_value = "1.e+20"
    if sv.prec.strip() in ["float", "real", ""]:
        prec = "4"
    elif sv.prec.strip() == "double":
        prec = "8"
    elif sv.prec.strip() == "integer" or sv.prec.strip() == "int":
        prec = "2";
        missing_value = "0"  # 16384"
    else:
        raise dr2xml_error("prec=%s for sv=%s" % (sv.prec, sv.label))
    rep += ' detect_missing_value="%s" \n\tdefault_value="%s" prec="%s"' % (detect_missing, missing_value, prec)
    #
    # TBD : implement DR recommendation for cell_method : The syntax is to append, in brackets,
    # TBD    'interval: *amount* *units*', for example 'area: time: mean (interval: 1 hr)'.
    # TBD    The units must be valid UDUNITS, e.g. day or hr.
    rep += ' cell_methods="%s" cell_methods_mode="overwrite"' % sv.cell_methods
    # --------------------------------------------------------------------
    # enforce time average before remapping (when there is one) except if there
    # is an expr, set in ping for the ping variable of that field, and which
    # involves time operation (using @)
    # --------------------------------------------------------------------
    if operation == 'once':
        freq_op = ""
    else:
        freq_op = 'freq_op="%s"' % \
                  longest_possible_period(Cmip6Freq2XiosFreq(sv.frequency, table),
                                          get_variable_from_lset_with_default("too_long_periods", []))
    #
    rep += ' operation="%s"' % operation
    if not idHasExprWithAt(alias, context_index):
        # either no expr, or expr without an @  ->
        # may use @ for optimizing operations order (average before re-gridding)
        if last_grid_id != grid_id_in_ping:
            if operation == 'average':
                # do use @ for optimizing :
                rep += ' %s>\n\t\t@%s' % (freq_op, last_field_id)
            elif operation == 'instant':
                # must set freq_op (this souldn't be necessary, but is needed with Xios 1442)
                if get_variable_from_lset_with_default("useAtForInstant", False):
                    rep += ' %s>\n\t\t@%s' % (freq_op, last_field_id)
                else:
                    rep += ' %s>' % (freq_op)
            else:
                # covers only case once , already addressed by freq_op value='' ?
                rep += ' >'
        else:
            # No remap
            rep += ' >'
    else:  # field has an expr, with an @
        # Cannot optimize
        if operation == 'instant':
            # must reset expr (if any) if instant, for using arithm. operation defined in ping.
            # this allows that the type of operation applied is really 'instant', and not the one
            # that operands did inherit from ping_file
            rep += ' expr="_reset_"'
        if (operation == 'average'):
            warnings_for_optimisation.append(alias)
        rep += ' %s>' % (freq_op)
    rep += '\n'
    #
    # --------------------------------------------------------------------
    # Add Xios variables for creating NetCDF attributes matching CMIP6 specs
    # --------------------------------------------------------------------
    comment = None
    # Process experiment-specific comment for the variable
    if sv.label in get_variable_from_sset_without_default('comments').keys():
        comment = get_variable_from_sset_without_default('comments', sv.label)
    else:  # Process lab-specific comment for the variable
        if sv.label in get_variable_from_lset_without_default('comments').keys():
            comment = get_variable_from_lset_without_default('comments', sv.label)
    if comment:
        rep += wrv('comment', comment)  # TBI
    #
    if sv.stdname:
        rep += wrv("standard_name", sv.stdname)
    #
    desc = sv.description
    # if desc : desc=desc.replace(">","&gt;").replace("<","&lt;").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;")
    if desc:
        desc = desc.replace(">", "&gt;").replace("<", "&lt;").strip()
    rep += wrv("description", desc)
    #
    rep += wrv("long_name", sv.long_name)
    if sv.positive != "None" and sv.positive != "":
        rep += wrv("positive", sv.positive)
    rep += wrv('history', 'none')
    if sv.units:
        rep += wrv('units', sv.units)
    if sv.cell_methods:
        rep += wrv('cell_methods', sv.cell_methods)
    if sv.cell_measures:
        rep += wrv('cell_measures', sv.cell_measures)
    #
    if sv.struct is not None:
        fmeanings = sv.struct.flag_meanings
        if fmeanings is not None and fmeanings.strip() != '':
            rep += wrv('flag_meanings', fmeanings.strip())
        fvalues = sv.struct.flag_values
        if fvalues is not None and fvalues.strip() != '':
            rep += wrv('flag_values', fvalues.strip())
    #
    # We override the Xios value for interval_operation because it sets it to
    # the freq_output value with our settings (for complicated reasons)
    if grid_with_vertical_interpolation:
        interval_op = get_variable_from_lset_without_default("vertical_interpolation_sample_freq")
    else:
        source, source_type = get_source_id_and_type()
        grid_choice = get_variable_from_lset_without_default("grid_choice", source)
        interval_op = `int(get_variable_from_lset_without_default('sampling_timestep', grid_choice, context))` + " s"
    if operation != 'once':
        rep += wrv('interval_operation', interval_op)

    # mpmoine_note: 'missing_value(s)' normalement plus necessaire, a verifier
    # TBS# rep+=wrv('missing_values',sv.missing,num_type="double")
    rep += '     </field>\n'
    #
    return rep


def process_singleton(sv, alias, pingvars, field_defs, grid_defs, scalar_defs, table):
    """
    Based on singleton dimensions of variable SV, and assuming that this/these dimension(s)
    is/are not yet represented by a scalar Xios construct in corresponding field's grid,
    creates a further field with such a grid, including creating the scalar and
    re-using the domain of original grid

    """

    printout = False
    # get grid for the variable , before vertical interpo. if any
    # (could rather use last_grid_id and analyze if it has pressure dim)
    alias_ping = ping_alias(sv, pingvars)
    context_index = get_config_variable("context_index")
    input_grid_id = id2gridid(alias_ping, context_index)
    input_grid_def = get_grid_def_with_lset(input_grid_id, grid_defs)
    if printout:
        print "process_singleton : ", "processing %s with grid %s " % (alias, input_grid_id)
    #
    further_field_id = alias
    further_grid_id = input_grid_id
    further_grid_def = input_grid_def
    #
    # for each sv's singleton dimension, create the scalar, add a scalar
    # construct in a further grid, and convert field to a further field
    for dimk in sv.sdims:
        sdim = sv.sdims[dimk]
        if is_singleton(sdim):  # Only one dim should match
            #
            # Create a scalar for singleton dimension
            # sdim.label is non-ambiguous id, thanks to the DR, but its value may be
            # ambiguous w.r.t. a dr2xml suffix for interpolating to a single pressure level
            scalar_id = "Scal" + sdim.label
            if sdim.units == '':
                unit = ''
            else:
                unit = ' unit="%s"' % sdim.units
            #
            if sdim.type == 'character':
                value = ' label="%s"' % sdim.label
            else:
                value = ' value="%s"' % sdim.value
                types = {'double': ' prec="8"', 'float': ' prec="4"', 'integer': ' prec="2"'}
                value = types[sdim.type] + " " + 'value="%s"' % sdim.value
            if sdim.axis != '':
                # Space axis, probably Z
                axis = ' axis_type="%s"' % (sdim.axis)
                if sdim.positive: axis += ' positive="%s"' % (sdim.positive)
            else:
                axis = ""
            if sdim.bounds == "yes":
                try:
                    bounds = sdim.boundsValues.split()
                    bounds_value = ' bounds="(0,1)[ %s %s ]" bounds_name="%s_bounds"' % \
                                   (bounds[0], bounds[1], sdim.out_name)
                except:
                    if sdim.label == "lambda550nm":
                        bounds_value = ''
                    else:
                        raise dr2xml_error("Issue for var %s with dim %s bounds=%s" % (sv.label, sdim.label, bounds))
            else:
                bounds_value = ""
            #
            name = sdim.out_name
            # These dimensions are shared by some variables with another sdim with same out_name ('type'):
            if sdim.label in ["typec3pft", "typec4pft"]: name = "pfttype"
            #
            if sdim.stdname.strip() == '' or sdim.label == "typewetla":
                stdname = ""
            else:
                stdname = 'standard_name="%s"' % sdim.stdname
            #
            scalar_def = '<scalar id="%s" name="%s" %s long_name="%s"%s%s%s%s />' % \
                         (scalar_id, name, stdname, sdim.title, value, bounds_value, axis, unit)
            scalar_defs[scalar_id] = scalar_def
            if printout:
                print "process_singleton : ", "adding scalar %s" % scalar_def
            #
            # Create a grid with added (or changed) scalar
            glabel = further_grid_id + "_" + scalar_id
            further_grid_def = add_scalar_in_grid(further_grid_def, glabel, scalar_id, \
                                                  name, sdim.axis == "Z")
            if printout:
                print "process_singleton : ", " adding grid %s" % further_grid_def
            grid_defs[glabel] = further_grid_def
            further_grid_id = glabel

    # Compare grid definition (in case the input_grid already had correct ref to scalars)
    if further_grid_def != input_grid_def:
        #  create derived_field through an Xios operation (apply all scalars at once)
        further_field_id = alias + "_" + further_grid_id.replace(input_grid_id + '_', '')
        # Must init operation and detect_missing when there is no field ref
        field_def = '<field id="%s" grid_ref="%s" operation="instant" detect_missing_value="true" > %s </field>' % \
                    (further_field_id, further_grid_id, alias)
        field_defs[further_field_id] = field_def
        if printout:
            print "process_singleton : ", " adding field %s" % field_def
    return further_field_id, further_grid_id


def has_singleton(sv):
    rep = any([is_singleton(sv.sdims[k]) for k in sv.sdims])
    return rep


def is_singleton(sdim):
    if sdim.axis == '':
        # Case of non-spatial dims. Singleton only have a 'value' (except Scatratio has a lot (in DR01.00.21))
        return sdim.value != '' and len(sdim.value.strip().split(" ")) == 1
    else:
        # Case of space dimension singletons. Should a 'value' and no 'requested'
        return ((sdim.value != '') and (sdim.requested.strip() == '')) \
               or (sdim.label == "typewetla")  # The latter is a bug in DR01.00.21 : typewetla has no value tehre


def add_scalar_in_grid(gridin_def, gridout_id, scalar_id, scalar_name, remove_axis, change_scalar=True):
    """
    Returns a grid_definition with id GRIDOUT_ID from an input grid definition
    GRIDIN_DEF, by adding a reference to scalar SCALAR_ID

    If CHANGE_SCALAR is True and GRIDIN_DEF has an axis with an extract_axis child,
    remove it (because it is assumed to be a less well-defined proxy for the DR scalar

    If such a reference is already included in that grid definition, just return
    input def

    if REMOVE_AXIS is True, if GRIDIN_DEF already includes an axis, remove it for output grid

    Note : name of input_grid is not changed in output_grid

    """
    format = '< *scalar *([^>]*)scalar_ref=["\']%s["\']'
    expr = format % scalar_id
    if re.search(expr, gridin_def):
        return gridin_def
    gridin_def = gridin_def.replace("\n", "")
    # TBD : in change_scalar : discard extract_axis only if really relevant (get the right axis)
    # TBD : in change_scalar : preserve ordering of domains/axes...
    if change_scalar:
        extract_pattern = "<scalar *>.*<extract_axis.*/> *</scalar *>"
        gridin_def, count = re.subn(extract_pattern, "", gridin_def)
    pattern = '< *grid *([^> ]*) *id=["\']([^"\']*)["\'] *(.*)</ *grid *>'
    replace = r'<grid \1 id="%s" \3<scalar scalar_ref="%s" name="%s"/>  </grid>' % (gridout_id, scalar_id, scalar_name)
    (rep, count) = re.subn(pattern, replace, gridin_def.replace("\n", ""))
    if count == 0: raise dr2xml_error("No way to add scalar '%s' in grid '%s'" % (scalar_id, gridin_def))
    #
    # Remove any axis if asked for
    if remove_axis:
        axis_pattern = '< *axis *[^>]*>'
        (rep, count) = re.subn(axis_pattern, "", rep)
        # if count==1 :
        #    print "Info: axis has been removed for scalar %s (%s)"%(scalar_name,scalar_id)
        #    print "grid_def="+rep
    return rep + "\n"


def wrv(name, value, num_type="string"):
    global print_wrv
    if not print_wrv: return ""
    if type(value) == type(""): value = value[0:1024]  # CMIP6 spec : no more than 1024 char
    # Format a 'variable' entry
    return '     <variable name="%s" type="%s" > %s ' % (name, num_type, value) + \
           '</variable>\n'


def make_source_string(sources, source_id):
    """
    From the dic of sources in CMIP6-CV, Creates the string representation of a
    given model (source_id) according to doc on global_file_attributes, so :

    <modified source_id> (<year>): atmosphere: <model_name> (<technical_name>, <resolution_and_levels>); ocean: <model_name> (<technical_name>, <resolution_and_levels>); sea_ice: <model_name> (<technical_name>); land: <model_name> (<technical_name>); aerosol: <model_name> (<technical_name>); atmospheric_chemistry <model_name> (<technical_name>); ocean_biogeochemistry <model_name> (<technical_name>); land_ice <model_name> (<technical_name>);

    """
    # mpmoine_correction:make_source_string: pour lire correctement le fichier 'CMIP6_source_id.json'
    source = sources[source_id]
    components = source['model_component']
    rep = source_id + " (" + source['release_year'] + "): "
    for realm in ["aerosol", "atmos", "atmosChem", "land", "ocean", "ocnBgchem", "seaIce"]:
        component = components[realm]
        description = component['description']
        if description != "none": rep = rep + "\n" + realm + ": " + description
    return rep
