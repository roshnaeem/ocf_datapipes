import numpy as np
import pytest

from ocf_datapipes.transform.xarray import CreatePVImage


@pytest.mark.skip("Too Memory Intensive")
def test_create_pv_image(passiv_datapipe, sat_datapipe):
    pv_image_datapipe = CreatePVImage(passiv_datapipe, sat_datapipe)
    data = next(iter(pv_image_datapipe))
    assert np.max(data) > 0


@pytest.mark.skip("Too Memory Intensive")
def test_create_pv_image_normalized(passiv_datapipe, sat_datapipe):
    pv_image_datapipe = CreatePVImage(passiv_datapipe, sat_datapipe, normalize=True)
    data = next(iter(pv_image_datapipe))
    assert np.isclose(np.max(data), 1.0)
    assert np.isclose(np.min(data), 0.0)
