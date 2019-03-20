# CFsites-related elements (CFMIP)
# A file named cfsites_grid_file_name must be provided at runtime, which
# includes a field named cfsites_grid_field_id, defined on an unstructured
# grid which is composed of CF sites
cfsites_radix = "cfsites"
cfsites_domain_id = cfsites_radix + "_domain"
cfsites_grid_id = cfsites_radix + "_grid"
cfsites_grid_file_name = cfsites_radix + "_grid"
cfsites_grid_file_id = cfsites_radix + "_file"
cfsites_grid_field_id = cfsites_radix + "_field"


def cfsites_input_filedef():
    """
    Returns a file definition for defining a COSP site grid by reading a field named
    'cfsites_grid_field' in a file named 'cfsites_grid.nc'
    """
    # rep='<file id="%s" name="%s" mode="read" >\n'%\
    rep = '<file id="%s" name="%s" mode="read" output_freq="1y" >\n' % \
          (cfsites_grid_file_id, cfsites_grid_file_name) + \
          '\t<field id="%s" operation="instant" grid_ref="%s" />\n' % (cfsites_grid_field_id, cfsites_grid_id) + \
          ' </file>'
    return rep


def add_cfsites_in_defs(grid_defs, domain_defs):
    """
    Add grid_definition and domain_definition for cfsites in relevant dicts
    """
    grid_defs[cfsites_grid_id] = '<grid id="%s" > <domain domain_ref="%s" /> </grid>\n' % \
                                 (cfsites_grid_id, cfsites_domain_id)
    domain_defs[
        cfsites_radix] = ' <domain id="%s" type="unstructured" prec="8" lat_name="latitude" ' \
                         'lon_name="longitude" dim_i_name="site" > ' % cfsites_domain_id + \
                         '<generate_rectilinear_domain/>' + \
                         '<interpolate_domain order="1" renormalize="true" mode="read_or_compute" ' \
                         'write_weight="true" />' + \
                         '</domain>'
