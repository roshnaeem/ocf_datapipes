"""Remove any data with nans"""
import logging

import xarray as xr
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

logger = logging.getLogger(__name__)


@functional_datapipe("remove_nans")
class RemoveNansIterDataPipe(IterDataPipe):
    """Remove nans from the dataset"""

    def __init__(self, source_datapipe: IterDataPipe, time_dim: str = "time_utc"):
        """
        Remove bad PV systems

        Args:
            source_datapipe: Datapipe of PV data
        """
        self.source_datapipe = source_datapipe
        self.time_dim = time_dim

    def __iter__(self) -> xr.DataArray:
        for xr_data in self.source_datapipe:
            logger.debug(
                f"Dropping nans on {self.time_dim}. Currently there are {len(xr_data[self.time_dim])}"
            )
            logger.debug(f"Minimum value is {xr_data[self.time_dim].min()}")
            logger.debug(f"Maximum value is {xr_data[self.time_dim].max()}")
            xr_data_new = xr_data.dropna(dim=self.time_dim)
            logger.debug(
                f"After dropping nans on {self.time_dim}, there are {len(xr_data_new[self.time_dim])}"
            )
            if len(xr_data_new[self.time_dim]) == 0:
                logger.debug(xr_data)
                raise Exception("Data has only nans in it")
            logger.debug(f"Minimum value is {xr_data_new[self.time_dim].min()}")
            logger.debug(f"Maximum value is {xr_data_new[self.time_dim].max()}")
            yield xr_data_new
