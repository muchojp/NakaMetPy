# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Original source lisence:
# Copyright (c) 2015,2016,2017,2018 MetPy Developers.
#
"""Tools for calculating with weather data."""

# What do we want to pull into the top-level namespace?
# import os
import sys
# import warnings

if sys.version_info < (3,):
    raise ImportError(
        """You are running NakaMetPy 0.1 or greater on Python 2.
        NakaMetPy does not work on Python 2.
        """)

# Must occur before below imports
# warnings.filterwarnings('ignore', 'numpy.dtype size changed')
# os.environ['PINT_ARRAY_PROTOCOL_FALLBACK'] = '0'

# from nakametpy._version import get_version  # noqa: E402
from ._version import get_version  # noqa: E402
__version__ = get_version()
del get_version
