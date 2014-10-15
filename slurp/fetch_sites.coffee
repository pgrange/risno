require('source-map-support').install()

async = require('async')

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
  for id, site of config
    do (site) ->
      async.mapLimit [1..200], 1, (page, callback) ->
        console.log ' [_] fetching page ' + page + ' of ' + site.name
        fetch.fetch_store_ads site, 'aquitaine', page, (err) ->
          if err
            console.log ' [*] error fetching page ' + page + ' of ' + site.name + err
          else
            console.log ' [x] fetched page ' + page + ' of ' + site.name
          callback()
      , (err, results) ->
        console.log 'done'
