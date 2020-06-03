"""
Load full dataset h5 file example
using the msd_summary_file.h5.
This file only contains the metadata.

It doesn't contain tags or song analysis features.
"""

import os
import sys
import pathlib
import pandas as pd

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../../.."
    )
)


from recommender.infrastructure.msd.loaders import hdf5_getters


MSD_DATA_DIR = os.path.normpath(os.getenv("DATA_DIR") or os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "../../../../data/msdchallenge"
))


h5 = hdf5_getters.open_h5_file_read(
    os.path.join(MSD_DATA_DIR,"msd_summary_file.h5"))

num_songs = hdf5_getters.get_num_songs(h5)
print(num_songs)