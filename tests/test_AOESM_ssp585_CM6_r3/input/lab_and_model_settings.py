#!/usr/bin/python
# -*- coding: utf-8 -*-


lab_and_model_settings = {
    'path_to_parse': '{path_xml}/',
    'comment': '',
    'tierMax': 1,
    'references': 'http://www.umr-cnrm.fr/cmip6/references',
    'excluded_tables': ['Eyr', 'Oyr', 'Odec', 'IfxAnt', 'ImonAnt'],
    'realms_per_context': {
        'nemo': ['seaIce', 'ocean', 'ocean seaIce', 'ocnBgChem', 'seaIce ocean'],
        'surfex': ['atmos', 'atmos atmosChem', 'atmosChem', 'aerosol', 'atmos land', 'land', 'landIce land', 'aerosol',
                   'land landIce', 'landIce'],
        'trip': []
    },
    'fx_from_file': {
        'areacella': {
            'complete': {
                'HR': 'areacella_complete_CMIP6_tl359',
                'LR': 'areacella_complete_CMIP6_tl127'
            }
        }
    },
    'grid_choice': {
        'CNRM-ESM2-1': 'LR',
        'CNRM-ESM2-1-HR': 'HR',
        'CNRM-CM6-1': 'LR',
        'CNRM-CM6-1-HR': 'HR'
    },
    'print_stats_per_var_label': True,
    'vertical_interpolation_sample_freq': '3h',
    'vertical_interpolation_operation': 'instant',
    'orphan_variables': {
        'nemo': [''],
        'surfex': ['siconca'],
        'trip': ['areacellr', 'dgw', 'drivw', 'qgwr', 'rivi', 'rivo', 'waterDpth', 'wtd', 'fwtd', 'fldf', 'carbw',
                 'carbdis', 'carbin']
    },
    'CFsubhr_frequency': '2ts',
    'excluded_request_links': ['RFMIP-AeroIrf'],
    'max_priority': 1,
    'info_url': 'http://www.umr-cnrm.fr/cmip6/',
    'use_cmorvar_label_in_filename': False,
    'allow_duplicates_in_same_table': False,
    'allow_pseudo_standard_names': True,
    'sampling_timestep': {
        'HR': {
            'nemo': 1800.0,
            'surfex': 900.0,
            'trip': 1800.0
        },
        'LR': {
            'nemo': 1800.0,
            'surfex': 900.0,
            'trip': 1800.0
        }
    },
    'sizes': {
        'HR': [1514100, 75, 259200, 91, 30, 14, 128],
        'LR': [106428, 75, 32768, 91, 30, 14, 128]
    },
    'source_types': {
        'CNRM-ESM2-1': 'AOGCM BGC AER CHEM',
        'CNRM-ESM2-1-HR': 'AOGCM BGC AER',
        'CNRM-CM6-1': 'AOGCM',
        'CNRM-CM6-1-HR': 'AOGCM'
    },
    'configurations': {
        'AOESMHR': ('CNRM-ESM2-1-HR', 'AOGCM BGC AER', []),
        'AESM': ('CNRM-ESM2-1', 'AGCM BGC AER CHEM', ['nemo']),
        'OESMHR': ('CNRM-ESM2-1-HR', 'OGCM BGC', ['surfex', 'trip']),
        'AOESM': ('CNRM-ESM2-1', 'AOGCM BGC AER CHEM', []),
        'LESM': ('CNRM-ESM2-1', 'LAND BGC', ['nemo']),
        'AGCM': ('CNRM-CM6-1', 'AGCM', ['nemo']),
        'OGCMHR': ('CNRM-CM6-1-HR', 'OGCM', ['surfex', 'trip']),
        'AOGCMHR': ('CNRM-CM6-1-HR', 'AOGCM', []),
        'AGCMHR': ('CNRM-CM6-1-HR', 'AGCM', ['nemo']),
        'OESM': ('CNRM-ESM2-1', 'OGCM BGC', ['surfex', 'trip']),
        'AESMHR': ('CNRM-ESM2-1-HR', 'AGCM BGC AER', []),
        'AOGCM': ('CNRM-CM6-1', 'AOGCM', []),
        'LGCM': ('CNRM-CM6-1', 'LAND', ['nemo']),
        'OGCM': ('CNRM-CM6-1', 'OGCM', ['surfex', 'trip'])
    },
    'grids': {
        'HR': {
            'nemo': ['gn', '', '', '25 km', 'native ocean tri-polar grid with 1.47 M ocean cells'],
            'surfex': ['gr', 'complete', 'glat', '50 km', 'data regridded to a 359 gaussian grid (360x720 latlon) from a native atmosphere T359l reduced gaussian grid'],
            'trip': ['gn', '', '', '50 km', 'regular 1/2 deg lat-lon grid']
        },
        'LR': {
            'nemo': ['gn', '', '', '100 km', 'native ocean tri-polar grid with 105 k ocean cells'],
            'surfex': ['gr', 'complete', 'glat', '250 km', 'data regridded to a T127 gaussian grid (128x256 latlon) from a native atmosphere T127l reduced gaussian grid'],
            'trip': ['gn', '', '', '50 km', 'regular 1/2 deg lat-lon grid']
        }
    },
    'excluded_pairs': [('sfdsi', 'SImon')],
    'dr2xml_manages_enddate': True,
    'excluded_vars': ['pfull', 'phalf', 'n2oClim', 'ch4globalClim', 'co2massClim', 'n2oglobalClim', 'ch4Clim', 'o3Clim',
                      'co2Clim'],
    'too_long_periods': ['dec', 'yr'],
    'ping_variables_prefix': 'CMIP6_',
    'debug_parsing': False,
    'comments': {
        'htovovrt': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'tpf': 'Region where always 0m correspond to none-permafrost areas',
        'sivols': 'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'snc': 'ISBA snow cover over bare ground comparable with stallite data (Psng in equation C1 in Decharme et al. 2016)',
        'siextentn': 'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'rivi': 'CTRIP river grid-cell inflow considering upstream grdi-cell water fluxes and total runoff input (mrro) from ISBA',
        'snovols': 'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'snovoln': 'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'hfbasinpmad': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'dgw': 'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr',
        'dcw': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'siextents': 'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'sivoln': 'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'zomsf_3bsn': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'hfbasin': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'sltbasin': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'dslw': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dtes': 'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        'htovgyre  ': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'fldcapacity': '100 * ISBA Field Capacity in m3/m3',
        'sltovovrt': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'dsw': 'Change in floodplains water ; ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'sw': 'Surface floodplains water storage (e.g. Decharme et al. 2018)',
        'siareas': 'The sector attribute is erroneous, this variable is indeed integrated over the southern hemisphere.',
        'siarean': 'The sector attribute is erroneous, this variable is indeed integrated over the northern hemisphere.',
        'wilt': '100 * ISBA Wilting Point in m3/m3',
        'eow': 'Liquid water evaporation from floodplains (e.g. Decharme et al. 2018)',
        'prsnsn': 'In ISBA, prsnsn is always 1 because all snowfall falls onto snowpack',
        'dtesn': 'ISBA land energy budget = (dtes+dtesn)/dt + hfmlt - hfdsl ; dt is given by netcdf attribute : interval_operation',
        'sltnortha': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'mrtws': 'ISBA-CTRIP total water storage (soil+canopy+snow+rivers+groundwater+floodplains; e.g. Decharme et al. 2018)',
        'sltovgyre': 'This variable has an axis labelled j-mean, while CMIP6 calls for an axis labelled latitude. We want here to pinpoint that we provide values which are averaged over the X-axis of our tripolar grid, along which latitude do vary. This axis begins South.Please refer to the lat/lon coordinate variables in this file for further details.',
        'dsn': 'ISBA land water budget = (dslw+dcw+dsn+dsw)/dt - (pr-et-mrro) ; dt is given by netcdf attribute : interval_operation',
        'dmlt': 'Region where always 12m correspond to none-permafrost areas',
        'drivw': 'CTRIP river water budget = (drivw+dgw)/dt - (rivi-rivo)*1000/areacellr - qgwr'
    },
    'max_file_size_in_floats': 4000000000.0,
    'non_standard_attributes': {
        'xios_commit': '1442-shuffle',
        'nemo_gelato_commit': '49095b3accd5d4c_6524fe19b00467a',
        'arpege_minor_version': '6.3.2'
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
    'institution_id': 'CNRM-CERFACS',
    'excluded_spshapes': ['XYA-na', 'XYG-na', 'na-A'],
    'mips': {
        'HR': set(['OMIP', 'CMIP', 'CMIP6', 'ScenarioMIP']),
        'LR': set(['C4MIP', 'DCPP', 'CORDEX', 'ISMIP6', 'GMMIP', 'RFMIP', 'LUMIP', 'OMIP', 'CMIP6', 'SIMIP', 'DAMIP',
                   'AerChemMIP', 'FAFMIP', 'PMIP', 'CFMIP', 'ScenarioMIP', 'LS3MIP', 'CMIP', 'GeoMIP', 'HighResMIP'])
    },
    'non_standard_axes': {
        'siline': 'siline',
        'dbze': 'dbze',
        'klev': 'alevel',
        'soil_carbon_pools': ('soilpools', 'fast medium slow'),
        'effectRadL': 'effectRadL',
        'vegtype': ('vegtype', 'Bare_soil Rock Permanent_snow Temperate_broad-leaved_decidus Boreal_needleaf_evergreen Tropical_broad-leaved_evergreen C3_crop C4_crop Irrigated_crop C3_grass C4_grass Wetland Tropical_broad-leaved_decidus Temperate_broad-leaved_evergreen Temperate_needleaf_evergreen Boreal_broad-leaved_decidus Boreal_needleaf_decidus Tundra_grass Shrub'),
        'sza5': 'sza5',
        'effectRadIc': 'effectRadIc',
        'oline': 'oline',
        'basin': ('basin', 'global_ocean atlantic_arctic_ocean indian_pacific_ocean dummy dummy'),
        'klev_half': 'alevel'
    },
    'branching': {
        'CNRM-ESM2-1': {
            'historical': (1850, [1850, 1883, 1941])
        },
        'CNRM-CM6-1': {
            'historical': (1850, [1850, 1883, 1941, 1960, 1990, 2045, 2079, 2108, 2214, 2269])
        },
        'CNRM-CM6-1-HR': {
            'historical': (1850, [1850, 1883, 1941])
        }
    },
    'excluded_vars_per_config': {
        'AGCM': ['ch4', 'co2', 'co', 'concdust', 'ec550aer', 'h2o', 'hcho', 'hcl', 'hno3', 'mmrbc', 'mmrdust', 'mmroa',
                 'mmrso4', 'mmrss', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod', 'oh', 'so2', 'mmrpm1', 'fco2antt',
                 'fco2fos', 'fco2nat', 'loadbc', 'loaddust', 'loadoa', 'loadso4', 'loadss', 'oxloss', 'oxprod', 'vmrox',
                 'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust', 'dryoa', 'dryso2', 'dryso4', 'dryss',
                 'emibc',
                 'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'od440aer', 'od870aer', 'od550lt1aer', 'wetbc',
                 'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct',
                 'fFireNat',
                 'fLuc', 'fProductDecomp', 'netAtmosLandCO2Flux', 'od443dust', 'od865dust', 'sconcdust', 'sconcso4',
                 'sconcss', 'sedustCI', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire', 'fLitterSoil',
                 'fVegLitter', 'nbp', 'shrubFrac'], 'AESM': ['co2mass', 'ch4global', 'n2oglobal'],
        'AOGCM': ['ch4', 'co2', 'co', 'concdust', 'ec550aer', 'h2o', 'hcho', 'hcl', 'hno3', 'mmrbc', 'mmrdust', 'mmroa',
                  'mmrso4', 'mmrss', 'n2o', 'no2', 'no', 'o3Clim', 'o3loss', 'o3prod', 'oh', 'so2', 'mmrpm1',
                  'fco2antt',
                  'fco2fos', 'fco2nat', 'loadbc', 'loaddust', 'loadoa', 'loadso4', 'loadss', 'oxloss', 'oxprod',
                  'vmrox',
                  'bry', 'cly', 'ho2', 'meanage', 'noy', 'drybc', 'drydust', 'dryoa', 'dryso2', 'dryso4', 'dryss',
                  'emibc',
                  'emidust', 'emioa', 'emiso2', 'emiso4', 'emiss', 'od440aer', 'od870aer', 'od550lt1aer', 'wetbc',
                  'wetdust', 'wetoa', 'wetso4', 'wetss', 'cLand', 'cSoil', 'fAnthDisturb', 'fDeforestToProduct',
                  'fFireNat', 'fLuc', 'fProductDecomp', 'netAtmosLandCO2Flux', 'od443dust', 'od865dust', 'sconcdust',
                  'sconcso4', 'sconcss', 'sedustCI', 'burntFractionAll', 'cLitter', 'cProduct', 'cVeg', 'fFire',
                  'fLitterSoil', 'fVegLitter', 'nbp', 'shrubFrac'],
        'LGCM': ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt', 'ccb', 'cct', 'ci',
                 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                 'rldscs', 'rlut', 'rlutcs', 'rsdscs', 'rsdt', 'rsuscs', 'rsut', 'rsutcs', 'ch4global', 'co2mass',
                 'n2oglobal', 'mc', 'cl', 'cli', 'clw'], 'AOESM': ['co2mass', 'ch4global', 'n2oglobal'],
        'LESM': ['ch4', 'co2', 'hur', 'hus', 'n2o', 'o3', 'ta', 'ua', 'va', 'wap', 'zg', 'clt', 'ccb', 'cct', 'ci',
                 'clivi', 'clt', 'clwvi', 'evspsbl', 'fco2antt', 'fco2fos', 'pr', 'prc', 'prsn', 'prw', 'ps', 'psl',
                 'rldscs', 'rlut', 'rlutcs', 'rsdscs', 'rsdt', 'rsuscs', 'rsut', 'rsutcs', 'ch4global', 'co2mass',
                 'n2oglobal', 'mc', 'cl', 'cli', 'clw']
    },
    'allow_tos_3hr_1deg': True,
    'contact': 'contact.cmip@meteo.fr',
    'compression_level': 4,
    'grid_policy': 'adhoc',
    'bytes_per_float': 2.4
}
