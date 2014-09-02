require('source-map-support').install()

cheerio = require('cheerio')

exports.testShouldFindAllAds = (test) ->
  dom = cheerio.load '<ad></ad><ad></ad>'

  ads = find_ads dom, 'ad'

  test.equal ads.length, 2
  test.done()

exports.testShouldParseAdDescription = (test) ->
  ad_dom = cheerio.load '<description>Description</description>'

  ad = parse_ad ad_dom, description: 'description'

  test.equals ad.description, 'Description'
  test.done()

exports.testShouldParseAdLocation = (test) ->
  ad_dom = cheerio.load '<location>Location</location>'

  ad = parse_ad ad_dom, location: 'location'

  test.equals ad.location, 'Location'
  test.done()

exports.testShouldParseAdPrice = (test) ->
  ad_dom = cheerio.load '<price>12043</price>'

  ad = parse_ad ad_dom, price: 'price'

  test.equals ad.price, 12043
  test.done()

exports.testShouldExtractPriceFromCrap = (test) ->
  ad_dom = cheerio.load '<price>This house costs only 12 043 595euro</price>'

  ad = parse_ad ad_dom, price: 'price'

  test.equals ad.price, 12043595
  test.done()

find_ads = (context, selector) ->
  context(selector)

parse_ad = (ad, selectors) ->
  price = /[0-9]+[0-9 ]*/.exec(ad(selectors.price).text())
  price = price[0].replace /\s/g, '' if price

  description: ad(selectors.description).text()
  location: ad(selectors.location).text()
  price: price
