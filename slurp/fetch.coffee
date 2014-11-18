require('source-map-support').install()

require('iconv-lite').extendNodeEncodings()

request = require('request')
cheerio = require('cheerio')
async = require('async')
crypto = require('crypto')

nconf = require('nconf')
elasticsearch = require('elasticsearch')
slurp = require('./slurp')

fetch_page = (client, sequence, handler) ->
  next = sequence.shift()
  client next, (error, response, body) ->
    if error
      console.log('error: ' + error)
      handler error
    else if response.statusCode != 200
      handler undefined, response.statusCode, body
    else if sequence.length
      fetch_page(client, sequence, handler)
    else
      handler(undefined, response.statusCode, body)
  

set_id = (ad, handler) ->
  hash = (value) ->
    md5 = crypto.createHash('md5')
    md5.update value
    md5.digest 'hex'
  set_id_from_description = (ad) ->
    ad.id = hash ad.description
    ad

  if not ad.img
    handler null, set_id_from_description(ad)
  else
    client = request.defaults({forever: true})
    client ad.img, (err, response, body) ->
      if err or response.statusCode != 200
        console.log('err: ' + err) if err
        console.log('http status code: ' + response.statusCode) if response
        handler null, set_id_from_description(ad)
      else
        ad.id = hash body
        handler null, ad

exports.fetch_ads = (site, region, page, handler) ->
  exports.fetch_page site, region, page, (error, statusCode, body) ->
    if error
      handler error
    else if statusCode != 200
      handler null, statusCode
    else
      page = cheerio.load(body)
      ads = slurp.find_ads page('body'), site
      parsed_ads = (slurp.parse_ad page(ad), site for ad in ads)

      async.mapLimit parsed_ads, 1, set_id, (err, parsed_ads) ->
        handler null, statusCode, parsed_ads

exports.fetch_page = (site, region, page, handler) ->
  url = slurp.url site, region, page

  if site.force_encoding
    client = request.defaults({forever: true, jar: true, encoding: site.force_encoding})
  else
    client = request.defaults({forever: true, jar: true})

  fetch_page client, url, handler

exports.fetch_store_ads = (site, region, page, handler) ->
  exports.fetch_ads site, region, page, (err, statusCode, ads) ->
    if not ads
      handler 'Unable to fetch ads: ' + err + statusCode unless ads
    else
      pool.acquire (err, elastic_client) ->
        insert_ad = (ad, handler) ->
          elastic_client.index
            index: "ads"
            type: "immo"
            id: ad.id
            body: ad
          .then () -> handler()
          .catch (err) -> handler err

        async.map ads, insert_ad, (err) ->
          pool.release(elastic_client)
          handler err

poolModule = require('generic-pool')
pool = poolModule.Pool
  name     : 'elasticsearch',
  create   : (callback) ->
    elastic_client = new elasticsearch.Client
      host: nconf.get('elastic_db')
      maxSockets: 1
    callback(null, elastic_client)
  destroy  : (client) ->
    client.close()
  max      : 1,
  #specifies how long a resource can stay idle in pool before being removed
  idleTimeoutMillis : 10000,
