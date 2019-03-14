#!python3
# access_rates.py

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

from gridfinder._util import clip_raster


def make_same_as(curr_arr, curr_aff, curr_crs, dest_arr_like, dest_affine, dest_crs):
    """

    """

    dest_arr = np.empty_like(dest_arr_like)

    with rasterio.Env():
        reproject(
            source=curr_arr,
            destination=dest_arr,
            src_transform=curr_aff,
            dst_transform=dest_affine,
            src_crs=curr_crs,
            dst_crs=dest_crs,
            resampling=Resampling.nearest,
        )

    return dest_arr


def buffer_raster(arr):
    """

    """

    max_row = arr.shape[0]
    max_col = arr.shape[1]
    buffered = arr.copy()

    for row in range(0, max_row):
        for col in range(0, max_col):
            loc = (row, col)
            if arr[loc] == 1:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        next_row = row + i
                        next_col = col + j
                        next_loc = (next_row, next_col)

                        if not (
                            next_row < 0
                            or next_col < 0
                            or next_row >= max_row
                            or next_col >= max_col
                            or next_loc == loc
                        ):
                            buffered[next_loc] = 1

    return buffered


def calc_weights(pop, urban, ntl, targets, more, access):
    """

    """

    # The calculated weights for each segment will go here

    if access["urban"] > 0.9:
        weights = np.ones_like(pop) * access["rural"]
        weights[urban >= 2] = access["urban"]
        return weights

    weights = np.zeros_like(pop)

    # Investigate each combination of urban/rural and four quartiles
    # of population density
    for loc in ["urban", "rural"]:
        for q in [0.25, 0.5, 0.75, 1]:

            # Values of 2 and 3 are considered urban
            if loc == "urban":
                condition_del = urban < 3
                access_level = access["urban"]
            else:
                condition_del = urban >= 3
                access_level = access["rural"]

            # Ignore errors from doing arr[arr < x] with nan values
            with np.errstate(invalid="ignore"):
                pop_temp = np.copy(pop)  # local copy of pop for this loop
                pop_temp[condition_del] = np.nan  # remove urban/rural
                pop_temp[targets == 0] = np.nan  # remove not electrified

                # Filter to only keep this quartile
                quant_below = np.nanquantile(pop_temp, q - 0.25)
                quant = np.nanquantile(pop_temp, q)
                pop_temp[pop_temp <= quant_below] = np.nan
                pop_temp[pop_temp > quant] = np.nan

                # Get the average brightness per person of the top x% for this quartile
                # Where x is the rural/urban access rate
                ntl_per_pop = ntl / pop_temp
                ntl_quant = min(max(1 - access_level - more[loc][q], 0), 1)
                ntl_cut = np.nanquantile(ntl_per_pop, ntl_quant)

                # Create a weights array and assign values accoring to the formula below
                w = np.zeros_like(pop)
                w = 1 - (ntl_cut - ntl_per_pop) / ntl_cut
                w[w > 0.95] = 0.95  # limit values to max 1
                w[np.isnan(w)] = 0

                # Add the sucessive weights to the main array
                weights += w

    return weights


def calc_pop_elec(pop, urban, ntl, targets, access):
    """

    """

    more = {
        "urban": {0.25: 0.015, 0.5: 0.02, 0.75: 0.025, 1: 0.03},
        "rural": {0.25: 0.005, 0.5: 0.01, 0.75: 0.015, 1: 0.02},
    }

    runs = 0
    prev_access_model_total = None
    while True:
        runs += 1
        weights = calc_weights(pop, urban, ntl, targets, more, access)

        # Create electrified array by multiplying
        pop_elec = pop * weights
        pop_elec[np.isnan(pop_elec)] = 0

        access_model_total = np.nansum(pop_elec) / np.nansum(pop)
        print(f'{access["total"]:.4f}', f'{access_model_total:.4f}')

        if abs(access["total"] - access_model_total) < 0.02:
            print("Reached accuracy")
            break
        elif runs >= 20:
            print("STOP - reached limit")
            break
        elif access_model_total == prev_access_model_total:
            print("STOP - no change")
        else:
            if access_model_total < access["total"]:
                direc = 1
            else:
                direc = -1
            for k, v in more.items():
                for l, w in v.items():
                    more[k][l] += (
                        more[k][l]
                        * direc
                        * (20 / runs)
                        * abs(access["total"] - access_model_total)
                    )

    return pop_elec


def regularise(country, aoi, pop_in, urban_in, ntl_in, targets_in):
    """

    """

    # Clip all to same AOI
    pop, affine, crs = clip_raster(pop_in, aoi)
    urban, urban_aff, urban_crs = clip_raster(urban_in, aoi)
    ntl, ntl_aff, ntl_crs = clip_raster(ntl_in, aoi)
    targets, targets_aff, targets_crs = clip_raster(targets_in, aoi)

    pop[pop < 0] = 0
    urban[urban < 0] = 0
    ntl[ntl < 0] = 0
    targets[targets < 0] = 0

    if pop.ndim > 2:
        pop = pop[0]
    if urban.ndim > 2:
        urban = urban[0]
    if ntl.ndim > 2:
        ntl = ntl[0]
    if targets.ndim > 2:
        targets = targets[0]

    urban = make_same_as(urban, urban_aff, urban_crs, pop, affine, crs)
    ntl = make_same_as(ntl, ntl_aff, ntl_crs, pop, affine, crs)
    targets = make_same_as(targets, targets_aff, targets_crs, pop, affine, crs)
    assert pop.shape == urban.shape == ntl.shape == targets.shape

    # Drop 0 pop makes visual inspection easier
    # And so that quantile values ignore 0
    pop[pop == 0] = np.nan

    targets = buffer_raster(targets)

    return pop, urban, ntl, targets, affine, crs


def estimate(pop, urban, ntl, targets, access):
    """

    """

    pop_elec = calc_pop_elec(pop, urban, ntl, targets, access)

    access_model_total = np.nansum(pop_elec) / np.nansum(pop)
    access_model_urban = np.nansum(pop_elec[urban >= 3]) / np.nansum(pop[urban >= 3])
    access_model_rural = np.nansum(pop_elec[urban < 3]) / np.nansum(pop[urban < 3])

    print("Access\tActual\tModel")
    print(f"Total:\t{access['total']:.2f}\t{access_model_total:.2f}")
    print(f"Urban:\t{access['urban']:.2f}\t{access_model_urban:.2f}")
    print(f"Rural:\t{access['rural']:.2f}\t{access_model_rural:.2f}")

    return pop_elec, access_model_total
