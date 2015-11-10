require('source-map-support').install()

nodeunit = require('nodeunit')

fetch = require('./fetch')

exports.fetching = nodeunit.testCase
  setUp: (end_of_setup) ->
    fake_http_client()
    end_of_setup()

  tearDown: (end_of_teardown) ->
    restore_http_client()
    end_of_teardown()

  testShouldFetchAllPubs: (test) ->
    fetch.fetch_ads site, 'aquitaine', 2, (error, status, ads) ->
      test.equal 4, ads.length
      test.done()

  testShouldTransmitStatusCode: (test) ->
    fetch.fetch_ads site, 'error_500', 2, (error, status, ads) ->
      test.equal 500, status
      test.done()

  testShouldSetAdIdFromImageHash: (test) ->
    fetch.fetch_ads site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('1'), ads[0].id
      test.done()

  testShouldDeduceIdFromDescriptionWhenNoImage: (test) ->
    fetch.fetch_ads site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('ad 2'), ads[1].id
      test.done()

  testShouldDeduceIdFromDescriptionWhenErrorWhileTryingToFetchImage: (test) ->
    fetch.fetch_ads site, 'aquitaine', 2, (error, status, ads) ->
      test.equal hash('ad 3'), ads[2].id
      test.done()

exports.storing = nodeunit.testCase
  setUp: (end_of_setup) ->
    fake_date_now()
    fake_http_client()
    setup_test_elastic_db (end_of_setup)

  tearDown: (done) ->
    restore_date_now()
    restore_http_client()
    teardown_test_elastic_db()
    done()

  testShouldFetchAndStoreAdsWithoutErrorsInNominalCase: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err, ads) ->
      test.equal null, err
      test.done()

  testShouldFetchAndStoreAdsInElasticDb: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err) ->
      assert_ad_in_db test, '1', (ad) ->
        test.equal "ad 1", ad.description
        test.equal "somwhere", ad.location
        test.equal 12043, ad.price
        test.equal "http://test.com/img1", ad.img
        test.equal "http://test.com/pub", ad.url
        test.equal site_name, ad.site_name
        test.equal site_host, ad.site_host

  testFetchAndStoreAdsShouldGiveListOfAdsToHandler: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err, ads) ->
      test.equal 4, ads.length
      test.done()

  testFetchAndStoreAdsShouldGiveOldValuesOfUpdatedAdsToHandler: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2,
      (err, ads, replaced_ads) ->
        test.equal 1, replaced_ads.length
        test.equal already_known_ad.description, replaced_ads[0]._source.description
        test.notEqual null, replaced_ads[0].fields._timestamp
        test.done()

  testFetchAndStoreAdsShouldSetFirstSeenDateTheFirstTimeAnAdIsSeen: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err, ads) ->
      assert_ad_in_db test, '1', (ad) ->
        test.notEqual null, ad.first_seen
        test.equal fake_now, ad.first_seen

  testFetchAndStoreAdsShouldNotSetFirstSeenDateIfItIsNotTheFirstTimeAnAdIsSeen: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err, ads) ->
      assert_ad_in_db test, already_known_ad.id, (ad) ->
        test.equal already_known_ad.first_seen, ad.first_seen

  # We used _timestamp to check for old ads in db.
  # However, _timestamp is updated to often (for instance
  # when location or type is updated).
  # We are going to use this explicit field instead.
  testFetchAndStoreAdsShouldSetLastSeenTimeToNow: (test) ->
    fetch.fetch_store_ads site, 'aquitaine', 2, (err, ads) ->
      assert_ad_in_db test, '1', (ad) ->
        test.equal fake_now, ad.last_seen


############
# Fixtures #
############

site_name = "test"
site_host = "test.com"
site =
  name: site_name
  host: site_host
  url_sequence: "http://HOST/REGION/PAGE"
  ads: "ad"
  selectors:
    price: "price"
    location: "location"
    description: "description"

fake_pages =
  'http://test.com/img1':
    statusCode: 200
    body: "1"
  'http://test.com/img4':
    statusCode: 200
    body: "4"
   'http://test.com/aquitaine/2':
    statusCode: 200
    body: """
<body>
  <a href="/pub">'
    <ad>
      <description>ad 1</description>
      <location>somwhere</location>"
      <price>12043</price>"
      <img src='http://test.com/img1'></img>
    </ad>
  </a>
  <a href="/pub">'
    <ad>
      <description>ad 2</description>
      <location>somwhere (no image)</location>"
      <price>12044</price>"
    </ad>
  </a>
  <a href="/pub">'
    <ad>
      <description>ad 3</description>
      <location>somwhere (bad image)</location>"
      <price>12045</price>"
      <img src='http://test.com/error_image'></img>
    </ad>
  </a>
  <a href="/pub">'
    <ad>
      <description>ad 4</description>
      <location>somwhere (already known)</location>"
      <price>12046</price>"
      <img src='http://test.com/img4'></img>
    </ad>
  </a>
</body>
"""

already_known_ad =
  id: '4'
  first_seen: "long time ago"
  description: "old description"
  location: "old location"
  price: 12046
  img: "http://test.com/img4"
  url: "http://test.com/pub"
  site_name: site_name
  site_host: site_host

#########
# Utils #
#########

request = require('request')
original_http_client = request.defaults
fake_http_client = () ->
  request.defaults = () ->
    (url, handler) ->
      response = fake_pages[url]
      response ?= {statusCode: 500, body: ''}
      handler null, response, response.body
restore_http_client = () ->
  request.defaults = original_http_client
 
original_now = Date.now()
fake_now = "right now !"
fake_date_now = () ->
  Date.now = () -> return fake_now
restore_date_now = () ->
  Date.now = original_now
 
elastic_client = null
elasticsearch = require('elasticsearch')
setup_test_elastic_db = (handler) ->
  nconf = require('nconf')
  nconf.defaults {elastic_db: 'localhost:9299'}
  elastic_client = new elasticsearch.Client
                   host: 'localhost:9299'
  elastic_client.indices.delete
    index: 'ads'
    refresh: true
  .finally () ->
    elastic_client.indices.create
      index: 'ads'
      body:
        mappings:
          immo:
            _timestamp:
              enabled: true
              store: true
      refresh: true
    .finally () ->
      elastic_client.index
        index: "ads"
        type: "immo"
        id: hash(already_known_ad.id)
        body: already_known_ad
      .finally () ->
         handler()
teardown_test_elastic_db = () ->
  elastic_client.close()

assert_ad_in_db = (test, ad_id, assertions) ->
  elastic_client.get
    index: 'ads'
    type: 'immo'
    id: hash(ad_id)
  .then (result) ->
    ad = result._source
    assertions ad
    test.done()
  .catch (err) ->
    test.fail "elastic request failed", err
    test.done()

hash = (value) ->
    md5 = require('crypto').createHash('md5')
    md5.update value
    md5.digest 'hex'
