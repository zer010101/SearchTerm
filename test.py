import searchterm

search = searchterm.google(query = 'QUERY_GOES_HERE')
for url in search:
    print(url)