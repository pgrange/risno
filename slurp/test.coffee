require('source-map-support').install()

cheerio = require('cheerio')

slurp = require('./slurp')

exports.testShouldFindAllAds = (test) ->
  dom = cheerio.load '<ad></ad><ad></ad>'

  ads = slurp.find_ads dom, 'ad'

  test.equal ads.length, 2
  test.done()

exports.testShouldParseAdDescription = (test) ->
  ad = parse_ad_from_src '<description>Description</description>'

  test.equals ad.description, 'Description'
  test.done()

exports.testShouldParseAdLocation = (test) ->
  ad = parse_ad_from_src '<location>Location</location>'

  test.equals ad.location, 'Location'
  test.done()

exports.testShouldParseAdPrice = (test) ->
  ad = parse_ad_from_src '<price>12043</price>'

  test.equals ad.price, 12043
  test.done()

exports.testShouldExtractPriceFromCrap = (test) ->
  ad = parse_ad_from_src '<price>only 12 043 595euro</price>'

  test.equals ad.price, 12043595
  test.done()

exports.testShouldNotFailIfSelectorsAreMissing = (test) ->
  ad= cheerio.load('<ad></ad>')('ad')
 
  slurp.parse_ad ad
  
  test.done()

exports.testShouldParseAdImage = (test) ->
  ad = parse_ad_from_src '<img src="http://site/image"></img>'

  test.equals ad.image, 'http://site/image'
  test.done()

exports.testShouldExtractImageWithOriginalAttributeIfAny = (test) ->
  ad = parse_ad_from_src '<img src="http://no"></img><img original="http://site/image"></img>'

  test.equals ad.image, 'http://site/image'
  test.done()

exports.testShouldConvertImageRelativeURIToAbsolute = (test) ->
  ad = parse_ad_from_src '<img src="/image"></img>'

  test.equals ad.image, 'http://site/image'
  test.done()

exports.testShouldParseAdUrl = (test) ->
  dom = cheerio.load('<a href="http://site/ad"><ad></ad></a>')

  ad = slurp.parse_ad dom('ad')

  test.equals ad.url, 'http://site/ad'
  test.done()

exports.testShouldExtractUrlFromStrangeAVendreALouerMethod = (test) ->
  ad = parse_ad_from_src '<a class="link-wrapper" href="/ad"></a>'

  test.equals ad.url, 'http://site/ad'
  test.done()

exports.testShouldExtractUrlFromStrangePagesJaunesMethod = (test) ->
  ad = parse_ad_from_src '<a href="#null" class=" idTag_PARTAGER" data-pjonglet="{cont:\'blocTools949ca309-4e4f-e311-9ab4-5cf3fc6a23ca\',ong:\'tab02\',ajax:\'http://www.pagesjaunes.fr/verticales/immo/partagerAnnonceLR.do?idAnnonce=2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca\',reload:1}">Partager</a>'

  test.equals ad.url, 'http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do?idAnnonce=2d7ff5b1-1165-e211-86f2-5cf3fc6a23ca'
  test.done()

parse_ad_from_src = (src) ->
  ad = cheerio.load('<ad>' + src + '</ad>')('ad')
  slurp.parse_ad ad, 
    price: 'price'
    location: 'location'
    description: 'description',
    'site'
