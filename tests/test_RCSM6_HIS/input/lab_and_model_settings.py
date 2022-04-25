# -*- coding: utf-8 -*-

# This file is used for telling dr2xml a number of parameters that are dependant on the
# laboratory and models, and the default value for parameters that are dependant on the
# experiment (and which may be changed in a companion file 'experiment_settings.py'

# The plain user will usually not change anything here; the CMIP6 expert will, in
# agreement with the lab's CMIP6 point(s) of contact

# The reference documents are listed in top level document :https://pcmdi.llnl.gov/CMIP6/Guide/
# Of interest :
#   - paragraph 5 of https://pcmdi.llnl.gov/CMIP6/Guide/modelers.html
#   - CMIP6 Data Request , in browsable format: http://clipc-services.ceda.ac.uk/dreq/index.html


from tests.tests_config import path_xml
path_xml_aladin = "/".join([path_xml, "../xml_files_RCSM6_HIS"])

j_mean_comment = "This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. " \
                 "We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar " \
                 "grid, along which latitude do vary. This axis begins South. Please refer to the lat/lon coordinate " \
                 "variables in this file for further details."
sectors_comment_south = 'The sector attribute is erroneous, this variable is indeed integrated over the southern ' \
                        'hemisphere.'
sectors_comment_north = 'The sector attribute is erroneous, this variable is indeed integrated over the northern ' \
                        'hemisphere.'
CTRIP_rwb_comment = 'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr'
CTRIP_rgci = 'CTRIP river grid-cell inflow considering upstream grdi-cell water fluxes and total runoff input (mrro) ' \
             'from ISBA'
ISBA_leb = 'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : ' \
           'interval_operation'
ISBA_lwb = 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : ' \
           'interval_operation'

