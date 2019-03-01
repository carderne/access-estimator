#!python3
# local_costs.py

from math import sqrt

import numpy as np


def get_cost(pop):
    """
    Calculate local MV, LV and connection cost for given population.
    """

    if pop < 2:
        return 0

    connection_cost_per_hh = 500  # USD/hh
    mv_line_cost = 45e3  # USD/km
    lv_line_cost = 15e3  # USD/km

    num_people_per_hh = 4
    grid_cell_area = 0.45 * 0.45  # in km2, normally 1km2

    lv_line_max_length = 1  # km
    lv_line_capacity = 10  # kW/line
    mv_line_max_length = 50  # km
    mv_line_capacity = 50  # kW/line

    peak_load = pop * 1  # kW
    no_mv_lines = peak_load / mv_line_capacity
    no_lv_lines = peak_load / lv_line_capacity

    lv_networks_lim_capacity = no_lv_lines / no_mv_lines
    lv_networks_lim_length = (
        (grid_cell_area / no_mv_lines) / (lv_line_max_length / sqrt(2))
    ) ** 2
    actual_lv_lines = min(
        [
            pop / num_people_per_hh,
            max([lv_networks_lim_capacity, lv_networks_lim_length]),
        ]
    )

    hh_per_lv_network = (pop / num_people_per_hh) / (actual_lv_lines * no_mv_lines)
    lv_unit_length = sqrt(grid_cell_area / (pop / num_people_per_hh)) * sqrt(2) / 2
    lv_lines_length_per_lv_network = 1.333 * hh_per_lv_network * lv_unit_length
    total_lv_length = no_mv_lines * actual_lv_lines * lv_lines_length_per_lv_network

    line_reach = (grid_cell_area / no_mv_lines) / (
        2 * sqrt(grid_cell_area / no_lv_lines)
    )
    total_mv_length = min([line_reach, mv_line_max_length]) * no_mv_lines

    mv_cost = total_mv_length * mv_line_cost
    lv_cost = total_lv_length * lv_line_cost
    conn_cost = (pop / num_people_per_hh) * connection_cost_per_hh

    return int(mv_cost + lv_cost + conn_cost)


def apply(pop_elec):
    """

    """

    pop_elec = pop_elec.astype(np.int)
    f = np.vectorize(get_cost, otypes=[np.int])
    costs = f(pop_elec)
    total_cost = np.sum(costs)
    print(f"Total cost: USD {total_cost:,}")

    return costs.astype(np.float)
