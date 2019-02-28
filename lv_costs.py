#!python3

"""
LV lines + grid capex

Functions
- assess_lvlines
- lvlines_length
- lines_capex

"""


def assess_lvlines(MVlines_in, aoi_in, ntl_in, pop_in, elec_rates):
    """Assess location and length of lv lines

    Parameters
    ----------
    MVlines_in : str, Path
        Path to a MV_lines raster.
    aoi_in : str, Path or GeoDataFrame
        AOI to clip the pop raster
    ntl_in : str, Path
        Path to a raster file
    pop_in: str, Path
    path to a population raster such as GHS or HRSL.
    elec_rates : global, urban and rural electrification rates

    Returns
    -------
    raster with all lines
    """

    # Keep only the cells 1km (or more?) around the MVlines + the HV lines cells

    # For countries with high access rate, connect every household around the MV lines
    if c_rate > 95%:
        lvlines_length(MVlines_in, aoi_in, pop_in)

    else:
        split all rasters between urban and rur
        al
        sort by pop density and create 4 groups each of them with 25% of the cells (urban_1 to urban_4, rural_1 to rural_5)
        sort each group by brightness/pop 
        In each group, Assign a weight to each cell w = 1-((average brightness of top x% of cells in group)-(brightness of cell i))/(brightness of top x% of cells in group). x could be the country rural/urban electrification rate.
        In each cell calculate the grid electrified population: w*pop
        Create a grid electrified pop raster elec_pop
        lvlines_length(MVlines_in, aoi_in, elec_pop)

    Create a raster with all lines

    return alllines_raster


def lvlines_length(MVlines_in, aoi_in, pop_in):
    """
    Parameters
        ----------
    MVlines_in : str, Path
        Path to a MV_lines raster. 
    aoi_in : str, Path or GeoDataFrame
        AOI to clip the pop raster
    pop_in: str, Path
        path to a population raster such as GHS or HRSL.
    Returns
    -------
    raster with all lines
    """

    # use the code you provided
    num_people_per_hh = 4
    lv_line_max_length = 1  # km(depends what we choose above  )
    no_mv_lines = 1  # default value given the size of our cells, otherwise need to count the nb of lines in each cell
    for each cell  # obviously let's not write a for loop but I don't know how to call the cells
        lv_networks_lim_length = ((self.grid_cell_area / no_mv_lines) / (self.lv_line_max_length / sqrt(2))) ** 2
        actual_lv_lines = people / num_people_per_hh
        hh_per_lv_network = (people / num_people_per_hh) / (actual_lv_lines * no_mv_lines)
        lv_unit_length = sqrt(self.grid_cell_area / (people / num_people_per_hh)) * sqrt(2) / 2
        lv_lines_length_per_lv_network = 1.333 * hh_per_lv_network * lv_unit_length
        total_lv_lines_length = no_mv_lines * actual_lv_lines * lv_lines_length_per_lv_network

    return a raster with LV line length


def lines_capex(alllines_in):
    """
    Parameters
        ----------
    allines_in : str, Path
        Path to a grid lines raster. 

    Returns
    -------
    raster with all lines + capex
    """

    lvcapex = 15  # (k$/km)	
    mvcapex = 30  # (k$/km)
    hvcapex = 15  # (k$/km)
    grid = gpd.read_file(alllines_in)
    # I don't know if the data will look like that but we can adjust when we have the final alllines_in file
    grid['Capex'] = 0
    grid.loc[grid['Line'] == 'HV', 'Capex'] = grid.loc[grid['Line'] == 'HV', 'Capex']*hvcapex
    grid.loc[grid['Line'] == 'MV', 'Capex'] = grid.loc[grid['Line'] == 'MV', 'Capex']*mvcapex
    grid.loc[grid['Line'] == 'LV', 'Capex'] = grid.loc[grid['Line'] == 'LV', 'Capex']*lvcapex
