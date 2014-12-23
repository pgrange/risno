require('source-map-support').install()

nodeunit = require('nodeunit')

nconf = require('nconf')
request = require('request')
elasticsearch = require('elasticsearch')

fetch = require('./fetch')
test_ads = [
    description: "ad 1"
    location: "somwhere"
    price: "12043"
    img: "img1"
  ,
    description: "ad 2"
    location: "somwhere"
    price: "12044"
  ,
    description: "ad 3"
    location: "somwhere"
    price: "12045"
    img: "error_image"
]

test_site =
  name: "test"
  host: "test.com"
  url_sequence: "http://HOST/REGION/PAGE"
  ads: "ad"
  selectors:
    price: "price"
    location: "location"
    description: "description"

fake_ads_page = () ->
  response = "<body>"
  for ad in test_ads
    response = response + 
      '<a href="/pub">' +
        "<ad>" +
          "<description>" + ad.description + "</description>" +
          "<location>" + ad.location + "</location>" +
          "<price>" + ad.price + "</price>" +
          ("<img src='http://test.com/" + ad.img + "'></img>" if ad.img) +
        "</ad>" +
      "</a>"
  response + "</body>"

fake_pages =
  'http://test.com/aquitaine/2':
    statusCode: 200
    body: fake_ads_page()
  'http://test.com/img1':
    statusCode: 200
    body: "1" #c4ca4238a0b923820dcc509a6f75849b

hash = (value) ->
    md5 = require('crypto').createHash('md5')
    md5.update value
    md5.digest 'hex' 


original_http_client = request.defaults
restore_http_client = () ->
  request.defaults = original_http_client
test_http_client = (client) ->
  request.defaults = () ->
    client
test_http_response = (body, status) ->
  test_http_client (url, handler) ->
    handler null, {statusCode: status ? 200}, body
   
exports.fetching = nodeunit.testCase
  setUp: (done) ->
    test_http_client (url, handler) ->
      response = fake_pages[url]
      response ?= {statusCode: 500, body: ''}
      handler null, response, response.body
    
    nconf.defaults {elastic_db: 'localhost:9299'}
    this.elastic_client = new elasticsearch.Client
                      host: 'localhost:9299'
    do (elastic_client = this.elastic_client) ->
      elastic_client.indices.delete
        index: 'ads'
        refresh: true
      .finally () ->
        elastic_client.indices.create
          index: 'ads'
          refresh: true
        .finally () ->
          done()
  tearDown: (done) ->
    restore_http_client()
    this.elastic_client.close()
    done()

  testShouldFetchAllPubs: (test) ->
    fetch.fetch_ads test_site, 'aquitaine', 2, (error, status, ads) ->
      test.equal 3, ads.length
      test.done()

  testShouldTransmitStatusCode: (test) ->
    fetch.fetch_ads test_site, 'error_500', 2, (error, status, ads) ->
      test.equal 500, status
      test.done()

  testShouldSetAdIdFromImageHash: (test) ->
    fetch.fetch_ads test_site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('1'), ads[0].id
      test.done()

  testShouldDeduceIdFromDescriptionWhenNoImage: (test) ->
    fetch.fetch_ads test_site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('ad 2'), ads[1].id
      test.done()

  testShouldDeduceIdFromDescriptionWhenErrorWhileTryingToFetchImage: (test) ->
    fetch.fetch_ads test_site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('ad 3'), ads[2].id
      test.done()

  testShouldFetchAndStoreAdsInElasticDb: (test) ->
    elastic_client = this.elastic_client
    fetch.fetch_store_ads test_site, 'aquitaine', 2, (err) ->
      test.equal null, err
      elastic_client.get
        index: 'ads'
        type: 'immo'
        id: hash('1')
      .then (result) ->
        ad = result._source
        test.equal "ad 1", ad.description
        test.equal "somwhere", ad.location
        test.equal 12043, ad.price
        test.equal "http://test.com/img1", ad.img
        test.equal "http://test.com/pub", ad.url
        test.equal "test", ad.site_name
        test.done()
      .catch (err) ->
        test.fail "elastic request failed", err
        test.done()
 
  testFetchAndStoreAdsShouldGiveListOfAdsToHandler: (test) ->
    fetch.fetch_store_ads test_site, 'aquitaine', 2, (err, ads) ->
      test.equal null, err
      test.equal 3, ads.length
      test.done()

  testFetchAndStoreAdsShouldGiveOldValuesOfUpdatedAdsToHandler: (test) ->
    this.elastic_client.index
      index: "ads"
      type: "immo"
      id: hash("1")
      body:
        description: "old description"
        localtion: "old location"
        price: 12043
        img: "http://test.com/img1"
        url: "http://test.com/pub"
        site_name: "test"
    .then () ->
      fetch.fetch_store_ads test_site, 'aquitaine', 2,
        (err, ads, replaced_ads) ->
          test.equal null, err
          test.equal 1, replaced_ads.length
          test.equal "old description", replaced_ads[0].description
          test.done()
    .catch (err) ->
      test.fail err
      test.done()
