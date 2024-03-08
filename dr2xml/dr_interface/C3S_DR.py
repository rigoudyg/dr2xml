#####################################################################################
# Dimensions used in C3S-0.1
c3s_nc_dims = {}

c3s_nc_dims['leadtime'] = None
c3s_nc_dims['lat'] = 180
c3s_nc_dims['lon'] = 360
c3s_nc_dims['plev'] = 11
c3s_nc_dims['depth'] = 4 # values for ECMWFsys4
c3s_nc_dims['str31'] = 31
c3s_nc_dims['bnds'] = 2

#####################################################################################
# Coordinate variables used in C3S-0.1

c3s_nc_coords = {}

# Coordinates
c3s_nc_coords['lat'] = {'dimensions': ("lat",), 'attributes':{}, 'values': [v+0.5 for v in range(-90,90)] }
c3s_nc_coords['lat']['attributes']['axis'] = "Y"
c3s_nc_coords['lat']['attributes']['standard_name'] = "latitude"
c3s_nc_coords['lat']['attributes']['long_name'] = "latitude"
c3s_nc_coords['lat']['attributes']['units'] = "degrees_north"
c3s_nc_coords['lat']['attributes']['valid_min'] = -90.
c3s_nc_coords['lat']['attributes']['valid_max'] = 90.
c3s_nc_coords['lat']['attributes']['bounds'] = "lat_bnds"  
c3s_nc_coords['lat']['boundvalues'] = [(ll,ll+1) for ll in range(-90,90)]

c3s_nc_coords['lon'] = {'dimensions': ("lon",), 'attributes':{}, 'values': [v+0.5 for v in range(0,360)] }
c3s_nc_coords['lon']['attributes']['axis'] = "X"
c3s_nc_coords['lon']['attributes']['standard_name'] = "longitude"
c3s_nc_coords['lon']['attributes']['long_name'] = "longitude"
c3s_nc_coords['lon']['attributes']['units'] = "degrees_east"
c3s_nc_coords['lon']['attributes']['valid_min'] = 0.
c3s_nc_coords['lon']['attributes']['valid_max'] = 360.
c3s_nc_coords['lon']['attributes']['bounds'] = "lon_bnds"
c3s_nc_coords['lon']['boundvalues'] = [(ll,ll+1) for ll in range(0,360)] 

c3s_nc_coords['plev'] = {'dimensions': ("plev",), 'attributes':{}, 'values': [92500., 85000., 70000., 50000., 40000., 30000., 20000., 10000., 5000., 3000., 1000.] }
c3s_nc_coords['plev']['attributes']['axis'] = "Z"
c3s_nc_coords['plev']['attributes']['standard_name'] = "air_pressure"
c3s_nc_coords['plev']['attributes']['long_name'] = "pressure"
c3s_nc_coords['plev']['attributes']['units'] = "Pa"
c3s_nc_coords['plev']['attributes']['positive'] = "down"

c3s_nc_coords['depth'] = {'dimensions': ("depth",), 'attributes':{}, 'values': [0.035,0.175,0.64,1.945] } #values for ECMWFsys4
c3s_nc_coords['depth']['attributes']['axis'] = "Z"
c3s_nc_coords['depth']['attributes']['standard_name'] = "depth"
c3s_nc_coords['depth']['attributes']['long_name'] = "depth"
c3s_nc_coords['depth']['attributes']['units'] = "m"
c3s_nc_coords['depth']['attributes']['positive'] = "down"
c3s_nc_coords['depth']['attributes']['bounds'] = "depth_bnds"
c3s_nc_coords['depth']['boundvalues'] = [(0,0.07), (0.07,0.28), (0.28,1.00), (1.00,2.89) ] # values for ECMWFsys4

c3s_nc_coords['leadtime'] = {'dimensions': ("leadtime",), 'attributes':{}, 'values': [] }
c3s_nc_coords['leadtime']['attributes']['standard_name'] = "forecast_period"
c3s_nc_coords['leadtime']['attributes']['long_name'] = "Time elapsed since the start of the forecast"
c3s_nc_coords['leadtime']['attributes']['units'] = "hours"
c3s_nc_coords['leadtime']['attributes']['bounds'] = "leadtime_bnds"

