require('source-map-support').install()

nconf = require('nconf')
async = require('async')

elasticsearch = require('elasticsearch')

nconf.argv()
     .env()
     .file({ file: '/etc/opt/risno.json' })
     .defaults({elastic_db: 'localhost:9200'})

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
    last_fetch_timestamp = Date.now()
    region = 'aquitaine'
    stop_after_page = 0
    do (site, region, last_fetch_timestamp) ->
      async.mapLimit [1..200], 2, (page, callback) ->
        if stop_after_page and page > stop_after_page
          console.log ' [X] cancel (stopping) page ' + page + ' of ' + site.name
          callback(null, null)
        else
          console.log ' [_] fetching page ' + page + ' of ' + site.name
          fetch.fetch_store_ads site, region, page, (err) ->
            #TODO add ads and replaced ads parameter
            #     1. if one of replaced ads is "younger"
            #     than last_fetch_timestamp, we suppose
            #     that we are starting to loop
            #     throug ads and we stop.
            #     2. or if there were no ads in the page
            #     we should also stop...
            #     to stop : stop_after_page=page
            if err
              console.log ' [*] error fetching page ' + page + ' of ' + site.name + err
            else
              console.log ' [x] fetched page ' + page + ' of ' + site.name
            callback(null, err)
      , (err, results) ->
          for fetch_err in results
            errors = true if fetch_err
          if errors
            console.log site.name + " errors while fetching site. Not updating last fetch date"
          else
            update_last_fetch site, region, last_fetch_timestamp, () ->
              console.log site.name + " fetched at " + last_fetch_timestamp

update_last_fetch = (site, region, last_fetch_timestamp, handler) ->
  client = new elasticsearch.Client
    host: nconf.get('elastic_db')
  client.index
    index: "utils"
    type: "fetch_info"
    body:
      site: site.name
      region: region
      last_fetch: last_fetch_timestamp
  .then () ->
    client.close()
    handler()
  .catch (err) ->
    console.log err
    client.close()
    handler()
