import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#ref 
#ssh slam15@openlab.ics.uci.edu
#to restart- python3 launch.py --restart
#to run - python3 launch.py



#class errors
class statusError(Exception):
    '''Error for when status code is not 200 indication that there was an error with page retrieval.'''
    "Status is not ok. Error in retrieving page."
    pass

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
   
    # Return empty list if error
    if resp.error:
        return []
    
    # If status is 200, try parsing webpage
    if resp.status == 200:
        # Return empty list if no data
        if resp.raw_response is None:
            return []

        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        hyperLinkLst = [l.get("href") for l in soup.find_all('a')]
        return hyperLinkLst

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        #need to search thru only these domains, use regex
        '''
        *.ics.uci.edu/*
        *.cs.uci.edu/*
        *.informatics.uci.edu/*
        *.stat.uci.edu/*
        '''

        parsed = urlparse(url)

        #url = 'HTTP://www.Python.org/doc/#'
        #returns 'http://www.Python.org/doc/

        if parsed.scheme not in set(["http", "https"]): 
            return False
        
        #find if parse's domain is one of the above. 
        #testing 
        print("netlock: ", parsed.netloc)


        #Testing: want to just test if we can match one page of ics and not a sub page
         
        if parsed.netloc == "ics.uci.edu" and parsed.path == "": #in ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]:
            print("match")
            return True
        
        
         #return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
