from .dorker import SearchTerm
"""
CREDITS::
---------------------------------------
Source Title: searchterm
Author......: https://github.com/PyLore
Released....: 3/25/2022
Summary.....: A Python Library That
              Simplifies Google Dorking.
---------------------------------------

USAGE::
---------------------------------------
import searchterm

searchterm.google(query = 'QUERY_GOES_HERE')
searchterm.google(gdork = 'DORK_GOES_HERE')

Proxy Example:
searchterm.google(query = 'QUERY_GOES_HERE', proxy = 'http://127.0.0.1:8080')
---------------------------------------
"""
def google(query = None, gdork = None, proxy = None) -> list:
    session = SearchTerm(
        query = query,
        gdork = gdork,
        proxy = proxy
    )
    if session.execute():
        return session.urls
      
