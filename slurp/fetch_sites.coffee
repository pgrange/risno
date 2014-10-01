require('source-map-support').install()

require('nconf').defaults({elastic_db: 'localhost:9299'})

fetch = require('./fetch')
if process.argv[2]
  config_file = process.argv[2]
else
  config_file = __dirname + '/config.json'

read_config = (handler) ->
  fs = require('fs')

  fs.readFile config_file, 'utf8', (err, data) ->
    throw err if err
    handler JSON.parse(data)

read_config (config) ->
  console.log config
  for page in [1..200]
    for id, site of config
      do (site, page) ->
        console.log ' [_] fetching page ' + page + ' of ' + site.name
        fetch.fetch_store_ads site, 'aquitaine', page, (err) ->
          console.log ' [x] fetched page ' + page + ' of ' + site.name
          console.log(err) if err

