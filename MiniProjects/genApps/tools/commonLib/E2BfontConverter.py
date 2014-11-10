# -*- coding: utf-8 -*-
#####################################
#  E2B-FontConverter
#
######################################
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

##########################################
import requests
import pickle
import pdb


def recur_set(counts=3,lst='abc'):
  LIST = list(lst)
  all = LIST
  now = LIST
  import pdb
  
  for i in range(2,counts+1):
    print 'Calculating of length',i,'...'
    so = [ j+k for j in now for k in list(lst)]
    all += so
    now = so
  print len(all)
  #pdb.set_trace()
  return all
      
  
  
  

def grab_and_build_cache(trie_len=10):
  "Build an Cache and use this service for Offline "
  Map= {}
  COUNT = 4
  LIST = "abcdefghijklmnopqrstuvwxyz"
  #LIST = [ 'a','b','c','d','e','f','g' ]
  print '>>> Calculating all keys '  
  AllKey=recur_set(COUNT,LIST)
  print AllKey  
  for key in AllKey:
      r = requests.get("http://www.google.com/inputtools/request?text="+key+"&ime=transliteration_en_bn&num=5&cp=0&cs=0&ie=utf-8&oe=utf-8&app=jsapi")
      r = r.text      
      r = r.replace('true','True')
      r = r.replace('false','False')
      print r
      y = eval(r)
      Map[key]= y
  print Map
  pickle.dump( Map, open( LIST[0]+"-TO-"+LIST[-1]+"-LEN"+str(COUNT)+".pkl", "wb" ))
    
  
#############  Web server Operation here #######################

def load_cache():
  print 'loading cache...'
  cache = pickle.load ( open( "a2z-len5.pkl", "rb" ))
  return cache

global cache
cache = load_cache()


import flask
from flask import Flask,request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@crossdomain(origin='*') # <<< This for cross domain support 
def converts():
    if request.method == 'GET':
      #pdb.set_trace()
      q = request.args.get('q', '')
      if not q: return "Use /?q=abc "      
      #cache = load_cache()
      ll = cache.get(q)
      f = {'status': ll[0],'input': ll[1][0][0] ,'output': ll[1][0][1]}
      return flask.jsonify(**f)
############ End of server ###########
    
# tesing ..
#grab_and_build_cache()

#server
app.run(host='0.0.0.0')
