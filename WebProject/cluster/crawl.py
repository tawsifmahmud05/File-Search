from background_task import background
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time


from .forms import *

from tika import parser
import tika
tika.initVM()


def sendUrlformset(urllist):
    print(urllist)
    for newurl in urllist:
        global internal_urls
        internal_urls = set()
        global external_urls
        external_urls = set()
        global all
        all = set()

        crawl(newurl.url, int(newurl.depth))
        internal_urls.update(external_urls)
        all.update(internal_urls)
        if newurl.crawling_strategy == "PDF":
            for u in all:
                if u.endswith('.pdf'):
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"]
                        obj.filetype = "PDF"
                        obj.save()
                    except:
                        "No data found"


total_urls_visited = 0

# all = set()
# internal_urls = set()
# external_urls = set()


def is_valid(url):

    #Checks whether `url` is a valid URL.

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#Returns all URLs that is found on URL in which it belongs to the same website
def get_all_website_links(url):

    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                #print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
                # print(external_urls)
            continue
        print(href)
        urls.add(href)
        internal_urls.add(href)

    return urls

#Check crawling depth
def crawl(url, max_urls):

    global total_urls_visited
    total_urls_visited += 1
    #print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    all.update(links)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


def html_url(u):
    for u in all:
        if u.endswith('pdf'):
            print(u)


# def doc_url(d):
#     for d in all:
#         if d.endswith('doc') or d.endswith('docx'):
#             print(d)

@background(schedule=10)
def checkcluster():
    cluster_list = Cluster.objects.all().filter(crawled=False)
    for clus in cluster_list:
        clus.crawled = True
        urllist = Url.objects.all().filter(cluster=clus)
        sendUrlformset(urllist)
