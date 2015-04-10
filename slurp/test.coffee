require('source-map-support').install()

cheerio = require('cheerio')

slurp = require('./slurp')

#Find ads in page

exports.testShouldFindAllAds = (test) ->
  dom = cheerio.load '<body><ad></ad><ad></ad></body>'

  ads = slurp.find_ads dom('body'), ads: 'ad'

  test.equal ads.length, 2
  test.done()

#Parse ad

exports.testShouldParseAdDescription = (test) ->
  ad = parse_ad_from_src '<description>Description</description>'

  test.equals ad.description, 'Description'
  test.done()

exports.testShouldStripAdDescription = (test) ->
  ad = parse_ad_from_src '<description>\n                                    \n                                            \n                                        \n                                        \n                                        \n                                            Talence\n                                            \n                                                /\n                                            \n                                        \n                                        Gironde\n                                    \n                                </description>'

  test.equals ad.description, 'Talence / Gironde'
  test.done()

exports.testShouldStripAdLocation = (test) ->
  ad = parse_ad_from_src '<location>\n                                    \n                                            \n                                        \n                                        \n                                        \n                                            Talence\n                                            \n                                                /\n                                            \n                                        \n                                        Gironde\n                                    \n                                </location>'

  test.equals ad.location, 'Talence / Gironde'
  test.done()

exports.testShouldParseAdLocation = (test) ->
  ad = parse_ad_from_src '<location>Location</location>'

  test.equals ad.location, 'Location'
  test.done()

exports.testShouldParseAdPrice = (test) ->
  ad = parse_ad_from_src '<price>12043</price>'

  test.strictEqual ad.price, 12043
  test.done()

exports.testShouldExtractPriceFromCrap = (test) ->
  ad = parse_ad_from_src '<price>only 12 043 595euro</price>'

  test.equals ad.price, 12043595
  test.done()

exports.testShouldExtractPriceFromUtterCrap = (test) ->
  ad = parse_ad_from_src '<price>126&#160;900  € </price>'

  test.equals ad.price, 126900
  test.done()

exports.testShouldNotFailIfSelectorsAreMissing = (test) ->
  ad= cheerio.load('<ad></ad>')('ad')
 
  slurp.parse_ad ad
  
  test.done()

exports.testShouldSetSiteNameInAds = (test) ->
  ad = parse_ad_from_src ''

  test.equals ad.site_name, 'test'
  test.done()

exports.testShouldParseAdImage = (test) ->
  ad = parse_ad_from_src '<img src="http://site/image"></img>'

  test.equals ad.img, 'http://site/image'
  test.done()

exports.testShouldExtractImageWithOriginalAttributeIfAny = (test) ->
  ad = parse_ad_from_src '<img src="http://no"></img><img original="http://site/image"></img>'

  test.equals ad.img, 'http://site/image'
  test.done()

exports.testShouldConvertImageRelativeURIToAbsolute = (test) ->
  ad = parse_ad_from_src '<img src="/image"></img>'

  test.equals ad.img, 'http://site/image'
  test.done()

exports.testShouldNotGuessImageIfNoneFound = (test) ->
  ad = parse_ad_from_src '<ad></ad>'

  test.equal undefined, ad.img
  test.done()


exports.testShouldParseAdUrl = (test) ->
  dom = cheerio.load('<a href="http://site/ad"><ad></ad></a>')

  ad = slurp.parse_ad dom('ad')

  test.equals ad.url, 'http://site/ad'
  test.done()

exports.testShouldParseAdUrlWhenLinkInside = (test) ->
  dom = cheerio.load('<ad><a href="http://site/ad"></a></ad>')

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

exports.testShouldExtractUrlFromParuVenduMethod = (test) ->
  ad = parse_ad_from_src '<li>
                            <a class="picCntr" href="#goFD">not this one</a>
                            <div class="details">
                              <a href="http://site/ad">this one !</a>
                            </div>
                            <a class="picCntr" href="#goFD">not this one</a>
                          </li>'

  test.equals ad.url, 'http://site/ad'
  test.done()

parse_ad_from_src = (src) ->
  ad = cheerio.load('<ad>' + src + '</ad>')('ad')
  slurp.parse_ad ad, 
    host: 'site'
    name: 'test'
    selectors: 
      price: 'price'
      location: 'location'
      description: 'description',

# Build fetch URL

exports.testForgeSimpleUrl = (test) ->
  url = slurp.url
    host: 'www.exemple.com'
    url_sequence: 'http://HOST/ads/REGION?p=PAGE',
    'aquitaine', 2

  test.deepEqual url, ['http://www.exemple.com/ads/aquitaine?p=2']
  test.done()

exports.testForgeUrlWithSiteSpecificRegionIds = (test) ->
  url = slurp.url
    host: 'www.exemple.com'
    url_sequence: 'http://HOST/ads/REGION?p=PAGE'
    region_id: {'aquitaine': '12043'},
    'aquitaine', 2

  test.deepEqual url, ['http://www.exemple.com/ads/12043?p=2']
  test.done()

exports.testShouldFailWhenUnableToConvertRegionToId = (test) ->
  test.throws ->
    slurp.url
      host: 'www.exemple.com'
      url_sequence: 'http://HOST/ads/REGION?p=PAGE'
      region_id: {'aquitain': '12043'},
      'aquitaine', 2

  test.done()

exports.testShouldReturnArrayOfUrlsWhenComplexScenario = (test) ->
  url = slurp.url
    host: 'www.exemple.com'
    url_sequence: [
      'http://HOST/ads/REGION',
      'http://HOST/ads/PAGE',
    ],
    'aquitaine', 2

  test.deepEqual url, [
    'http://www.exemple.com/ads/aquitaine',
    'http://www.exemple.com/ads/2',
  ]
  test.done()


