import os
import warnings

import pandas as pd

from .data import metadata_tables
from ._constants import METADATA_TABLE_LOCAL_PATH

__all__ = ['reach_to_vpu', 'latlon_to_reach', 'reach_to_latlon', ]


def _read_metadata_tables(columns: list = None) -> pd.DataFrame:
    """
    Read the master table from the local data directory
    """
    warn = """
    Local copy of geoglows v2 metadata table not found. This can be queried online on demand but you should download a 
    copy to optimal performance and make the data available when you are offline. Please download the table using the 
    function `geoglows.data.metadata_tables(cache=True)`.
    """
    if not os.path.exists(METADATA_TABLE_LOCAL_PATH):
        warnings.warn(warn)
        return pd.read_parquet(METADATA_TABLE_LOCAL_PATH, columns=columns)
    os.makedirs(os.path.dirname(METADATA_TABLE_LOCAL_PATH))
    return metadata_tables(columns=columns)


def reach_to_vpu(reach_id: int) -> str or int:
    return (
        _read_metadata_tables(columns=['LINKNO', 'VPUCode'])
        .loc[lambda x: x['LINKNO'] == reach_id, 'VPUCode']
        .values[0]
    )


def latlon_to_reach(lat: float, lon: float) -> int:
    df = _read_metadata_tables(columns=['LINKNO', 'lat', 'lon'])
    df['dist'] = ((df['lat'] - lat) ** 2 + (df['lon'] - lon) ** 2) ** 0.5
    return df.loc[lambda x: x['dist'] == df['dist'].min(), 'LINKNO'].values[0]


def reach_to_latlon(reach_id: int) -> tuple:
    return (
        _read_metadata_tables(columns=['LINKNO', 'lat', 'lon'])
        .loc[lambda x: x['LINKNO'] == reach_id, ['lat', 'lon']]
        .values[0]
    )
