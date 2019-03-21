#!python3
# local_costs.py

from math import sqrt

import numpy as np


def lv_length(pop, peak_kw_pp=1):
    """
    Calculate local MV, LV and connection cost for given population.
    """

    if pop <= 0:
        return 0

    num_people_per_hh = 4
    grid_cell_area = 0.45 * 0.45  # km2
    lv_line_capacity = 10  # kW/line

    peak_load = pop * peak_kw_pp  # kW
    no_lv_lines = peak_load / lv_line_capacity

    hh_per_lv_network = (pop / num_people_per_hh) / no_lv_lines
    lv_unit_length = sqrt(grid_cell_area / (pop / num_people_per_hh)) * sqrt(2) / 2
    lv_lines_length_per_lv_network = 1.333 * hh_per_lv_network * lv_unit_length
    total_lv_length = no_lv_lines * lv_lines_length_per_lv_network

    return total_lv_length


def apply_lv_length(pop_elec):
    """

    """

    pop_elec = pop_elec.astype(np.int)
    f = np.vectorize(lv_length, otypes=[np.float32])
    costs = f(pop_elec)
    total_cost = np.sum(costs)
    print(f"Total cost: USD {total_cost:,}")

    return costs.astype(np.float32)