# Auxiliary coordinates
c3s_nc_coords['realization'] = {'dimensions': ("str31",), 'dtype':'S1','attributes':{}, 'values': "rXXiYYpZZ" }
c3s_nc_coords['realization']['attributes']['axis'] = "E"
c3s_nc_coords['realization']['attributes']['standard_name'] = "realization"
c3s_nc_coords['realization']['attributes']['long_name'] = "realization"
c3s_nc_coords['realization']['attributes']['units'] = "1"

c3s_nc_coords['height'] = {'dimensions': (), 'attributes':{}, 'values': None }
c3s_nc_coords['height']['attributes']['axis'] = "Z"
c3s_nc_coords['height']['attributes']['standard_name'] = "height"
c3s_nc_coords['height']['attributes']['long_name'] = "height"
c3s_nc_coords['height']['attributes']['units'] = "m"
c3s_nc_coords['height']['attributes']['positive'] = ""
c3s_nc_coords['height']['attributes']['valid_min'] = ""
c3s_nc_coords['height']['attributes']['valid_max'] = ""

c3s_nc_coords['reftime'] = {'dimensions': (), 'attributes':{}, 'values': [] }
c3s_nc_coords['reftime']['attributes']['standard_name'] = "forecast_reference_time"
c3s_nc_coords['reftime']['attributes']['long_name'] = "Start date of the forecast"
c3s_nc_coords['reftime']['attributes']['units'] = "hours since YYYY-MM-DDTh:mm:ssZ"
c3s_nc_coords['reftime']['attributes']['calendar'] = "gregorian"

c3s_nc_coords['time'] = {'dimensions': ("leadtime",), 'attributes':{}, 'values': [] }
c3s_nc_coords['time']['attributes']['standard_name'] = "time"
c3s_nc_coords['time']['attributes']['long_name'] = "Verification time of the forecast"
c3s_nc_coords['time']['attributes']['units'] = "hours since YYYY-MM-DDTh:mm:ssZ"
c3s_nc_coords['time']['attributes']['calendar'] = "gregorian"
c3s_nc_coords['time']['attributes']['bounds'] = "time_bnds"


#####################################################################################
# Common variables in C3S-0.1
c3s_nc_comvars = {}

c3s_nc_comvars['hcrs'] = {'dtype':"S1", 'dimensions': (), 'attributes':{'grid_mapping_name':'latitude_longitude'}, 'values':""}



#####################################################################################
# Variable details in C3S-0.1

#Surface Variables
c3s_nc_vars = {}

#...Static Variables (TODO: need a workaround with reftime/leadtime dimensions inclusion)
# c3s_nc_vars['sftlf'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}}
# c3s_nc_vars['sftlf']['dimensions'] = ('lat','lon')
# c3s_nc_vars['sftlf']['globattrs']['frequency'] = "fix"
# c3s_nc_vars['sftlf']['globattrs']['modeling_realm'] = "atmos"
# c3s_nc_vars['sftlf']['globattrs']['level_type'] = "surface"
# c3s_nc_vars['sftlf']['attributes']['standard_name'] = "land_area_fraction"
# c3s_nc_vars['sftlf']['attributes']['long_name'] = "Land_Area_Fraction"
# c3s_nc_vars['sftlf']['attributes']['units'] = "1"
# c3s_nc_vars['sftlf']['attributes']['coordinates'] = "lat lon"
# c3s_nc_vars['sftlf']['attributes']['grid_mapping'] = "hcrs"

# c3s_nc_vars['orog'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}}
# c3s_nc_vars['orog']['dimensions'] = ('lat','lon')
# c3s_nc_vars['orog']['globattrs']['frequency'] = "fix"
# c3s_nc_vars['orog']['globattrs']['modeling_realm'] = "atmos"
# c3s_nc_vars['orog']['globattrs']['level_type'] = "surface"
# c3s_nc_vars['orog']['attributes']['standard_name'] = "surface_altitude"
# c3s_nc_vars['orog']['attributes']['long_name'] = "Surface Altitude"
# c3s_nc_vars['orog']['attributes']['units'] = "m"
# c3s_nc_vars['orog']['attributes']['coordinates'] = "lat lon"
# c3s_nc_vars['orog']['attributes']['grid_mapping'] = "hcrs"


