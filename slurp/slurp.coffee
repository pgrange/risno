exports.url = (params, region, page_num) ->
  if params.region_id
    throw "Unknown region " + region unless params.region_id[region]
    region = params.region_id[region] if params.region_id
  format = params.format
  format = format.replace /HOST/, params.host
  format = format.replace /REGION/, region
  format = format.replace /PAGE/, page_num
  format

exports.find_ads = (context, selector) ->
  context(selector)

exports.parse_ad = (ad, selectors, host) ->
  selectors = {} if ! selectors
  price = /[0-9]+[0-9 ]*/.exec(ad.find(selectors.price).text())
  price = price[0].replace /\s/g, '' if price

  description: ad.find(selectors.description).text()
  location: ad.find(selectors.location).text()
  price: price
  image: find_image ad, host
  url: find_url ad, host

find_image = (ad, host) ->
  img = ad.find('img[original]')
  src = if img.length > 0 then img.attr('original') else ad.find('img').attr('src')

  if /^http:/.test(src)
    src
  else
    'http://' + host + src
  
find_url = (ad, host) ->
  a = ad.find('a.idTag_PARTAGER')
  if a.length > 0
    crappy_pages_jaunes_url(a)
  else
    a = ad.find('.link-wrapper') #avendrealouer specific
    href = if a.length > 0 then a.attr('href') else ad.parent('a').attr('href')

    if /^http:/.test(href)
      href
    else
      'http://' + host + href
 
crappy_pages_jaunes_url = (a) ->
  param = /\?idAnnonce=[^']*/.exec(a.attr('data-pjonglet'))
  'http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do' + param