lab_and_model_settings = {
    'path_to_parse': '{}/'.format(path_xml_aladin),
    'comment': '',
    'tierMax': 1,
    'references': 'http://www.umr-cnrm.fr/',
    'realms_per_context': {
        'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgChem', 'seaIce ocean'],
        'surfex': ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land', 'landIce land', 'aerosol',
                   'land landIce', 'landIce'],
        'trip': []
    },
    'source': 'CORDEX',
    'fx_from_file': {
        'areacella': {'complete': {
            'HR': 'areacella_complete_CMIP6_tl359',
            'LR': 'areacella_complete_CMIP6_tl127'
        }},
        'C': {'REG': 'areacella_zoneC'}
    },
    'grid_choice': {
        'CNRM-ESM2-1': 'LR',
        'CNRM-CM6-1': 'LR',
        'CNRM-CM6-1-HR': 'HR',
        'CNRM-ALADIN64': 'REG',
        'CNRM-ESM2-1-HR': 'HR',
        'CNRM-RCSM6': 'REG'
    },
    'print_stats_per_var_label': True,
    'vertical_interpolation_sample_freq': '1h',
    'vertical_interpolation_operation': 'instant',
    'orphan_variables': {
        'nemo': [''],
        'surfex': ['siconca', ],
        'trip': ['areacellr', 'dgw', 'drivw', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd', 'fwtd', 'fldf', 'carbw',
                 'carbdis', 'carbin']
    },
    'CFsubhr_frequency': '2ts',
    'excluded_request_links': ['RFMIP-AeroIrf'],
    'max_priority': 1,
    'info_url': 'http://www.umr-cnrm.fr/',
    'use_cmorvar_label_in_filename': False,
    'allow_duplicates_in_same_table': False,
    'institution': 'CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France)',
    'allow_pseudo_standard_names': True,
    'sampling_timestep': {
        'HR': {'nemo': 1800.0, 'surfex': 900.0, 'trip': 1800.0},
        'LR': {'nemo': 1800.0, 'surfex': 900.0, 'trip': 1800.0},
        'REG': {'nemo': 1800.0, 'surfex': 900.0, 'trip': 1800.0}
    },
    'sizes': {
        'HR': [1514100, 75, 259200, 91, 30, 14, 128],
        'LR': [106428, 75, 32768, 91, 30, 14, 128],
        'REG': [106428, 75, 23040, 91, 30, 14, 128]
    },
    'source_types': {
        'CNRM-ESM2-1': 'AOGCM BGC AER CHEM',
        'CNRM-CM6-1': 'AOGCM',
        'CNRM-CM6-1-HR': 'AOGCM',
        'CNRM-ALADIN64': 'ARCM AER',
        'CNRM-ESM2-1-HR': 'AOGCM BGC AER',
        'CNRM-RCSM6': 'AORCM AER'
    },
    'print_variables': ['activity_id', 'description', 'comment', 'contact', 'Conventions', 'creation_date',
                        'data_specs_version', 'dr2xml_version', 'experiment_id', 'EXPID', 'external_variables',
                        'frequency', 'grid', 'grid_label', 'history', 'institution', 'institute_id',
                        'nominal_resolution', 'product', 'project_id', 'model_id', 'rcm_version_id',
                        'realization_index', 'realm', 'references', 'table_id', 'title', 'tracking_id', 'variable_id',
                        'xios_commit', 'standard_name', 'long_name', 'units', 'cell_methods', 'cell_measures',
                        'driving_experiment', 'driving_experiment_name', 'driving_model_id',
                        'driving_model_ensemble_member', 'CORDEX_domain', 'grid_mapping',
                        'Lambert_conformal_longitude_of_central_meridian', 'Lambert_conformal_standard_parallel',
                        'Lambert_conformal_latitude_of_projection_origin'
                        ],
    'configurations': {
        'LESM': ('CNRM-ESM2-1', 'LAND BGC', ['nemo']),
        'AGCM': ('CNRM-CM6-1', 'AGCM', ['nemo']),
        'OGCMHR': ('CNRM-CM6-1-HR', 'OGCM', ['surfex', 'trip']),
        'AOGCMHR': ('CNRM-CM6-1-HR', 'AOGCM', []),
        'AGCMAER': ('CNRM-CM6-1', 'AGCM AER', ['nemo']),
        'AOESMHR': ('CNRM-ESM2-1-HR', 'AOGCM BGC AER', []),
        'AESM': ('CNRM-ESM2-1', 'AGCM BGC AER CHEM', ['nemo']),
        'AORCM': ('CNRM-RCSM6', 'AORCM AER', []),
        'AGCMHR': ('CNRM-CM6-1-HR', 'AGCM', ['nemo']),
        'OESMHR': ('CNRM-ESM2-1-HR', 'OGCM BGC', ['surfex', 'trip']),
        'OESM': ('CNRM-ESM2-1', 'OGCM BGC', ['surfex', 'trip']),
        'AESMHR': ('CNRM-ESM2-1-HR', 'AGCM BGC AER', []),
        'AGCMHRAER': ('CNRM-CM6-1-HR', 'AGCM AER', ['nemo']),
        'AOGCM': ('CNRM-CM6-1', 'AOGCM', []),
        'LGCM': ('CNRM-CM6-1', 'LAND', ['nemo']),
        'AOESM': ('CNRM-ESM2-1', 'AOGCM BGC AER CHEM', []),
        'ARCM': ('CNRM-ALADIN64', 'ARCM AER', ['nemo']),
        'OGCM': ('CNRM-CM6-1', 'OGCM', ['surfex', 'trip'])
    },
    'grids': {
        'HR': {'nemo': ['gn', '', '', '25 km', 'native ocean tri-polar grid with 1.47 M ocean cells'],
               'surfex': ['gr', 'complete', 'glat', '50 km', 'data regridded to a 359 gaussian grid (360x720 latlon)'
                                                             ' from a native atmosphere T359l reduced gaussian grid'],
               'trip': ['gn', '', '', '50 km', 'regular 1/2 deg lat-lon grid']
               },
        'LR': {
            'nemo': ['gn', '', '', '100 km', 'native ocean tri-polar grid with 105 k ocean cells'],
            'surfex': ['gr', 'complete', 'glat', '250 km', 'data regridded to a T127 gaussian grid (128x256 latlon) '
                                                           'from a native atmosphere T127l reduced gaussian grid'],
            'trip': ['gn', '', '', '50 km', 'regular 1/2 deg lat-lon grid']
        },
        'REG': {
            'nemo': ['gn', '', '', '8 km', 'native ocean tri-polar grid'],
            'surfex': ['gn', 'C', 'glat', '50 km', 'regional zone C '],
            'trip': ['gn', '', '', '50 km', 'regular 1/2 deg lat-lon grid']
        }
    },
    'dr2xml_manages_enddate': True,
    'excluded_vars': ['pfull', 'phalf', 'n2oClim', 'ch4globalClim', 'co2massClim', 'n2oglobalClim', 'ch4Clim', 'o3Clim',
                      'co2Clim'
                      ],
    'too_long_periods': ['dec', 'yr'],
    'ping_variables_prefix': 'CMIP6_',
    'debug_parsing': True,
    'comments': {
        'htovovrt': j_mean_comment,
        'tpf': 'Region where always 0m correspond to none-permafrost areas',
        'sivols': sectors_comment_south,
        'snc': 'ISBA snow cover over bare ground comparable with stallite data (Psng in equation C1 in Decharme et al. 2016)',
        'siextentn': sectors_comment_north,
        'rivi': 'CTRIP river grid-cell inflow considering upstream grdi-cell water fluxes and total runoff input (mrro) from ISBA',
        'snovols': sectors_comment_south,
        'snovoln': sectors_comment_north,
        'hfbasinpmad': j_mean_comment,
        'dgw': 'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr',
        'dcw': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'siextents': sectors_comment_south,
        'sivoln': sectors_comment_north,
        'zomsf_3bsn': j_mean_comment,
        'hfbasin': j_mean_comment,
        'sltbasin': j_mean_comment,
        'dslw': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dtes': 'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        'htovgyre  ': j_mean_comment,
        'fldcapacity': '100 * ISBA Field Capacity in m3/m3',
        'sltovovrt': j_mean_comment,
        'dsw': 'Change in floodplains water ; ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'sw': 'Surface floodplains water storage (e.g. Decharme et al. 2018)',
        'siareas': sectors_comment_south,
        'siarean': sectors_comment_north, 'wilt': '100 * ISBA Wilting Point in m3/m3',
        'eow': 'Liquid water evaporation from floodplains (e.g. Decharme et al. 2018)',
        'prsnsn': 'In ISBA, prsnsn is always 1 because all snowfall falls onto snowpack',
        'dtesn': 'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        'sltnortha': j_mean_comment,
        'mrtws': 'ISBA-CTRIP total water storage (soil+canopy+snow+rivers+groundwater+floodplains; e.g. Decharme et al. 2018)',
        'sltovgyre': j_mean_comment,
        'dsn': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dmlt': 'Region where always 12m correspond to none-permafrost areas',
        'drivw': 'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr'
    },
    'included_tables': ['Amon'],
    'max_file_size_in_floats': 4000000000.0,
    'non_standard_attributes': {
        'xios_commit': '1442-shuffle',
        'nemo_gelato_commit': '49095b3accd5d4c_6524fe19b00467a',
        'arpege_minor_version': '6.4.1'
    },
    'special_timestep_vars': {
        '60mi': ['cllcalipso', 'clmcalipso', 'clhcalipso', 'cltcalipso', 'cllcalipsoice', 'clmcalipsoice',
                 'clhcalipsoice', 'cltcalipsoice', 'cllcalipsoliq', 'clmcalipsoliq', 'clhcalipsoliq', 'cltcalipsoliq',
                 'cllcalipsoun', 'clmcalipsoun', 'clhcalipsoun', 'cltcalipsoun', 'clcalipso', 'clcalipsoice',
                 'clcalipsoliq', 'clcalipsoun', 'clcalipsotmp', 'clcalipsotmpice', 'clcalipsotmpliq', 'clcalipsotmpun',
                 'cfadLidarsr532', 'parasolRefl', 'parasolCRefl', 'cltlidarradar', 'clcalipso2', 'cfadDbze94',
                 'cltisccp', 'pctisccp', 'tauisccp', 'albisccp', 'meantbisccp', 'meantbclrisccp', 'clisccp', 'cltmodis',
                 'clwmodis', 'climodis', 'clhmodis', 'clmmodis', 'cllmodis', 'tautmodis', 'tauwmodis', 'tauimodis',
                 'reffclwmodis', 'reffclimodis', 'pctmodis', 'lwpmodis', 'iwpmodis', 'clmodis', 'jpdftaureliqmodis',
                 'jpdftaureicemodis', 'clmisr']
    },
    'institution_id': 'CNRM',
    'excluded_spshapes': ['XYA-na', 'XYG-na', 'na-A'],
    'mips': {
        'HR': {'ScenarioMIP', 'CMIP', 'CMIP6', 'OMIP'},
        'LR': {'C4MIP', 'DCPP', 'CORDEX', 'ISMIP6', 'GMMIP', 'RFMIP', 'LUMIP', 'CFMIP', 'FAFMIP', 'DAMIP', 'AerChemMIP',
               'SIMIP', 'CMIP', 'PMIP', 'CMIP6', 'ScenarioMIP', 'LS3MIP', 'OMIP', 'GeoMIP', 'HighResMIP'},
        'REG': {'CORDEX'}
    },
    'non_standard_axes': {
        'siline': 'siline',
        'dbze': 'dbze',
        'klev': 'alevel',
        'soil_carbon_pools': ('soilpools', 'fast medium slow'),
        'effectRadL': 'effectRadL',
        'vegtype': ('vegtype', 'Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen '
                               'Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass '
                               'Wetland Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen '
                               'Temperate_needleaf_evergreen Boreal_broad-leaved_decidus Boreal_needleaf_decidus '
                               'Tundra_grass Shrub'),
        'sza5': 'sza5',
        'effectRadIc': 'effectRadIc',
        'oline': 'oline',
        'basin': ('basin', 'global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
        'klev_half': 'alevel'
    },
    'branching': {
        'CNRM-ESM2-1': {'historical': (1850, [1850, 1883, 1941])},
        'CNRM-CM6-1': {'historical': (1850, [1850, 1883, 1941, 1960, 1990, 2045, 2079, 2108, 2214, 2269])},
        'CNRM-CM6-1-HR': {'historical': (1850, [1850, 1883, 1941])}
    },
    'excluded_vars_per_config': {
        'LESM': ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt', 'ccb', 'cct', 'ci',
                 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                 'rldscs', 'rlut', 'rlutcs', 'rsdscs', 'rsdt', 'rsuscs', 'rsut', 'rsutcs', 'ch4global', 'co2mass',
                 'n2oglobal', 'mc', 'cl', 'cli', 'clw'],
        'LGCM': ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt', 'ccb', 'cct', 'ci',
                 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                 'rldscs', 'rlut', 'rlutcs', 'rsdscs', 'rsdt', 'rsuscs', 'rsut', 'rsutcs', 'ch4global', 'co2mass',
                 'n2oglobal', 'mc', 'cl', 'cli', 'clw'],
        'AGCMHRAER': ['ch4', 'co2', 'co', 'h2o', 'hcho', 'hcl', 'hno3', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss',
                      'o3prod', 'oh', 'fco2antt', 'fco2fos', 'fco2nat', 'oxloss', 'oxprod', 'vmrox', 'bry', 'cly',
                      'ho2', 'meanage', 'noy', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat',
                      'fLuc', 'fProductDecomp', 'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct',
                      'cVeg', 'fFire', 'fLitterSoil', 'fVegLitter', 'nbp', 'shrubFrac'],
        'AGCM': ['ch4', 'co2', 'co', 'concdust', 'ec550aer', 'h2o', 'hcho', 'hcl', 'hno3', 'mmrbc', 'mmrdust', 'mmroa',
                 'mmrso4', 'mmrss', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod', 'oh', 'so2', 'mmrpm1', 'fco2antt',
                 'fco2fos', 'fco2nat', 'loadbc', 'loaddust', 'loadoa', 'loadso4', 'loadss', 'oxloss', 'oxprod', 'vmrox',
                 'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust', 'dryoa', 'dryso2', 'dryso4', 'dryss',
                 'emibc', 'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'od440aer', 'od870aer', 'od550lt1aer',
                 'wetbc', 'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct',
                 'fFireNat', 'fLuc', 'fProductDecomp', 'netAtmosLandCO2Flux', 'od443dust', 'od865dust', 'sconcdust',
                 'sconcso4', 'sconcss', 'sedustCI', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire',
                 'fLitterSoil', 'fVegLitter', 'nbp', 'shrubFrac'],
        'AOGCM': ['ch4', 'co2', 'co', 'concdust', 'ec550aer', 'h2o', 'hcho', 'hcl', 'hno3', 'mmrbc', 'mmrdust', 'mmroa',
                  'mmrso4', 'mmrss', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod', 'oh', 'so2', 'mmrpm1',
                  'fco2antt', 'fco2fos', 'fco2nat', 'loadbc', 'loaddust', 'loadoa', 'loadso4', 'loadss', 'oxloss',
                  'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust', 'dryoa', 'dryso2',
                  'dryso4', 'dryss', 'emibc', 'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'od440aer', 'od870aer',
                  'od550lt1aer', 'wetbc', 'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand', 'cSoil', 'fAnthDisturb',
                  'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp', 'netAtmosLandCO2Flux', 'od443dust',
                  'od865dust', 'sconcdust', 'sconcso4', 'sconcss', 'sedustCI', 'burntFractionAll', 'cLitter',
                  'cProduct', 'cVeg', 'fFire', 'fLitterSoil', 'fVegLitter', 'nbp', 'shrubFrac'],
        'AGCMAER': ['ch4', 'co2', 'co', 'h2o', 'hcho', 'hcl', 'hno3', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod',
                    'oh', 'fco2antt', 'fco2fos', 'fco2nat', 'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage',
                    'noy', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                    'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                    'fVegLitter', 'nbp', 'shrubFrac'],
        'AOESM': ['co2mass', 'ch4global', 'n2oglobal'],
        'ARCM': ['ch4', 'co2', 'co', 'h2o', 'hcho', 'hcl', 'hno3', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod',
                 'oh', 'fco2antt', 'fco2fos', 'fco2nat', 'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage',
                 'noy', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                 'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                 'fVegLitter', 'nbp', 'shrubFrac'],
        'AESM': ['co2mass', 'ch4global', 'n2oglobal'],
        'AORCM': ['ch4', 'co2', 'co', 'h2o', 'hcho', 'hcl', 'hno3', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod',
                  'oh', 'fco2antt', 'fco2fos', 'fco2nat', 'oxloss', 'oxprod', 'vmrox', 'bry', 'cly', 'ho2', 'meanage',
                  'noy', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct', 'fFireNat', 'fLuc', 'fProductDecomp',
                  'netAtmosLandCO2Flux', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                  'fVegLitter', 'nbp', 'shrubFrac']
    },
    'allow_tos_3hr_1deg': True,
    'contact': 'contact.aladin-cordex@meteo.fr',
    'compression_level': 0,
    'grid_policy': 'adhoc',
    'bytes_per_float': 2.4,
    'project': "CORDEX"
}
