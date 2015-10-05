# -*- coding: iso-8859-15 -*-

import os

from pyes import ES, MatchQuery, TermQuery, TextQuery, MatchAllQuery, FilteredQuery, BoolQuery, ESRange
from pyes.filters import MissingFilter, TermFilter, ORFilter, MatchAllFilter, RangeFilter
from datetime import datetime, timedelta

elastic_url=os.environ.get('ELASTIC_URL', '127.0.0.1:9200')
conn = ES(elastic_url) # Use HTTP
e_index = "ads_2.2"

log_context = ""
def log(status, message = ""):
  from colorama import Fore, Back, Style
  if status == "OK": color = Fore.GREEN
  elif status == "KO": color = Fore.RED
  else: color = Fore.YELLOW
 
  from datetime import datetime
  print color + status + " " + Fore.BLUE + log_context +  ' [' + str(datetime.now()) + ']' + Fore.RESET + " " + message.encode('UTF-8')

def check_index_version():
  q = TermQuery('dtc', 'dtc')
  conn.search(query=q, indices=e_index, doc_types="dtc").total

def insert_to_db(pub):
  conn.update(e_index, "immo", pub.get_id(), document=pub, upsert=pub)

def get_to_expire_pubs(last_fetch):
  q = FilteredQuery(MatchAllQuery(), MissingFilter('expired'))
  q = FilteredQuery(q, RangeFilter(qrange=ESRange('_timestamp', to_value=last_fetch)))

  pubs = conn.search(query=q, indices=e_index, doc_types="immo")
  return pubs

def show_pub(pub):
  print pub

def expired_before_timestamp():
  twentyfour_hours_ago = int((datetime.now()-timedelta(days=1)).strftime("%s"))*1000
  return twentyfour_hours_ago
  #q = MatchQuery('site', site)
  #fetch_info = conn.search(query=q, indices='utils', doc_types="fetch_info", sort='last_fetch:desc')
  #if len(fetch_info) > 0: return fetch_info[0]['last_fetch']
  ##FIXME this is the future bug of 2038 january the 19th 3:14:7
  #return 21474836470

def expire(pub):
  pub['expired'] = True

if __name__ == '__main__':
  import traceback
  import argparse

  log_context = "expire"

  previous_total = -1
  total = 0
  while previous_total != total:
    # That's odd but it seems we do not update all
    # found pubs... so adding this while loop :(
    previous_total = total

    pubs = get_to_expire_pubs(expired_before_timestamp())

    count = 0
    expired = 0
    total = pubs.total
    log('OK', str(total) + ' pubs to expire')
    for pub in pubs:
      expire(pub)
      expired = expired + 1
      insert_to_db(pub)
      count = count + 1
      if count % 20 == 0:
        log('OK', str(count) + ' / ' + str(total) + ' updated')
  log('OK', str(expired) + ' pubs expired')
