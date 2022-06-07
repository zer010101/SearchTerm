from requests    import request
from re          import findall

from .exceptions import CaptchaError, ResultsError, RequestFailure, QueryError
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

BLACKLISTED_DOMAINS = [
    'google.com',
    'w3.org'
]

HEADERS = {
    'Host'           : 'www.google.com',
    'Referer'        : 'https://google.com/',
    'Accept'         : '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5',
    'Connection'     : 'close',
    'Cookies'        : 'COOKIE_UPDATES_HERE'
}

class SearchTerm:

    def __init__(self, query = None, gdork = None, proxy = None) -> None:
        # Query gets set here if present.
        if query == '':
            raise QueryError
            
        self.query    = query
        
        if gdork:
           # Google Dork gets set here if present.
           self.gdork = gdork
        else:
           # Otherwise we use this dork.
           self.gdork = f'intext:"{self.query}"'
        # Apply proxy IF present.   
        self.proxy    = proxy
        self.urls     = []
        
    @staticmethod
    def _headers() -> dict:    
        cookie = []
        resp   = request(
            method = 'GET',
            url    = 'http://www.google.com'
        )
        
        # Apply Each Value Into Our Cookie.
        for key, value in resp.cookies.items(): 
            cookie.append(f'{key}={value};')
        # Make a copy of our headers. 
        r_headers = HEADERS.copy()
        r_headers.update({'Cookies' : ''.join(cookie)})
        
        return r_headers


    def _detect_captcha(self):
        # If google blocks the request.
        return 'Our systems have detected unusual traffic from your computer network' in self.r
           
    @staticmethod
    def _format_url(url) -> str:
        
        # Remove useless strings if present.
        if '/url?q=' in url : url = url.replace('/url?q=','')
        if '&sa=' in url    : url = url.split('&sa=')[0]
        if '&amp' in url    : url = url.split('&amp')[0]
        if '\\x26amp' in url: url = url.split('\\x26amp')[0]
      
        return url
    
    
    @staticmethod
    def check_blacklist(url: str) -> bool:
        
        for blacklisted_domain in BLACKLISTED_DOMAINS:
            if blacklisted_domain in url:
                return True
             
             
    def _read_html(self) -> None:
        if self._detect_captcha(): 
            raise CaptchaError
            
        for url in findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.r):
         if self.check_blacklist(url): 
            continue
         
         if not url in self.urls: 
            self.urls.append(self._format_url(url))

        if not self.urls: 
            raise ResultsError
            


    def _create_request(self) -> None:
        # Constructs a request to google.
        try:
            # If request was a success.
            return request(
                method  = 'GET',
                url     = f'https://www.google.com/search?q={self.gdork}',
                headers = self._headers(),
                proxies = {'https': self.proxy}
            ).text 
        except Exception as e: 
            raise RequestFailure
         
         
    def _execute(self) -> list:
        self.r  = self._create_request()
        # Find URLS.
        self._read_html()
        # Return URLS.
        return self.urls
