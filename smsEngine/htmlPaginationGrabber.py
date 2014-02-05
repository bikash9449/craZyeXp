import requests
from bs4 import BeautifulSoup
import string
import re
import urlparse
import pickle
from sms import getSmsHandaler

DEBUG = False

# Help Function for Save and Restore WebSite Data ########
def save_site_data(url,data):
  file_name =  urlparse.urlparse(url).netloc+'.pkl'
  pickle.dump( data, open( file_name, "wb" ))

def load_site_data(url):
  file_name =  urlparse.urlparse(url).netloc+'.pkl'
  try:
    return pickle.load( open( file_name, "rb" ) )
  except:
    print 'No store data found for '+file_name
    return None

# Helper Function for makeing clean HTML data
def clean_text(s):
  """ Helper function remove all \n \t \r etc"""
  return re.sub( '[\n\t\r\s]+', ' ', s ).strip()


# HElper function for multiple way of site grabbing

def getHTMLMenuContent(first_url,max_menu=100):
  """
  This code return the list of menu or cetegories url.
  For example for a sms site it will return a base link of each categories.
  """
  cat_url_list = []
  if DEBUG: print '>>> Reading '+first_url+'...'
  resp = requests.get(first_url)
  html = resp.text
  soup = BeautifulSoup(html)
  
  # Get list of Contents
  for a in soup.find('ul',{'class':'menu'}).find_all('a'):
    cat_url_list.append((clean_text(a.text),a['href']))
  return cat_url_list


def getHTMLPaginationContent(first_url,max_count=99999):
  """
  The Logrithm is so smple like this.
  1. Take the first url as input
  2. we make a msg_list aas global.
  while( tehere is no next url)
  {
    1.Grap the site and pupulate global list
    2.Parse pagination and find next url if exist
  }
  """
  msg_list=[]
  cur_count =0;
  while(first_url):
    if DEBUG: print '>>> Reading '+first_url+'...'
    resp = requests.get(first_url)
    html = resp.text
    soup = BeautifulSoup(html)
    ######## Step1: Dig the Content and Populate the list ###
    content = soup.find('div',{'class':'blog'}).find_all('div',{'class':'article_column'})
    for c in content:
      msg_list.append(c.find_all('p')[1].text)
      cur_count +=1
      if cur_count == max_count:
        return msg_list
    
    ######## Step 2: Find The next Page in the pagination ####
    page = soup.find('ul',{'class':'pagination'})
    next_page = None
    for a in page.find_all('a'):
      if a.text =='Next':
        next_page = a['href']
    first_url = next_page
  return msg_list

def grabFullSite(base_url,use_cache=True):
  #Check for cache..
  if use_cache:
    if DEBUG: print '>>> Checking for cache...'
    data = load_site_data(base_url)
    if data:
      if DEBUG: print '>>> data Found in cache, Skip grabbing...'
      if DEBUG: print '>>> Total Content Count::'+str(sum([len(i) for i in data.values()]))
      return data
  if DEBUG: print '\n>>> Cache Not found hence grading'
  
  if DEBUG: print '\n>>> getting categorie list'
  cat_list = getHTMLMenuContent(base_url)
  
  data ={}
  for name,url in cat_list:
    if DEBUG: print '\n>>> Start processing categories:'+name
    data[name] = getHTMLPaginationContent(url)
    if DEBUG: print '>>> End processing categories:'+name
    if DEBUG: print '>>> Total Numbe of message is found:'+str(len(data[name]))
    

  if DEBUG: print '>>> Storing in cache Fefore Return'  
  save_site_data(base_url,data)
  if DEBUG: print '>>> Site Grab completed\n>>> Total Content Count::'+str(sum([len(i) for i in data.values()]))
  return data
  

def smsSendSchedular(to_list,sms_list,interval_in_sec=3600,randamize=True,default_service = "160by2"):
  " A mini Schedulr for sending sms"
  print ">>> You have Schedule %d number of sms  to the number %s in the interval of %d second " %(len(sms_list),to_list,interval_in_sec) 
  raw_input(">>> Please press ENTER type to Confirm.")
  import time
  import random
  from ConfigParser import ConfigParser
  import way2sms
  import one6tiby2
  
  if randamize: random.shuffle(sms_list)

  config = ConfigParser()
  config.read("../config.ini")
  username = config.get(default_service, "uname")
  password = config.get(default_service, "password")
  
  for sms in sms_list:
    try:
      handler = getSmsHandaler(username,password,default_service)
      for to in to_list:
        handler.do(to,sms)
    except Exception,e:
      print 'OOPS.. Msg not send some error',str(e)
    time.sleep(interval_in_sec)
  
  
  
### Sample Test ###
def activate():
  SITE_URL = 'http://g10sms.com/sms140/'
  data = grabFullSite(SITE_URL)
  print '>>> Hello, we support following SMS type:'
  for key in data.keys():
    print '%s(%d) ' %(key, len(data[key])) ,
  x = raw_input("\n>>> Please press type which SMS you want to subscribe:")
  smsSendSchedular(['8880428779'],sms_list = data[x],interval_in_sec = 1800,default_service="way2sms")

activate()
