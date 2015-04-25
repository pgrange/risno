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
    last_page_candidates = []
    do (site, region, last_fetch_timestamp, stop_after_page, last_page_candidates) ->
      async.mapLimit [1..3000], 10, (page, callback) ->
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
              if ads.length == 0 or (fetching_duplicates last_fetch_timestamp, old_ads, ads)
                msg =  if ads.length == 0 then 'No ad' else 'Found duplicated ads'
                console.log ' [_] ' + msg + ' on page ' + page + ' for ' + site.name + '. Adding this to stop page candidates'
                last_page_candidates.push page
                if we_should_stop last_page_candidates
                  console.log ' [X] Enough last page candidates. Signaling to stop fetching of ' + site.name + ' after ' + page + ' pages.'
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

we_should_stop = (last_page_candidates) ->
  if last_page_candidates.length < 3
    false
  else
    last_page_candidates.sort((a,b) -> a-b)
    a = last_page_candidates[last_page_candidates.length - 3]
    b = last_page_candidates[last_page_candidates.length - 2]
    c = last_page_candidates[last_page_candidates.length - 1]
    (b == a+1) and (c == b+1)
