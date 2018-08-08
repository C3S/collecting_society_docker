# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire
#
# This script strips all styles from the discogs webpage to be fed into our database
#
# adapted from lukeldb's post https://www.discogs.com/forum/thread/757820
#
# prior to running this, first 
# - pip install beautifulsoup4
# - pip install releases
# - pip install lxml
# - adapt number of pages in range(1,#+1) where # is current number of styles / 44
#
# After running the script, delete the database so the styles will be filled into the table

import re
from bs4 import BeautifulSoup
import requests

data = ''
prefix = 'https://reference.discogslabs.com/browse/style?page='
for page in range(1,13+1):
    content = requests.get(prefix+str(page)).content # is type 'bytes'
    data += BeautifulSoup(content, 'lxml').decode() # is type 'string'
end_keys = [m.end() for m in re.finditer("\"title\":", data)]
start_quotes = [data.find('"',k) for k in end_keys]
end_quotes = [data.find('"',q+1) for q in start_quotes]
styles = [data[s+1:e] for s,e in zip(start_quotes,end_quotes)]
#styles = [bytes(s).decode('unicode_escape') for s in styles]
dupes = set([x for x in styles if styles.count(x) > 1])
styles = sorted(list(set(styles))) # remove dupes
n = 0
ignored = 0
with open('discogs_styles.txt', 'w') as f:
    for s in styles:
        if s[:9] != u'Browsing ':
            f.write(s.encode('UTF-8')+'\n')
            n += 1
print "Imported " + str(n) + " styles from discogs."
if len(dupes) > 0:
    print "The following duplicate styles where found and only imported once:"
    for d in dupes:
        if s[:9] != u'Browsing ':
            print " - " + d