#...Time evolving variables
c3s_nc_vars['tas'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tas']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tas']['auxcoords'] = ('height',)
c3s_nc_vars['tas']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['tas']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tas']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tas']['attributes']['standard_name'] = "air_temperature"
c3s_nc_vars['tas']['attributes']['long_name'] = "Near-Surface Air Temperature"
c3s_nc_vars['tas']['attributes']['units'] = "K"
c3s_nc_vars['tas']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['tas']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['tas']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['tas']['modify']['height'] = {'values':2., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':10.} }

c3s_nc_vars['tasmax'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tasmax']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tasmax']['auxcoords'] = ('height',)
c3s_nc_vars['tasmax']['globattrs']['frequency'] = "day"
c3s_nc_vars['tasmax']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tasmax']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tasmax']['attributes']['standard_name'] = "air_temperature"
c3s_nc_vars['tasmax']['attributes']['long_name'] = "Daily Maximum Near-Surface Air Temperature"
c3s_nc_vars['tasmax']['attributes']['units'] = "K"
c3s_nc_vars['tasmax']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['tasmax']['attributes']['cell_methods'] = "leadtime: maximum"
c3s_nc_vars['tasmax']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['tasmax']['modify']['height'] = {'values':2., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':10.} }

c3s_nc_vars['tasmin'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tasmin']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tasmin']['auxcoords'] = ('height',)
c3s_nc_vars['tasmin']['globattrs']['frequency'] = "day"
c3s_nc_vars['tasmin']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tasmin']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tasmin']['attributes']['standard_name'] = "air_temperature"
c3s_nc_vars['tasmin']['attributes']['long_name'] = "Daily Minimum Near-Surface Air Temperature"
c3s_nc_vars['tasmin']['attributes']['units'] = "K"
c3s_nc_vars['tasmin']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['tasmin']['attributes']['cell_methods'] = "leadtime: minimum"
c3s_nc_vars['tasmin']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['tasmin']['modify']['height'] = {'values':2., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':10.} }

c3s_nc_vars['tdps'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tdps']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tdps']['auxcoords'] = ('height',)
c3s_nc_vars['tdps']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['tdps']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tdps']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tdps']['attributes']['standard_name'] = "dew_point_temperature"
c3s_nc_vars['tdps']['attributes']['long_name'] = "2m Dewpoint Temperature"
c3s_nc_vars['tdps']['attributes']['units'] = "K"
c3s_nc_vars['tdps']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['tdps']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['tdps']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['tdps']['modify']['height'] = {'values':2., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':10.} }

c3s_nc_vars['uas'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['uas']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['uas']['auxcoords'] = ('height',)
c3s_nc_vars['uas']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['uas']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['uas']['globattrs']['level_type'] = "surface"
c3s_nc_vars['uas']['attributes']['standard_name'] = "x_wind"
c3s_nc_vars['uas']['attributes']['long_name'] = "Eastward Near-Surface Wind"
c3s_nc_vars['uas']['attributes']['units'] = "m s-1"
c3s_nc_vars['uas']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['uas']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['uas']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['uas']['modify']['height'] = {'values':10., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':30.} }

c3s_nc_vars['vas'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['vas']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['vas']['auxcoords'] = ('height',)
c3s_nc_vars['vas']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['vas']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['vas']['globattrs']['level_type'] = "surface"
c3s_nc_vars['vas']['attributes']['standard_name'] = "y_wind"
c3s_nc_vars['vas']['attributes']['long_name'] = "Northward Near-Surface Wind"
c3s_nc_vars['vas']['attributes']['units'] = "m s-1"
c3s_nc_vars['vas']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['vas']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['vas']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['vas']['modify']['height'] = {'values':10., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':30.} }

c3s_nc_vars['wsgmax'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['wsgmax']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['wsgmax']['auxcoords'] = ('height',)
c3s_nc_vars['wsgmax']['globattrs']['frequency'] = "day"
c3s_nc_vars['wsgmax']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['wsgmax']['globattrs']['level_type'] = "surface"
c3s_nc_vars['wsgmax']['attributes']['standard_name'] = "wind_speed_of_gust"
c3s_nc_vars['wsgmax']['attributes']['long_name'] = "Maximum Wind Speed of Gust"
c3s_nc_vars['wsgmax']['attributes']['units'] = "m s-1"
c3s_nc_vars['wsgmax']['attributes']['coordinates'] = "reftime realization time leadtime height lat lon"
c3s_nc_vars['wsgmax']['attributes']['cell_methods'] = "leadtime: maximum"
c3s_nc_vars['wsgmax']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['wsgmax']['modify']['height'] = {'values':10., 'attributes':{'positive':'up', 'valid_min':1., 'valid_max':30.} }

c3s_nc_vars['psl'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['psl']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['psl']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['psl']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['psl']['globattrs']['level_type'] = "surface"
c3s_nc_vars['psl']['attributes']['standard_name'] = "air_pressure_at_sea_level"
c3s_nc_vars['psl']['attributes']['long_name'] = "Sea Level Pressure"
c3s_nc_vars['psl']['attributes']['units'] = "Pa"
c3s_nc_vars['psl']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['psl']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['psl']['attributes']['grid_mapping'] = "hcrs"
c3s_nc_vars['psl']['attributes']['_FillValue'] = 1.0e20

c3s_nc_vars['clt'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['clt']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['clt']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['clt']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['clt']['globattrs']['level_type'] = "surface"
c3s_nc_vars['clt']['attributes']['standard_name'] = "cloud_area_fraction"
c3s_nc_vars['clt']['attributes']['long_name'] = "Total Cloud Fraction"
c3s_nc_vars['clt']['attributes']['units'] = "1"
c3s_nc_vars['clt']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['clt']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['clt']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['tsl'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tsl']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tsl']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['tsl']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['tsl']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tsl']['attributes']['standard_name'] = "soil_temperature"
c3s_nc_vars['tsl']['attributes']['long_name'] = "Temperature of Soil"
c3s_nc_vars['tsl']['attributes']['units'] = "K"
c3s_nc_vars['tsl']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['tsl']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['tsl']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['tso'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tso']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tso']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['tso']['globattrs']['modeling_realm'] = "ocean"
c3s_nc_vars['tso']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tso']['attributes']['standard_name'] = "sea_surface_temperature"
c3s_nc_vars['tso']['attributes']['long_name'] = "Sea Surface Temperature"
c3s_nc_vars['tso']['attributes']['units'] = "K"
c3s_nc_vars['tso']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['tso']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['tso']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['sitemptop'] = {'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['sitemptop']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['sitemptop']['globattrs']['frequency'] = "6hr"
c3s_nc_vars['sitemptop']['globattrs']['modeling_realm'] = "seaIce"
c3s_nc_vars['sitemptop']['globattrs']['level_type'] = "surface"
c3s_nc_vars['sitemptop']['attributes']['standard_name'] = "sea_ice_temperature"
c3s_nc_vars['sitemptop']['attributes']['long_name'] = "Surface Temperature of Sea Ice"
c3s_nc_vars['sitemptop']['attributes']['units'] = "K"
c3s_nc_vars['sitemptop']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['sitemptop']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['sitemptop']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['sic'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['sic']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['sic']['globattrs']['frequency'] = "day"
c3s_nc_vars['sic']['globattrs']['modeling_realm'] = "seaIce"
c3s_nc_vars['sic']['globattrs']['level_type'] = "surface"
c3s_nc_vars['sic']['attributes']['standard_name'] = "sea_ice_area_fraction"
c3s_nc_vars['sic']['attributes']['long_name'] = "Sea Ice Area Fraction"
c3s_nc_vars['sic']['attributes']['units'] = "1"
c3s_nc_vars['sic']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['sic']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['sic']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['mrlsl'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['mrlsl']['dimensions'] = ('leadtime','depth','lat','lon')
c3s_nc_vars['mrlsl']['globattrs']['frequency'] = "day"
c3s_nc_vars['mrlsl']['globattrs']['modeling_realm'] = "soil"
c3s_nc_vars['mrlsl']['globattrs']['level_type'] = "surface"
c3s_nc_vars['mrlsl']['attributes']['standard_name'] = "moisture_content_of_soil_water"
c3s_nc_vars['mrlsl']['attributes']['long_name'] = "Water Content per Unit Area of Soil Layers"
c3s_nc_vars['mrlsl']['attributes']['units'] = "kg m-2"
c3s_nc_vars['mrlsl']['attributes']['coordinates'] = "reftime realization time leadtime depth lat lon"
c3s_nc_vars['mrlsl']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['mrlsl']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lwesnw'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lwesnw']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lwesnw']['globattrs']['frequency'] = "day"
c3s_nc_vars['lwesnw']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['lwesnw']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lwesnw']['attributes']['standard_name'] = "lwe_thickness_of_surface_snow_amount"
c3s_nc_vars['lwesnw']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Surface Snow Amount"
c3s_nc_vars['lwesnw']['attributes']['units'] = "m"
c3s_nc_vars['lwesnw']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lwesnw']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['lwesnw']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rhosn'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rhosn']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rhosn']['globattrs']['frequency'] = "day"
c3s_nc_vars['rhosn']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['rhosn']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rhosn']['attributes']['standard_name'] = "snow_density"
c3s_nc_vars['rhosn']['attributes']['long_name'] = "Snow Density"
c3s_nc_vars['rhosn']['attributes']['units'] = "kg m-3"
c3s_nc_vars['rhosn']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rhosn']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['rhosn']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lweprs'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lweprs']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lweprs']['globattrs']['frequency'] = "day"
c3s_nc_vars['lweprs']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['lweprs']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lweprs']['attributes']['standard_name'] = "lwe_thickness_of_stratiform_precipitation_amount"
c3s_nc_vars['lweprs']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Stratiform Precipitation Amount"
c3s_nc_vars['lweprs']['attributes']['units'] = "m"
c3s_nc_vars['lweprs']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lweprs']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['lweprs']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lweprc'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lweprc']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lweprc']['globattrs']['frequency'] = "day"
c3s_nc_vars['lweprc']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['lweprc']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lweprc']['attributes']['standard_name'] = "lwe_thickness_of_convective_precipitation_amount"
c3s_nc_vars['lweprc']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Convective Precipitation Amount"
c3s_nc_vars['lweprc']['attributes']['units'] = "m"
c3s_nc_vars['lweprc']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lweprc']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['lweprc']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lwepr'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lwepr']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lwepr']['globattrs']['frequency'] = "day"
c3s_nc_vars['lwepr']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['lwepr']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lwepr']['attributes']['standard_name'] = "lwe_thickness_of_precipitation_amount"
c3s_nc_vars['lwepr']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Total Precipitation Amount"
c3s_nc_vars['lwepr']['attributes']['units'] = "m"
c3s_nc_vars['lwepr']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lwepr']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['lwepr']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lweprsn'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lweprsn']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lweprsn']['globattrs']['frequency'] = "day"
c3s_nc_vars['lweprsn']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['lweprsn']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lweprsn']['attributes']['standard_name'] = "lwe_thickness_of_snowfall_amount"
c3s_nc_vars['lweprsn']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Snowfall Amount"
c3s_nc_vars['lweprsn']['attributes']['units'] = "m"
c3s_nc_vars['lweprsn']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lweprsn']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['lweprsn']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['hfss'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['hfss']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['hfss']['globattrs']['frequency'] = "day"
c3s_nc_vars['hfss']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['hfss']['globattrs']['level_type'] = "surface"
c3s_nc_vars['hfss']['attributes']['standard_name'] = "surface_upward_sensible_heat_flux"
c3s_nc_vars['hfss']['attributes']['long_name'] = "Surface Upward Sensible Heat Flux"
c3s_nc_vars['hfss']['attributes']['units'] = "W m-2"
c3s_nc_vars['hfss']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['hfss']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['hfss']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['hfls'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['hfls']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['hfls']['globattrs']['frequency'] = "day"
c3s_nc_vars['hfls']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['hfls']['globattrs']['level_type'] = "surface"
c3s_nc_vars['hfls']['attributes']['standard_name'] = "surface_upward_latent_heat_flux"
c3s_nc_vars['hfls']['attributes']['long_name'] = "Surface Upward Latent Heat Flux"
c3s_nc_vars['hfls']['attributes']['units'] = "W m-2"
c3s_nc_vars['hfls']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['hfls']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['hfls']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rsds'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rsds']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rsds']['globattrs']['frequency'] = "day"
c3s_nc_vars['rsds']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rsds']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rsds']['attributes']['standard_name'] = "surface_downwelling_shortwave_flux_in_air"
c3s_nc_vars['rsds']['attributes']['long_name'] = "Surface Downwelling Shortwave Radiation"
c3s_nc_vars['rsds']['attributes']['units'] = "W m-2"
c3s_nc_vars['rsds']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rsds']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rsds']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rlds'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rlds']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rlds']['globattrs']['frequency'] = "day"
c3s_nc_vars['rlds']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rlds']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rlds']['attributes']['standard_name'] = "surface_downwelling_longwave_flux_in_air"
c3s_nc_vars['rlds']['attributes']['long_name'] = "Surface Downwelling Longwave Radiation"
c3s_nc_vars['rlds']['attributes']['units'] = "W m-2"
c3s_nc_vars['rlds']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rlds']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rlds']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rss'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rss']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rss']['globattrs']['frequency'] = "day"
c3s_nc_vars['rss']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rss']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rss']['attributes']['standard_name'] = "surface_net_downward_shortwave_flux"
c3s_nc_vars['rss']['attributes']['long_name'] = "Net Shortwave Surface Radiation"
c3s_nc_vars['rss']['attributes']['units'] = "W m-2"
c3s_nc_vars['rss']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rss']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rss']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rls'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rls']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rls']['globattrs']['frequency'] = "day"
c3s_nc_vars['rls']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rls']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rls']['attributes']['standard_name'] = "surface_net_downward_longwave_flux"
c3s_nc_vars['rls']['attributes']['long_name'] = "Net Longwave Surface Radiation"
c3s_nc_vars['rls']['attributes']['units'] = "W m-2"
c3s_nc_vars['rls']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rls']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rls']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rst'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rst']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rst']['globattrs']['frequency'] = "day"
c3s_nc_vars['rst']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rst']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rst']['attributes']['standard_name'] = "toa_net_downward_shortwave_flux"
c3s_nc_vars['rst']['attributes']['long_name'] = "TOA Net Shortwave Radiation"
c3s_nc_vars['rst']['attributes']['units'] = "W m-2"
c3s_nc_vars['rst']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rst']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rst']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rlt'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rlt']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rlt']['globattrs']['frequency'] = "day"
c3s_nc_vars['rlt']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rlt']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rlt']['attributes']['standard_name'] = "toa_net_downward_longwave_flux"
c3s_nc_vars['rlt']['attributes']['long_name'] = "TOA Net Longwave Radiation"
c3s_nc_vars['rlt']['attributes']['units'] = "W m-2"
c3s_nc_vars['rlt']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rlt']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['rlt']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['rsdt'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['rsdt']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['rsdt']['globattrs']['frequency'] = "day"
c3s_nc_vars['rsdt']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['rsdt']['globattrs']['level_type'] = "surface"
c3s_nc_vars['rsdt']['attributes']['standard_name'] = "toa_incoming_shortwave_flux"
c3s_nc_vars['rsdt']['attributes']['long_name'] = "TOA Incident Shortwave Radiation"
c3s_nc_vars['rsdt']['attributes']['units'] = "W m-2"
c3s_nc_vars['rsdt']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['rsdt']['attributes']['cell_methods'] = "leadtime: mean (interval 0.75 hour)"
c3s_nc_vars['rsdt']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['tauu'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tauu']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tauu']['globattrs']['frequency'] = "day"
c3s_nc_vars['tauu']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tauu']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tauu']['attributes']['standard_name'] = "surface_downward_eastward_stress"
c3s_nc_vars['tauu']['attributes']['long_name'] = "Surface Downward Eastward Wind Stress"
c3s_nc_vars['tauu']['attributes']['units'] = "Pa"
c3s_nc_vars['tauu']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['tauu']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['tauu']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['tauv'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['tauv']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['tauv']['globattrs']['frequency'] = "day"
c3s_nc_vars['tauv']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['tauv']['globattrs']['level_type'] = "surface"
c3s_nc_vars['tauv']['attributes']['standard_name'] = "surface_downward_northward_stress"
c3s_nc_vars['tauv']['attributes']['long_name'] = "Surface Downward Northward Wind Stress"
c3s_nc_vars['tauv']['attributes']['units'] = "Pa"
c3s_nc_vars['tauv']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['tauv']['attributes']['cell_methods'] = "leadtime: mean (interval: 7.50 minutes)"
c3s_nc_vars['tauv']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['lwee'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['lwee']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['lwee']['globattrs']['frequency'] = "day"
c3s_nc_vars['lwee']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['lwee']['globattrs']['level_type'] = "surface"
c3s_nc_vars['lwee']['attributes']['standard_name'] = "lwe_thickness_of_water_evaporation_amount"
c3s_nc_vars['lwee']['attributes']['long_name'] = "Liquid Water Equivalent Thickness of Evaporation Amount"
c3s_nc_vars['lwee']['attributes']['units'] = "m"
c3s_nc_vars['lwee']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['lwee']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['lwee']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['mrroa'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['mrroa']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['mrroa']['globattrs']['frequency'] = "day"
c3s_nc_vars['mrroa']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['mrroa']['globattrs']['level_type'] = "surface"
c3s_nc_vars['mrroa']['attributes']['standard_name'] = "runoff_amount"
c3s_nc_vars['mrroa']['attributes']['long_name'] = "Total Run-off Amount"
c3s_nc_vars['mrroa']['attributes']['units'] = "kg m-2"
c3s_nc_vars['mrroa']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['mrroa']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['mrroa']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['mrroas'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['mrroas']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['mrroas']['globattrs']['frequency'] = "day"
c3s_nc_vars['mrroas']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['mrroas']['globattrs']['level_type'] = "surface"
c3s_nc_vars['mrroas']['attributes']['standard_name'] = "surface_runoff_amount"
c3s_nc_vars['mrroas']['attributes']['long_name'] = "Surface Run-off Amount"
c3s_nc_vars['mrroas']['attributes']['units'] = "kg m-2"
c3s_nc_vars['mrroas']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['mrroas']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['mrroas']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['mrroab'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['mrroab']['dimensions'] = ('leadtime','lat','lon')
c3s_nc_vars['mrroab']['globattrs']['frequency'] = "day"
c3s_nc_vars['mrroab']['globattrs']['modeling_realm'] = "land"
c3s_nc_vars['mrroab']['globattrs']['level_type'] = "surface"
c3s_nc_vars['mrroab']['attributes']['standard_name'] = "subsurface_runoff_amount"
c3s_nc_vars['mrroab']['attributes']['long_name'] = "Subsurface Run-off Amount"
c3s_nc_vars['mrroab']['attributes']['units'] = "kg m-2"
c3s_nc_vars['mrroab']['attributes']['coordinates'] = "reftime realization time leadtime lat lon"
c3s_nc_vars['mrroab']['attributes']['cell_methods'] = "leadtime: sum"
c3s_nc_vars['mrroab']['attributes']['grid_mapping'] = "hcrs"

#Pressure Level Variables
c3s_nc_vars['zg'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['zg']['dimensions'] = ('leadtime','plev','lat','lon')
c3s_nc_vars['zg']['globattrs']['frequency'] = "12hr"
c3s_nc_vars['zg']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['zg']['globattrs']['level_type'] = "pressure"
c3s_nc_vars['zg']['attributes']['standard_name'] = "geopotential_height"
c3s_nc_vars['zg']['attributes']['long_name'] = "Geopotential Height"
c3s_nc_vars['zg']['attributes']['units'] = "m"
c3s_nc_vars['zg']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
c3s_nc_vars['zg']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['zg']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['ta'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['ta']['dimensions'] = ('leadtime','plev','lat','lon')
c3s_nc_vars['ta']['globattrs']['frequency'] = "12hr"
c3s_nc_vars['ta']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['ta']['globattrs']['level_type'] = "pressure"
c3s_nc_vars['ta']['attributes']['standard_name'] = "air_temperature"
c3s_nc_vars['ta']['attributes']['long_name'] = "Air Temperature"
c3s_nc_vars['ta']['attributes']['units'] = "K"
c3s_nc_vars['ta']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
c3s_nc_vars['ta']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['ta']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['hus'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['hus']['dimensions'] = ('leadtime','plev','lat','lon')
c3s_nc_vars['hus']['globattrs']['frequency'] = "12hr"
c3s_nc_vars['hus']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['hus']['globattrs']['level_type'] = "pressure"
c3s_nc_vars['hus']['attributes']['standard_name'] = "specific_humidity"
c3s_nc_vars['hus']['attributes']['long_name'] = "Specific Humidity"
c3s_nc_vars['hus']['attributes']['units'] = "1"
c3s_nc_vars['hus']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
c3s_nc_vars['hus']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['hus']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['ua'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['ua']['dimensions'] = ('leadtime','plev','lat','lon')
c3s_nc_vars['ua']['globattrs']['frequency'] = "12hr"
c3s_nc_vars['ua']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['ua']['globattrs']['level_type'] = "pressure"
c3s_nc_vars['ua']['attributes']['standard_name'] = "x_wind"
c3s_nc_vars['ua']['attributes']['long_name'] = "Eastward Wind"
c3s_nc_vars['ua']['attributes']['units'] = "m s-1"
c3s_nc_vars['ua']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
c3s_nc_vars['ua']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['ua']['attributes']['grid_mapping'] = "hcrs"

c3s_nc_vars['va'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
c3s_nc_vars['va']['dimensions'] = ('leadtime','plev','lat','lon')
c3s_nc_vars['va']['globattrs']['frequency'] = "12hr"
c3s_nc_vars['va']['globattrs']['modeling_realm'] = "atmos"
c3s_nc_vars['va']['globattrs']['level_type'] = "pressure"
c3s_nc_vars['va']['attributes']['standard_name'] = "y_wind"
c3s_nc_vars['va']['attributes']['long_name'] = "Northward Wind"
c3s_nc_vars['va']['attributes']['units'] = "m s-1"
c3s_nc_vars['va']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
c3s_nc_vars['va']['attributes']['cell_methods'] = "leadtime: point"
c3s_nc_vars['va']['attributes']['grid_mapping'] = "hcrs"

# Alternative variables for ua/va
# c3s_nc_vars['rv'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
# c3s_nc_vars['rv']['dimensions'] = ('leadtime','plev','lat','lon')
# c3s_nc_vars['rv']['globattrs']['frequency'] = "12hr"
# c3s_nc_vars['rv']['globattrs']['modeling_realm'] = "atmos"
# c3s_nc_vars['rv']['globattrs']['level_type'] = "pressure"
# c3s_nc_vars['rv']['attributes']['standard_name'] = "atmoshphere_relative_vorticity"
# c3s_nc_vars['rv']['attributes']['long_name'] = "Relative Vorticity"
# c3s_nc_vars['rv']['attributes']['units'] = "s-1"
# c3s_nc_vars['rv']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
# c3s_nc_vars['rv']['attributes']['cell_methods'] = "leadtime: point"
# c3s_nc_vars['rv']['attributes']['grid_mapping'] = "hcrs"

# c3s_nc_vars['wnddiv'] = {'dimensions':(), 'auxcoords':(), 'attributes':{}, 'globattrs':{}, 'values': [], 'modify':{} }
# c3s_nc_vars['wnddiv']['dimensions'] = ('leadtime','plev','lat','lon')
# c3s_nc_vars['wnddiv']['globattrs']['frequency'] = "12hr"
# c3s_nc_vars['wnddiv']['globattrs']['modeling_realm'] = "atmos"
# c3s_nc_vars['wnddiv']['globattrs']['level_type'] = "pressure"
# c3s_nc_vars['wnddiv']['attributes']['standard_name'] = "divergence_of_wind"
# c3s_nc_vars['wnddiv']['attributes']['long_name'] = "Divergence of Wind"
# c3s_nc_vars['wnddiv']['attributes']['units'] = "s-1"
# c3s_nc_vars['wnddiv']['attributes']['coordinates'] = "reftime realization time leadtime plev lat lon"
# c3s_nc_vars['wnddiv']['attributes']['cell_methods'] = "leadtime: point"
# c3s_nc_vars['wnddiv']['attributes']['grid_mapping'] = "hcrs"
