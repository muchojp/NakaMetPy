# Copyright (c) 2021, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# Original source lisence:
# Copyright (c) 2019 MetPy Developers.
# 
# 
"""Tools for versioning."""


def get_version():
    """Get NakaMetPy's version.
    Either get it from package metadata, or get it using version control information if
    a development install.

    PyPIに登録していれば楽にバージョンの管理ができるが、今のところその予定はないため、手打ちする
    """
    """ try:
        from setuptools_scm import get_version
        return get_version(root='../..', relative_to=__file__,
                           version_scheme='post-release')
    except (ImportError, LookupError):
        try:
            from importlib.metadata import version, PackageNotFoundError
        except ImportError:  # Can remove when we require Python > 3.7
            from importlib_metadata import version, PackageNotFoundError

        try:
            return version(__package__)
        except PackageNotFoundError:
            return 'Unknown' """
    # return '0.1.0' # (2021.01.19)
    return '0.2.0' # (2021.02.18)
