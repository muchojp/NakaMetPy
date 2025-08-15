import pandas as pd

class airport_info:
  r"""Airports Infomaion

  飛行場情報クラス
  """
  def __init__(self):
    self._df = pd.read_json("./data/nws/stations.json")

  def search_icaoId(self, icaoId:str) -> pd.DataFrame:
    r"""Search airport for ICAO code

    ICAOコードで飛行場を検索

    Parameters
    --------
    icaoId: `str`
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
    >>> df = airport.search_icaoId("RJAA")
    >>> print(df)
    """
    return self._df[self._df["icaoId"] == icaoId]

  def search_iataId(self, iataId:str) -> pd.DataFrame:
    r"""Search airport for IATA code

    IATAコードで飛行場を検索

    Parameters
    --------
    iataId: `str`
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
    >>> df = airport.search_iataId("NRT")
    >>> print(df)
    """
    return self._df[self._df["iataId"] == iataId]

  def search_icaoId_match(self, icaoId:str) -> pd.DataFrame:
    r"""Search airport for ICAO code

    ICAOコードで飛行場を検索

    Parameters
    --------
    icaoId: `str`
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
    >>> df = airport.search_icaoId_match(r'^RJ[a-zA-Z0-9]+$'))
    >>> print(df)
    """
    return self._df[self._df["icaoId"].str.match(icaoId)]

  def search_iataId_match(self, iataId:str) -> pd.DataFrame:
    r"""Search airport for IATA code

    IATAコードで飛行場を検索

    Parameters
    --------
    iataId: `str`
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
    >>> df = airport.iataId_match(r'^RO[a-zA-Z]+$'))
    >>> print(df)
    """
    return self._df[self._df["iataId"].str.match(iataId)]
  
  def columns(self) -> list:
    r"""variables

    Returns
    -------
    columns: `list`

    Examples
    --------
    >>> airport = airport_info()
    >>> columns = airport.columns())
    >>> print(columns)
    """
    return self._df.columns.to_list()

if __name__ == "__main__":
  # print(search_icaoId("RJ"), type(search_icaoId("RJ")))
  # print(search_iataId("NRT"), type(search_iataId("NRT")))
  airport = airport_info()
  # print(airport.search_icaoId("RJAA"))
  # print(airport.search_iataId("NRT"))
  # print(airport.search_icaoId_match(r'^RJ[a-zA-Z0-9]+$'))
  # print(airport.search_icaoId_match(r'^RO[a-zA-Z]+$'))
  # print(airport.search_icaoId_match(r'^[a-zA-Z]+JF[a-zA-Z]$'))
  print(airport.columns())