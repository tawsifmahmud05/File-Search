
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
from typing import Reversible
from django.db.models import query
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import json
from .forms import *
from .models import *

import threading

import mimetypes

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from time import time, sleep

from tika import parser
import tika
tika.initVM()

# api
apiurl = "http://127.0.0.1:8000/api/file?format=json&"

json_list = {}


# Check user logged in or not
def indexView(request):
    if request.user.is_authenticated:
        return redirect('cluster:cluster')
    else:
        return render(request, 'login.html')


# Create cluster with urls

def create_cluster_with_urls(request):
    user = request.user
    template_name = 'addcluster.html'
    if request.method == 'GET':
        clusterform = ClusterModelForm(request.GET or None)
        urlformset = UrlFormset(queryset=Url.objects.none())
    elif request.method == 'POST':
        clusterform = ClusterModelForm(request.POST)
        urlformset = UrlFormset(request.POST)
        if clusterform.is_valid() and urlformset.is_valid():

            obj = clusterform.save(commit=False)
            obj.owner = request.user
            obj.crawled = False
            obj.save()
            for form in urlformset:

                newurl = form.save(commit=False)
                newurl.cluster = obj
                newurl.save()
            # checkcluster(user)
            t1 = threading.Thread(target=checkcluster, args=(user,))
            t1.start()
            return redirect('cluster:cluster')
    return render(request, template_name, {
        'clusterform': clusterform,
        'urlformset': urlformset,
    })


def download(request):
    df = pd.DataFrame(json_list)
    print(df)

# search page


def searchPageView(request):
    searchform = SearchForm(user=request.user)
    if request.method == 'GET':
        searchform = SearchForm(request.GET, user=request.user)
        if searchform.is_valid():
            keyword = searchform.cleaned_data.get("keyword")
            cluster = searchform.cleaned_data.get("usercluster")
            headers = {
                'Authorization': 'Token e697bea2c349db8c61a55accf6c0546db5de0dd8'}
            url = apiurl+"search=" + keyword + "&filecluster="+str(cluster.id)
            response = requests.get(url, headers=headers).json()
            diction = response
            json_list = response
            df = pd.DataFrame(json_list)
            print(df)
            text_list = []
            list = []
            for i in range(len(diction)):
                text = diction[i]['content']
                text_list.append(abbreviate(text, 150))
                # print(diction)
                # list = diction[i]['content'].split()
                # for j in range(len(list)):
                #     if list[j].lower() == keyword.lower():
                #         text_list.append('.......... '+list[j-3] + " " + list[j-2] + " " + list[j-1] + " " +
                #                          list[j] + " " + list[j+1] + " " + list[j+2] + " " + list[j+3] + " ..........")
                #         print('.......... '+list[j-3] + " " + list[j-2] + " " + list[j-1] + " " +
                #               list[j] + " " + list[j+1] + " " + list[j+2] + " " + list[j+3] + " ..........")
                #         break
            try:
                for i in range(len(diction)):
                    # try:Nat
                    diction[i]['content'] = text_list[i]
                    print(diction[i]['content'])

            except:
                print("Error")
            return render(request, 'search.html', {'searchform': searchform, 'file_list': diction, 'keyword': keyword, 'text_list': text_list})
    return render(request, 'search.html', {'searchform': searchform, })

# cluster page


def cluster_list(request):
    cluster_list = Cluster.objects.all().filter(owner=request.user)
    diction = {'title': 'Cluster', 'cluster_list': cluster_list}
    return render(request, 'cluster.html', context=diction)


def abbreviate(text, max):
    if(len(text) > max):
        text = text[0:max] + "......."
    return text


# Check crawling strategy


def sendUrlformset(urllist):
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
                    print(u)
                    try:
                        Fileform = FileModelForm()

                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "PDF"
                        obj.save()
                    except:
                        print("No data found")

        elif newurl.crawling_strategy == "DOC":
            for u in all:
                if u.endswith('.doc') or u.endswith('.docx'):
                    print(u)
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "DOC"
                        obj.save()
                    except:
                        print("No data found")

        elif newurl.crawling_strategy == "HTML":
            for u in all:
                if u.endswith('.html'):
                    print(u)
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "HTML"
                        obj.save()
                    except:
                        print("No data found")

        elif newurl.crawling_strategy == "PPT":
            for u in all:
                if u.endswith('.ppt') or u.endswith('.pptx'):
                    print(u)
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "PPT"
                        obj.save()
                    except:
                        print("No data found")

        elif newurl.crawling_strategy == "NON-HTML":
            for u in all:
                if u.endswith('.doc') or u.endswith('.ppt') or u.endswith('.pdf') or u.endswith('.docx') or u.endswith('.pptx'):
                    print(u)
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "NON-HTML"
                        obj.save()
                    except:
                        print("No data found")

        elif newurl.crawling_strategy == "ALL":
            for u in all:
                if u.endswith('.doc') or u.endswith('.ppt') or u.endswith('.html') or u.endswith('.pdf') or u.endswith('.docx') or u.endswith('.pptx'):
                    print(u)
                    try:
                        Fileform = FileModelForm()
                        obj = Fileform.save(commit=False)
                        obj.fileurl = u
                        obj.filecluster = str(newurl.cluster.id)
                        obj.mainurl = str(newurl.id)
                        parsed = parser.from_file(u)
                        obj.content = parsed["content"].replace("\n", " ")
                        obj.filetype = "ALL"
                        obj.save()
                    except:
                        print("No data found")

        else:
            print("NOT VALID")


total_urls_visited = 0


def is_valid(url):

    # Checks whether 'url' is a valid URL.

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# get all website link


def get_all_website_links(url):

    # Returns all URLs that is found on 'url' in which it belongs to the same website

    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    try:
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
                    # print(f"{GRAY}[!] External link: {href}{RESET}")
                    external_urls.add(href)
                    # print(external_urls)
                continue
            # print(href)
            urls.add(href)
            internal_urls.add(href)
    except:
        print('connection error')

    return urls

# Print all link


def crawl(url, max_urls):

    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    all.update(links)
    print(all)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


# def html_url(u):
#     for u in all:
#         if u.endswith('pdf'):
#             print(u)


def checkcluster(requ):
    cluster_list = Cluster.objects.all().filter(crawled=False).filter(owner=requ)
    for clus in cluster_list:
        urllist = Url.objects.all().filter(cluster=clus)
        sendUrlformset(urllist)
        user = requ
        clus.crawled = True
        clus.save()
        sendemail(user, clus)

        # subject = 'About Your Cluster'
        # message = f'Hi {user}, Your cluster is ready. You can search now.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user]
        # send_mail( subject, message, email_from, recipient_list )

# constant check cluster


# def loop():
#     while True:
#         checkcluster()
#         print("no cluster to crawl")


# t1 = threading.Thread(target=loop)
# t1.start()


# Sending email to owner

def sendemail(user, cluster):
    subject = 'About Your Cluster'
    message = f'Hi {user.username},\n\nYour cluster "{cluster.name}" is ready to use and waiting for you.\nEnjoy your searching with FileBook.\n\n\nBest of luck!\n- FileBook Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
