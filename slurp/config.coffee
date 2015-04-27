require('source-map-support').install()

path = require('path')
express = require('express')
body_parser = require('body-parser')
morgan = require('morgan')

fetch = require('./fetch')

config = {}
if process.argv[2]
  config_file = process.argv[2]
else
  config_file = __dirname + '/config.json'

app = express()
app.use body_parser.urlencoded({extended: false})
app.use express.static(path.join(__dirname, 'public'))
app.use morgan('combined')

app.get '/', (req, res) ->
  res.render 'index.jade', sites: config

# TODO is there a way to merge params, query and body
#      with new version of express, instead of searching
#      in every possible places ;( ?
#
# TODO Filter requests so that we are not polluted by
#      css, images and js needed by the navigator for
#      the fetched page.
#
app.get '/:site', (req, res) ->
  res.render 'config.jade',
    site: config[req.params.site]
    site_id: req.params.site

app.get '/remote/:site', (req, res) ->
  site = clone_site config[req.params.site]
  site.url_sequence = req.query.url_sequence.split('\n')
  page_number = req.query.page_number or 2
  console.log(site.url_sequence)
  console.log(page_number)

  fetch.fetch_page site, 'aquitaine', page_number, (error, statusCode, body) ->
    res.send error if error
    res.send 'invalid HTTP status code: ' + statusCode if statusCode != 200
    res.send(body)

app.post '/save/:site', (req, res) ->
  site_id = req.params.site
  site = config[site_id]
  site.url_sequence = req.body.url_sequence.split('\n')
  site.ads = req.body.ad_selector
  site.selectors.price = req.body.price_selector
  site.selectors.description = req.body.description_selector
  site.selectors.location = req.body.location_selector

  save_config config, () ->
    console.log 'new configuration saved: ' + config
    res.redirect '/' + site_id

read_config = (handler) ->
  fs = require('fs')

  fs.readFile config_file, 'utf8', (err, data) ->
    throw err if err
    handler JSON.parse(data)

save_config = (config, handler) ->
  fs = require('fs')

  fs.writeFile config_file, JSON.stringify(config, null, 2), (err) ->
    throw err if err
    handler()

read_config (config_from_file) ->
  config = config_from_file
  console.log config
  app.listen 12045
  console.log 'configuration tool ready'
  console.log 'connect to http://localhost:12045'

clone_site = (site) ->
  name: site.name
  host: site.host
  url_sequence: site.url_sequence
  ads: site.ads
  region_id: site.region_id
  selectors:
    price: site.price
    location: site.location
    description: site.description
