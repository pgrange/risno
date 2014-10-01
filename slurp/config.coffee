require('source-map-support').install()

path = require('path')
express = require('express')

fetch = require('./fetch')

config = {}

app = express()
app.use express.bodyParser()
app.use express.static(path.join(__dirname, 'public'))
app.use express.logger()

app.get '/', (req, res) ->
  res.render 'index.jade', sites: config

#TODO Filter requests so that we are not polluted by
#     css, images and js needed by the navigator for
#     the fetched page.
#
app.get '/:site', (req, res) ->
  res.render 'config.jade',
    site: config[req.param('site')]
    site_id: req.param('site')

app.get '/remote/:site', (req, res) ->
  site = clone_site config[req.param('site')]
  site.url_sequence = req.param('url_sequence').split('\n')
  console.log(site.url_sequence)

  fetch.fetch_page site, 'aquitaine', 2, (error, statusCode, body) ->
    res.send error if error
    res.send 'invalid HTTP status code: ' + statusCode if statusCode != 200
    res.send(body)

app.post '/save/:site', (req, res) ->
  site_id = req.param('site')
  site = config[site_id]
  site.url_sequence = req.param('url_sequence').split('\n')
  site.ads = req.param('ad_selector')
  site.selectors.price = req.param('price_selector')
  site.selectors.description = req.param('description selector')
  site.selectors.location = req.param('location_selector')

  save_config config, () ->
    console.log 'new configuration saved: ' + config
    res.redirect '/' + site_id

read_config = (handler) ->
  fs = require('fs')
  file = __dirname + '/config.json'

  fs.readFile file, 'utf8', (err, data) ->
    throw err if err
    handler JSON.parse(data)

save_config = (config, handler) ->
  fs = require('fs')
  file = __dirname + '/config.json'

  fs.writeFile file, JSON.stringify(config, null, 2), (err) ->
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
  selectors:
    price: site.price
    location: site.location
    description: site.description
