#!python3
# local_costs.py

from math import sqrt

import numpy as np


def lv_length(
    pop,
    peak_kw_pp=2,
    people_per_hh=4,
    cell_area=1,
    line_capacity=155555,
):
    """
    Calculate length of low-voltage lines in a grid cell.

    Parameters
    ----------
    pop : int
        Number of people.
    peak_kw_pp : float
        Peak kW demand per person.
    people_per_hh : int
        Num people per household.
    cell_area : float
        Size of grid cell in km2.
    line_capacity : float
        LV line carrying capacity in kW/line.

    Returns
    -------
    total_lv_length : float
        Length of LV lines in km.
    """

    if pop < 1:
        return 0

    num_lines = pop*peak_kw_pp/line_capacity
    unit_length = sqrt(cell_area/(pop/people_per_hh))
    total_length = num_lines*unit_length

    return total_length

def apply_lv_length(pop_elec, **kwargs):
    """

    """

    pop_elec = pop_elec.astype(np.int)
    f = np.vectorize(lv_length, otypes=[np.float32])
    lengths = f(pop_elec, **kwargs)
    total_length = np.sum(lengths)
    print(f"Total length: {total_length:,} km")

    return lengths.astype(np.float32)
