
import urllib2
from bs4 import BeautifulSoup

## Fetch's latest git commit for project
# @param: proj - str with project key
def fetch_git_commits(proj):
    
    url = "http://fgx.ch/projects/%s/repository/revisions.atom" % proj 
    response = urllib2.urlopen(url)
    html_doc = response.read()
    #print html_doc

    soup = BeautifulSoup(html_doc)
    entries =  soup.find_all("entry")
    #print entries
    
    lst = []
    for ent in entries:
        item = dict(title=ent.title.text, updated=ent.updated.text)
        lst.append(item)
        
    return lst
    #print "> ", ent.title
    
    
print fetch_git_commits("fgx-map")
