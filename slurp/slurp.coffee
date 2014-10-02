exports.url = (site, region, page_num) ->
  if site.region_id
    throw "Unknown region " + region unless site.region_id[region]
    region = site.region_id[region] if site.region_id
  replace = (format) ->
    format = format.replace /HOST/, site.host
    format = format.replace /REGION/, region
    format = format.replace /PAGE/, page_num

  if Array.isArray site.url_sequence
    replace format for format in site.url_sequence
  else
    [replace site.url_sequence]

exports.find_ads = (context, site) ->
  context.find(site.ads)

exports.parse_ad = (ad, site) ->
  site = {} unless site
  selectors = site.selectors || {}
  price = /[0-9]+[0-9 ]*/.exec(ad.find(selectors.price).text())
  price = price[0].replace /\s/g, '' if price

  description: strip ad.find(selectors.description).text()
  location: strip ad.find(selectors.location).text()
  price: price
  img: find_image ad, site.host
  url: find_url ad, site.host
  site_name: site.name

find_image = (ad, host) ->
  img = ad.find('img[original]')
  src = if img.length > 0 then img.attr('original') else ad.find('img').attr('src')

  if src
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

strip = (string) ->
  string.replace(/\s+/g, ' ').replace(/^\s/, '').replace(/\s$/, '')
 
crappy_pages_jaunes_url = (a) ->
  param = /\?idAnnonce=[^']*/.exec(a.attr('data-pjonglet'))
  'http://www.pagesjaunes.fr/verticales/immo/afficherFicheDetaillee.do' + param
