import requests, re

from .exceptions import CaptchaError,ResultsError,RequestFailure,QueryError
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
class SearchTerm:
    blacklisted_urls = [
                       'https://maps.google.com/maps',
                       'https://support.google.com/websearch',
                       'https://accounts.google.com/ServiceLogin',
                       'https://www.google.com/search',
                       'https://www.google.com/preferences',
                       'https://policies.google.com/privacy',
                       'https://policies.google.com/terms',
                       'https://www.youtube.com/watch'
                       ]
    def __init__(self, query = None, gdork = None, proxy = None):
        #Query gets set here if present.
        if query == '':
            raise QueryError
        self.query    = query
        if gdork:
           #Google Dork gets set here if present.
           self.gdork = gdork
        else:
           #Otherwise we use this dork.
           self.gdork = f'intext:"{self.query}"'
        #Apply proxy IF present.   
        self.proxy    = proxy
        
    @staticmethod
    def _headers():    
        cookie = ''
        r      = requests.get('http://www.google.com')
        #Apply Each Value Into Our Cookie.
        for key, value in r.cookies.items(): 
            cookie = ''.join(f'{key}={value};')  
        return  {
                'Host'           : 'www.google.com',
                'Referer'        : 'https://google.com/',
                'Accept'         : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5',
                'Connection'     : 'close',
                'Cookies'        : cookie
                }

    @staticmethod
    def _detect_captcha(self):
       #If google blocks the request.
       return 'Our systems have detected unusual traffic from your computer network' in self.r
           
    @staticmethod
    def _format_url(url):
       #Remove useless strings if present.
       if '/url?q=' in url: url = url.replace('/url?q=','')
       if '&sa=' in url: url    = url.split('&sa=')[0]
       return url
       
    def _read_html(self):
       if self._detect_captcha(self): raise CaptchaError
       urls = []
       for link in re.findall(r'http[s*]:[a-zA-Z0-9_.+-/#~]+', self.r):
          if not (link in SearchTerm.blacklisted_urls and urls) and 'http' in link:
                urls.append(self._format_url(link))
       if not urls: raise ResultsError
       return urls 

    def _create_request(self):
        #Constructs a request to google.
        try:
            #If Request Was A Success.
            session = requests.Session()
            return session.get(
                        url     = f'https://www.google.com/search?q={self.gdork}',
                        headers = self._headers(),
                        proxies = {'https': self.proxy}
                        ).text 
        except Exception as e: raise RequestFailure
            
    def _execute(self):
        self.r  = self._create_request()
        #Return The URLS.
        return self._read_html()
