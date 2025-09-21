# Copyright (c) 2025, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

import pandas as pd
import os

class airport_info:
  r"""Airports Infomaion

  飛行場情報クラス
  """
  def __init__(self):
    self._df = pd.read_json(os.path.join(os.path.dirname(__file__), "data", "nws", "stations.json"))

  def search_icao_airport_code(self, code:str) -> pd.DataFrame:
    r"""Search airport for ICAO code

    ICAOコードで飛行場を検索

    Parameters
    --------
    code: `str`
      ICAO code

    Returns
    -------
    df: `pandas.DataFrame`

    Note
    ----
    Return exact match results.

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.search_icao_airport_code("RJAA")
    >>> print(df)
    """
    return self._df[self._df["icaoId"] == code]

  def search_iata_airport_code(self, code:str) -> pd.DataFrame:
    r"""Search airport for IATA code

    IATAコードで飛行場を検索

    Parameters
    --------
    code: `str`
      IATA code

    Returns
    -------
    df: `pandas.DataFrame`

    Note
    ----
    Return exact match results.

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.search_iata_airport_code("NRT")
    >>> print(df)
    """
    return self._df[self._df["iataId"] == code]

  def search_icao_airport_code_match(self, code:str) -> pd.DataFrame:
    r"""Search airport for ICAO code

    ICAOコードで飛行場を検索

    Parameters
    --------
    code: `str`
      ICAO code

    Returns
    -------
    df: `pandas.DataFrame`

    Note
    ----
    Return search results matched by regular expressions.

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.search_icao_airport_code_match(r'^RJ[a-zA-Z0-9]+$'))
    >>> print(df)
    """
    return self._df[self._df["icaoId"].str.match(code)]

  def search_iata_airport_code_match(self, code:str) -> pd.DataFrame:
    r"""Search airport for IATA code

    IATAコードで飛行場を検索

    Parameters
    --------
    code: `str`
      IATA code

    Returns
    -------
    df: `pandas.DataFrame`

    Note
    ----
    Return search results matched by regular expressions.

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.search_iata_airport_code_match(r'^RO[a-zA-Z]+$'))
    >>> print(df)
    """
    return self._df[self._df["iataId"].str.match(code)]

  def search_elem_code_match(self, elem:str, code:str) -> pd.DataFrame:
    r"""Search an element code

    コードで要素名を検索

    Parameters
    --------
    elem: `str`
      elemment
    
    code: `str`
      code

    Returns
    -------
    df: `pandas.DataFrame`

    Note
    ----
    Return search results matched by regular expressions.

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.search_elem_code_match(r'^[a-zA-Z]+(NPMOD)$'))
    >>> print(df)
    """
    return self._df[self._df[elem].str.match(code)]
  
  def get_df(self) -> pd.DataFrame:
    r"""variables

    Returns
    -------
    columns: `pd.DataFrame`

    Examples
    --------
    >>> airport = airport_info()
    >>> df = airport.get_df())
    >>> print(df)
    """
    return self._df
  
  def get_columns(self) -> list:
    r"""variables

    Returns
    -------
    columns: `list`

    Examples
    --------
    >>> airport = airport_info()
    >>> columns = airport.get_columns())
    >>> print(columns)
    """
    return self._df.columns.to_list()

if __name__ == "__main__":
  airport = airport_info()
  print(airport.search_icao_airport_code("RJAA").values[0])