from requests    import request
from re          import findall

from .exceptions import CaptchaError, ResultsError, QueryError
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

BLACKLISTED_DOMAINS = (
    'google.com',
    'w3.org'
)

HEADERS = {
    'Host'           : 'www.google.com',
    'Referer'        : 'https://google.com/',
    'Accept'         : '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent'     : 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36',
    'Connection'     : 'close',
    'Cookies'        : 'COOKIE_UPDATES_HERE'
}

CAPTCHA_ERROR = 'Our systems have detected unusual traffic from your computer network'

class SearchTerm:
    def __init__(self, query = None, gdork = None, proxy = None) -> None:
        # Query gets set here if present.
        if not query:
            raise QueryError
            
        self.query = query
        
        if gdork:
           # Google Dork gets set here if present.
           self.gdork = gdork
        else:
           # Otherwise we use this dork.
           self.gdork = f'intext:"{self.query}"'
        # Apply proxy IF present.   
        self.proxy = proxy
        self.urls  = []
        
        
    @staticmethod
    def _headers() -> dict:    
        cookie = []
        
        resp = request(
            method = 'GET',
            url    = 'http://www.google.com'
        )
        
        # Apply Each Value Into Our Cookie.
        for key, value in resp.cookies.items(): 
            cookie.append(f'{key}={value}')
        # Make a copy of our headers. 
        r_headers = HEADERS.copy()
        r_headers.update({'Cookies' : ';'.join(cookie)})
        
        return r_headers


    def _detect_captcha(self: object) -> bool:
        # If google blocks the request.
        return CAPTCHA_ERROR in self.r
           
        
    @staticmethod
    def _format_url(url: str) -> str:
        useless_strings = ('&sa=','&amp','\\x26amp')
        # Remove useless strings if present.
        if '/url?q=' in url : url = url.replace('/url?q=','')
        
        for useless_string in useless_strings:
            if useless_string in url: 
                url = url.split(useless_string)[0]
      
        return url
    
    
    @staticmethod
    def if_blacklist(url: str) -> bool:
        for blacklisted_domain in BLACKLISTED_DOMAINS:
            if blacklisted_domain in url:
                return True
             
             
    def _read_html(self: object) -> None:
        if self._detect_captcha(): 
            raise CaptchaError
            
        for url in findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.r):
            
            if self.if_blacklist(url): 
                continue
         
            if not url in self.urls: 
                self.urls.append(self._format_url(url))

        if not self.urls: 
            raise ResultsError
            

    def _create_request(self: object) -> str:
        # Constructs a request to google.
        try:
            # If request was a success.
            return request(
                method  = 'GET',
                url     = f'https://www.google.com/search?q={self.gdork}',
                headers = self._headers(),
                proxies = {'https': self.proxy}
            ).text 
        except Exception:
            raise
         
         
    def _execute(self: object) -> bool:
        self.r = self._create_request()
        
        # Find URLS.
        self._read_html()
        return True
        
