import requests, re

from .exceptions import CaptchaError,ResultsError
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
class Google_Dorker:
    def __init__(self, query = None, gdork = None, proxy = None):
        """Query gets set here if present."""
        self.query    = query
        if gdork:
           """Google Dork gets set here if present."""
           self.gdork = gdork
        else:
           """Otherwise we use this dork."""
           self.gdork = f'intext:"{self.query}"'
        """Apply proxy IF present."""   
        self.proxy    = proxy
        
    @staticmethod
    def headers():    
        """Scrape our headers."""
        session     = requests.Session()
        s           = session.get('http://www.google.com')
        cookie      = ''
        """Apply Each Value Into Our Cookie."""
        for key, value in s.cookies.items():
            cookie += f'{key}={value}; '
        return  {
                'Host'           : 'www.google.com',
                'Referer'        : 'https://google.com/',
                'Accept'         : '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent'     : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5',
                'Connection'     : 'keep-alive',
                'Cookies'        : cookie
                }

    @staticmethod
    def detect_captcha(r):
       """ If google blocks the request we return True"""
       if 'Our systems have detected unusual traffic from your computer network' in r:
           return True
       return False   
           
    @staticmethod
    def format_url(url):
       """Remove useless strings if present."""
       if '/url?q=' in url:
           url = url.replace('/url?q=','')
       if '&sa=' in url:    
           url = url.split('&sa=')[0]
       return url
       
    @staticmethod
    def read_html(r):
       urls = []
       """Check for google captcha"""
       if Google_Dorker.detect_captcha(r):
           raise CaptchaError
       """Otherwise continue""" 
       links = re.findall(r'http[s*]:[a-zA-Z0-9_.+-/#~]+',r)
       for link in links:
          """If 'http' is present in link."""
          if 'http' in link:
              if link in urls:
                  pass
              else:  
                  url = Google_Dorker.format_url(link)
                  urls.append(url)
       return urls    

    def create_request(self):
        """Constructs a request to google."""
        try:
            """If Request Was A Success."""
            session = requests.Session()
            return session.get(
                        url     = f'https://www.google.com/search?q={self.gdork}',
                        headers = Google_Dorker.headers(),
                        proxies = {'https': self.proxy}
                        ).text 
        except Exception as e:
            """If The Request Failed."""
            return f"{e!r}"
            
    def main(self):
        """Executes all functions"""
        r    = Google_Dorker.create_request(self)
        """We Grab The URLS Now."""
        urls = Google_Dorker.read_html(r)
        """Return The URLS."""
        if urls == []:
           raise ResultsError
        return urls