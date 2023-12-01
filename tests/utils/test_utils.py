import numpy as np
from ocf_datapipes.utils.utils import searchsorted
from ocf_datapipes.utils.utils import combine_to_single_dataset, uncombine_from_single_dataset
# TODO - we should have a specific test data object instead of generating one from windnet
from ocf_datapipes.training.windnet import windnet_datapipe
from datetime import datetime
import xarray as xr


def test_searchsorted():
    ys = np.array([1, 2, 3, 4, 5], dtype=np.float32)
    assert searchsorted(ys, 2.1) == 2
    ys_r = np.array([5, 4, 3, 2, 1], dtype=np.float32)
    assert searchsorted(ys_r, 2.1, assume_ascending=False) == 3


def test_combine_uncombine_from_single_dataset(wind_configuration_filename):
    start_time = datetime(1900, 1, 1)
    end_time = datetime(2050, 1, 1)
    dp = windnet_datapipe(
        wind_configuration_filename,
        start_time=start_time,
        end_time=end_time,
    )
    dataset: xr.Dataset = next(iter(dp))
    assert isinstance(dataset, xr.Dataset)
    multiple_datasets = uncombine_from_single_dataset(dataset)
    for key in multiple_datasets.keys():
        if "time_utc" in multiple_datasets[key].coords.keys():
            time_coord = "time_utc"
        else:
            time_coord = "target_time_utc"
        for i in range(len(multiple_datasets[key][time_coord])):
            # Assert that data for each of the coords is the same
            for coord_key in multiple_datasets[key][i].coords.keys():
                np.testing.assert_equal(
                    multiple_datasets[key].isel({time_coord: i})[coord_key].values,
                    dataset[key][i][f"{key}__{coord_key}"].values,
                )
