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
    found_duplicate_on_page = []
    do (site, region, last_fetch_timestamp, stop_after_page) ->
      async.mapLimit [1..3000], 2, (page, callback) ->
        if stop_after_page and page > stop_after_page
          callback(null, null)
        else
          console.log ' [_] fetching page ' + page + ' of ' + site.name
          fetch.fetch_store_ads site, region, page, (err, ads, old_ads) ->
            # 1. if one of replaced ads is "younger"
            # than last_fetch_timestamp, we suppose
            # that we are starting to loop
            # throug ads and we should stop (after
            # three consecutive pages where "younger"
            # ads are found... juste to be sure.
            # 2. or if there were no ads in the page
            # we should also stop...
            # to stop : stop_after_page=page
            if err
              console.log ' [*] error fetching page ' + page + ' of ' + site.name + err
            else
              console.log ' [x] fetched page ' + page + ' of ' + site.name
              if ads.length == 0
                console.log ' [X] No more ads on this page, signaling to stop fetching of ' + site.name + ' after ' + page + ' pages.'
                stop_after_page = page
              else if fetching_duplicates last_fetch_timestamp, old_ads, ads
                found_duplicate_on_page.push page
                if we_should_stop found_duplicate_on_page
                  console.log ' [X] we are looping through ads, signaling to stop fetching of ' + site.name + ' after ' + page + ' pages.'
                  stop_after_page = page
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


fetching_duplicates = (timestamp, old_ads, ads) ->
  # we have to find at least three ads that
  # have been fetched after this fetching started
  # to consider having found duplicates on the page.
  youngers = (ad for ad in old_ads when ad.fields and ad.fields._timestamp > timestamp)
  youngers > 3

we_should_stop = (found_duplicate_on_page) ->
  if found_duplicate_on_page.length < 3
    false
  else
    found_duplicate_on_page.sort((a,b) -> a-b)
    a = found_duplicate_on_page[found_duplicate_on_page.length - 3]
    b = found_duplicate_on_page[found_duplicate_on_page.length - 2]
    c = found_duplicate_on_page[found_duplicate_on_page.length - 1]
    (b == a+1) and (c == b+1)
