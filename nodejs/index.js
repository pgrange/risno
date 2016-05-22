var path = require('path');
var express = require('express')
//TODO get rid of ejs, replace it with elasticsearch
var ejs = require('elastic.js')
var nconf = require('nconf')
var nodemailer = require('nodemailer')
var moment = require('moment')
var bunyan = require('bunyan')
var crypto = require('crypto')
var hash = function(value) {
  md5 = crypto.createHash('md5')
  md5.update(value)
  return md5.digest('hex')
}

nconf.argv()
     .env()
     .file({ file: '/etc/opt/risno.json' })
     .defaults({ listen_port: 12043,
                 elastic_db: 'localhost:9200'})

var app = express()
app.locals.pretty = true

app.use(express.bodyParser());
app.use(express.static(path.join(__dirname, 'public')))

function reqSerializer(req) {
  url = req.url.replace(/(\/_\/)(.*)(\/.*)/, function(match, p1, p2, p3, offset, string) {
    return p1+hash(p2)+p3
  })
  return {
    method: req.method,
    url: url,
    headers: req.headers
  }
}
var log = bunyan.createLogger({name: 'risno', serializers: {req: reqSerializer}})
app.use(function(req, res, next) {
  req.log = log.child({reqId: crypto.randomBytes(6).toString('hex')})
  res.log = req.log
  req.log.info({req: req})
  next()
})

app.get('/monitoring', function(req, res) {
  get_statistics(function(stats) {
    if (stats) {
      for (var i = 0; i < stats.length; i++) {
        var stat = stats[i]
        stat.human = moment(stat.older).fromNow()
      }
      res.send(stats)
    } else res.send(500)
  }, req)
})

app.get('/data', function(req, res) {
  var page = req.param('p')
  if (page) page = parseInt(page)
  else page=1
  get_raw_data(page, function(data) {
    if (data) {
      res.render('data.jade', {data: data, next_page: page+1})
    } else res.send(500)
  }, req)
})

app.get('/', function(req, res) {
  var user_code = req.param('user_code')
  if (user_code) res.redirect('_/' + user_code)
  else { 
    user_code = crypto.randomBytes(10).toString('hex')
    get_statistics(function(stats) {
      res.render('welcome.jade', {user_code: user_code, stats: stats, moment: moment})
    }, req)
  }
})

app.get('/_/:user_code/new', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      is_email_registered(user_code, function(email_registered) {
        render(res, user_code, email_registered, results, "new")
      }, req)
    }, new_query(user_code), filter, req)
  }, new_filter(user_code))
})
app.get('/_/:user_code/newnew', function(req, res) {
  var user_code = req.param('user_code')
  var _filter = new_filter(user_code)
  _filter = ejs.AndFilter([
    _filter,
    ejs.RangeFilter('first_seen').gt('now-1d')
  ])

  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      is_email_registered(user_code, function(email_registered) {
        render(res, user_code, email_registered, results, "new")
      }, req)
    }, new_query(user_code), filter, req)
  }, _filter)
})
app.get('/_/:user_code/like', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      is_email_registered(user_code, function(email_registered) {
        render(res, user_code, email_registered, results, "like")
      }, req)
    }, like_query(user_code), filter, req)
  }, like_filter(user_code))
})
app.get('/_/:user_code/dislike', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      is_email_registered(user_code, function(email_registered) {
        render(res, user_code, email_registered, results, "dislike")
      }, req)
    }, dislike_query(user_code), filter, req)
  }, dislike_filter(user_code))
})
app.get('/_/:user_code/criteria', function(req, res) {
  var user_code = req.param('user_code')
  get_criteria(user_code, function(criteria) {
    render_criteria(res, user_code, criteria)
  }, req)
})
app.post('/_/:user_code/criteria', function(req, res) {
  var user_code = req.param('user_code')
  var criteria = {
    max_price: parseInt(req.param('max_price')),
    min_price: parseInt(req.param('min_price')),
    cities: req.param('cities').split(','),
    types: [].concat(req.param('types'))
  }
  for(var i = 0; i < criteria.cities.length; i++) {
    city = criteria.cities[i]
    if (city == '') {
      criteria.cities.splice(i, 1)
      i--
    } else {
      //FIXME useless ?
      criteria.cities[i] = city
    }
  }
  doc = ejs.Document(e_index, "criteria", "criteria_" + user_code)
  doc.source(criteria).upsert(criteria)
  doc.doUpdate(function() {
    res.redirect("/_/" + user_code + "/new")
  }, function(e) {
    req.log.error("KATASTROPH" + e)
  })
})
app.post('/_/:user_code/pub/:id', function(req, res) {
  var user_code = req.param('user_code')
  var id = req.param('id')
  var opinion = req.param('opinion')
  if (opinion != "like" && opinion != "dislike") {
    var msg = "That's not an opinion: " + opinion
    res.send(400, msg)
  } else {
    vote(user_code, id, opinion, function() {
      res.send({id: id, opinion: opinion})
    })
  }
})
app.post('/_/:user_code/forget_me/:forget_me_code', function(req, res) {
  var user_code = req.param('user_code')
  var forget_me_code = req.param('forget_me_code')

  var query = ejs.TermQuery('user_code', user_code)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1000)
  .doSearch(function(result) {
    if (result.error) {
      req.log.error({result: result}, "error while searching for user(hashed) " + hash(user_code))
      res.send(500, '')
    } else if (result.hits.hits.length <= 0) {
      req.log.warn("unknown user_code(hashed) " + hash(user_code))
      res.send(404, '')
    } else if (result.hits.hits.length > 1){
      req.log.error({result: result}, "more than one mail for user_code(hashed) " + hash(user_code))
      res.send(500, '')
    } else {
      var user = result.hits.hits[0]._source
      var id   = result.hits.hits[0]._id
      if (forget_me_code != user.forget_me_code) {
        req.log.warn("unauthorized forget_me_code to suppress user(hashed) " + hash(user_code) + ": " + forget_me_code)
        res.send(403, '')
      } else {
        //WARNING performance issue risk with refresh here
        ejs.Document("users", "user", id)
        .refresh(true)
        .doDelete(
          function() {
            res.redirect("/_/" + user_code)
          },
          function(e) {
            req.log.error("KATASTROPH" + e)
            res.send(500, '')
          })
      }
    }
  })
})

app.get('/_/:user_code/forget_me/:forget_me_code', function(req, res) {
  var user_code = req.param('user_code')
  var forget_me_code = req.param('forget_me_code')
  res.render('forget_me.jade', {user_code: user_code,
                                forget_me_code: forget_me_code})
})
app.post('/_/:user_code/forget_me', function(req, res) {
  var user_code = req.param('user_code')

  var query = ejs.TermQuery('user_code', user_code)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1000)
  .doSearch(function(result) {
    if (result.error) {
      req.log.error({result: result}, "error while searching for user(hashed) " + hash(user_code))
      res.send(500, '')
    }
    else if (result.hits.hits.length <= 0) {
      req.log.warn("unknown user_code(hashed) " + hash(user_code))
      res.send(404, '')
    } else if (result.hits.hits.length > 1){
      req.log.error({result: result}, "more than one mail for user_code(hashed) " + hash(user_code))
      res.send(500, '')
    } else {
      var id = result.hits.hits[0]._id
      var mail = result.hits.hits[0]._source.mail
      var forget_me_code = crypto.randomBytes(10).toString('hex')
      ejs.Document("users", "user", id)
        .source({user_code: user_code,
                 mail: mail,
                 forget_me_code: forget_me_code})
        .doUpdate(
          function() {
            smtp_transport.sendMail(
              prepare_forget_me_mail(mail, user_code, forget_me_code),
              function(error, response) {
                if (error) {
                  req.log.error("Unable to send forget me code " +
                              "[" + hash(mail) + "]" + 
                              " " + error)
                  res.send(500, '')
                } else {
                  res.send(200, '')
                }
              }
            )
          },
          function(e) {
            req.log.error("KATASTROPH" + e)
          })
   }
  },function(error) {
    req.log.error({error: error})
  })
})
app.get('/suggest', function(req, res) {
  var prefix = req.param('prefix')
  elastic_client.suggest({
    index: "cities",
    body: {
      city: {
        text: prefix,
        completion: {
          field: "name_suggest",
          size: 1000
        }
      }
    }
  }, function(error, response) {
    res.send(response.city[0].options)
  })
})

app.get('/suggest/:prefix', function(req, res) {
  var prefix = req.param('prefix')
  elastic_client.suggest({
    index: "cities",
    body: {
      city: {
        text: prefix,
        completion: {
          field: "name_suggest",
          size: 1000
        }
      }
    }
  }, function(error, response) {
    res.send(response.city[0].options)
  })
})
app.post('/send_new_id', function(req, res) {
  var user_code = req.param('user_code')
  var mail = req.param('email')
  var confirm_email = req.param('confirm_email')
  //TODO check email == confirm_email

  //store email in db first time
  ejs.Document('users', 'user')
    .source({user_code: user_code, mail: mail})
    .doIndex(
      function() {
        send_new_id(mail, user_code, req)
        res.redirect(user_code + '/criteria')
      },
      function(e) {
        req.log.error("KATASTROPH" + e)
      })
})
app.get('/check_mail', function(req, res) {
  var mail = req.param('email')
  var query = ejs.TermQuery('mail', mail)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1000)
  .doSearch(function(result) {
    if (result.error) {
      req.log.error({result: result}, "error while searching for user by mail")
      res.send(false)
    } else if (result.hits.hits.length > 0) {
      res.send(true)
    } else {
      req.log.warn("unknown email " + mail)
      res.send(false)
    }
  })
})
app.post('/send_id', function(req, res) {
  var mail = req.param('email')
  var query = ejs.TermQuery('mail', mail)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1000)
  .doSearch(function(result) {
    if (result.error) {
      req.log.error({result: result}, "error while searching for user by mail")
      res.send(500, '')
    }
    else if (result.hits.hits.length <= 0) {
      req.log.warn("unknown email ")
      res.send(404, '')
    } else {
      var user_codes = []
      for(var i = 0; i < result.hits.hits.length; i++) {
        user_codes[i] = result.hits.hits[i]._source.user_code
      }
      smtp_transport.sendMail(
        prepare_send_id_mail(mail, user_codes),
        function(error, response) {
          if (error) {
            req.log.error("Unable to send ids " +
                        "[" + mail + "]" + 
                        " " + error)
            res.send(500, '')
          } else {
            req.log.info("ids sent " +
                        "[" + mail + "]" + 
                        " " + response.message);
            res.send(200, '')
          }
        }
      )
    }
  },function(error) {
    req.log.error({error: error}, "Unable to send id")
    req.send(500)
  })
})
app.get('/_/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  res.redirect('/_/' + user_code + '/new')
})
app.get('/:user_code', function(req, res) {
  //Compatibility for deprecated /:user_code urls
  var user_code = req.param('user_code')
  res.redirect('/_/' + user_code)
})
app.get('/:user_code/:action', function(req, res) {
  //Compatibility for deprecated /:user_code/:action urls
  var user_code = req.param('user_code')
  var action = req.param('action')
  res.redirect('/_/' + user_code + '/' + action)
})


//new elasticsearch client part
var elasticsearch = require('elasticsearch');
var elastic_client = new elasticsearch.Client({
  host: nconf.get('elastic_db')
});

//elastic part
var nc = require('elastic.js/elastic-node-client')
var host_port = nconf.get('elastic_db').split(':')
ejs.client = nc.NodeClient(host_port[0], host_port[1]);
var e_index = 'ads';
var e_type = 'immo';

function new_query(user_code) {
  return ejs.QueryStringQuery('*')
}

function new_filter(user_code) {
  return ejs.AndFilter([
    ejs.TypeFilter('immo'),
    ejs.MissingFilter('expired'),
    ejs.NotFilter(ejs.HasChildFilter(
      ejs.TermQuery('user_code', user_code), "opinion"))
  ])
}

function like_query(user_code) {
  return ejs.HasChildQuery(
    ejs.BoolQuery()
      .must(ejs.TermQuery('user_code', user_code))
      .must(ejs.TermQuery('opinion', 'like')),
    'opinion')
}

function like_filter(user_code) {
  return ejs.TypeFilter('immo')
}
var dislike_filter = like_filter

function dislike_query(user_code) {
  return ejs.HasChildQuery(
    ejs.BoolQuery()
      .must(ejs.TermQuery('user_code', user_code))
      .must(ejs.TermQuery('opinion', 'dislike')),
    'opinion')
}

function get_pubs(handle_results, query, filter, req) {
  if (! query) query = ejs.QueryStringQuery('*')
  if (! filter) filter = ejs.TypeFilter(e_type)
  
  // generates the elastic.js query and executes the search
  ejs.Request({indices: e_index, types: e_type})
    .query(query).sort("first_seen", "desc" )
    .size(100).filter(filter)
    .doSearch(handle_results,function(error) {
      req.log.error(error)
    })
}

function is_email_registered(user_code, handle, req) {
  var query = ejs.TermQuery('user_code', user_code)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1)
  .doSearch(function(result) {
    if (result.error) {
      req.log.error({result: result})
      handle(false)
    } else if (result.hits.hits.length == 0){
      handle(false)
    } else {
      handle(true)
    }
  })
}

function vote(user_code, id, opinion, handle_update) {
  ejs.Document(e_index, 'opinion', user_code + '_' + id)
    .parent(id)
    .source({user_code: user_code, opinion: opinion})
    .doIndex(handle_update(id, opinion))
}

function extract_pubs(results, opinion) {
  var pubs = []
  for(var i = 0; i < results.hits.hits.length; i++) {
    pubs[i] = results.hits.hits[i]._source
    pubs[i].id = results.hits.hits[i]._id
    pubs[i].opinion = opinion
  }
  return pubs
}

function render(res, user_code, email_registered, results, active) {
    if (results.error) res.log.error({result: results})
    var pubs = extract_pubs(results, active)
    res.render('pubs.jade', {user_code: user_code, email_registered: email_registered, pubs: pubs, active: active})
}

function get_criteria(user_code, handle_results, req) {
  var criteria_id = "criteria_" + user_code
  doc = ejs.Document(e_index, "criteria", criteria_id)
  doc.doGet(function(result) {
    handle_results(result._source)
  }, function(e) {
    req.log.error("KATASTROPH" + e)
  })
}

function with_criteria(req, user_code, handle, filter) {
  if (req.param('raw')) {
    handle(filter)
    return
  }
  if (! filter) filter = ejs.TypeFilter(e_type)
  filter = ejs.AndFilter(filter)
  get_criteria(user_code, function(criteria) {
    if (criteria) {
      if (criteria.max_price)
        filter.filters(ejs.RangeFilter("price").lte(criteria.max_price))
      if (criteria.min_price)
        filter.filters(ejs.RangeFilter("price").gte(criteria.min_price))
      if (criteria.cities)
        filter.filters(cities_filter(criteria.cities))
      if (criteria.types)
        filter.filters(types_filter(criteria.types))
    }
    handle(filter)
  }, req)
}

function types_filter(types) {
  var filters = []
  for(var i = 0; i < types.length; i++) {
    var type = types[i]
    if (type == "other") {
      filters.push(ejs.MissingFilter('types'))
    } else {
      filters.push(ejs.QueryFilter(ejs.MatchQuery('types', type)))
    }
  }
  return ejs.OrFilter(filters)
}

function cities_filter(cities) {
  var filters = []
  for(var i = 0; i < cities.length; i++) {
    var city = cities[i].replace(' ', '')
    filters.push(ejs.QueryFilter(ejs.MatchQuery('cities', city)))
  }
  return ejs.OrFilter(filters)
}

function render_criteria(res, user_code, criteria) {
  res.render('criteria.jade', {user_code: user_code, criteria: criteria, active: 'criteria'})
}

//city pretty formatting
app.locals.format_city_from_id = function(id) {
  id = '' + id //convert jade object to string
  var ucFirstAllWords = function(str) {
    var pieces = str.split(" ");
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1).toLowerCase();
    }
    return pieces.join(" ");
  }

  var zip = id.replace(/fr_([0-9]+)_.*/, '$1')
  var name = id.replace(/fr_[0-9]+_/, '').replace(/_/g, ' ')
  return ucFirstAllWords(name) + ' (' + zip + ')'
}
//type pretty formatting
app.locals.tr_type = function(type) {
  var tr_type = {
    'flat' : {text: 'appart.', icon: 'glyphicon-stats'},
    'house': {text: 'maison', icon: 'glyphicon-home'},
    'field': {text: 'terrain', icon: 'glyphicon-flag'}
  }
  var tr = tr_type[type]
  if (! tr) tr = {'text': 'autre', icon: 'glyphicon-question-sign'}
  return tr
}

function send_new_id(to, id, req) {
smtp_transport.sendMail(
 {
  from: "Risno <contact@risno.org>",
  to: to,
  subject: "Bienvenue sur Risno",
  text: "Bonjour,\n" +
        "\n" +
        "Bienvenue sur Risno !\n" +
        "Retrouvez vos nouvelles annonces immobilières sur Risno :\n" +
        "\n" +
        "http://risno.org/" + id
 },
 function(error, response) {
   if (error) {
     req.log.error("Unable to send new id " +
                 "[" + id + "]" + "[" + to + "]" + 
                 " " + error)
   } else {
     req.log.info("New id sent " +
                 "[" + id + "]" + "[" + to + "]" + 
                 " " + response.message);
   }
 })
}

function prepare_send_id_mail(mail, user_codes) {
  var text= "Bonjour,\n" +
        "\n" +
        "Retrouvez vos nouvelles annonces immobilières sur Risno :\n" +
        "\n"
  for(var i = 0; i < user_codes.length; i++) {
    text += "http://risno.org/_/" + user_codes[i] + "\n"
  }
  return {
    from: "Risno <contact@risno.org>",
    to: mail,
    subject: "Rappel de vos identifiants Risno",
    text: text
  }
}

function prepare_forget_me_mail(mail, user_code, forget_me_code) {
  var text= "Bonjour,\n" +
        "\n" +
        "Quelqu'un a demandé à supprimer votre email de Risno. S'il s'agit bien de vous, cliquez sur le lien ci-dessous pour effectuer cette opération :\n" +
        "\n"
    text += "http://risno.org/_/" + user_code + "/forget_me/" + forget_me_code + "\n"
  return {
    from: "Risno <contact@risno.org>",
    to: mail,
    subject: "Suppression de votre email sur Risno",
    text: text
  }
}

function get_raw_data(page, callback, req) {
  elastic_client.search({
    index: "ads",
    type: "immo",
    size: 100,
    from: 100*(page-1)
  },
  function(error, response) {
    if (error) { 
      req.log.error({error: error})
      return callback()
    }
    console.log(response)
    var results=[]
    for(var i = 0; i < response.hits.hits.length; i++) {
      var pub = response.hits.hits[i]._source
      if (pub.cities && pub.cities.length > 0) pub.city = pub.cities[0]
      if (pub.types  && pub.types.length  > 0) pub.type = pub.types[0]
      results.push(pub)
    }
    callback(results)
  })
}

function get_statistics(callback, req) {
  elastic_client.search({
    index: "ads",
    searchType: "count",
    body: {
      aggregations: {
        not_expired: {
          filter: {
            missing: {
              field: "expired"
            }
          },
          aggregations: {
            nb_per_site: {
              terms: {
                field: "site_host"
              },
              aggregations: {
                older: {
                  min: {
                    field: "_timestamp"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  function(error, response) {
    if (error) { 
      req.log.error({error: error})
      return callback()
    }
    var aggregations = response.aggregations.not_expired.nb_per_site.buckets
    var results = [] 
    for(var i = 0; i < aggregations.length; i++) {
      var aggregation = aggregations[i]
      if (aggregation.key) {
        results.push({
          host: aggregation.key,
          nb: aggregation.doc_count,
          older: aggregation.older.value
        })
      }
    }
    callback(results)
  })
}

var smtp_config = nconf.get('smtp')
if (! smtp_config || ! smtp_config.host)
  smtp_config = {
    "host": nconf.get('smtp_host'),
    "auth": {
      "user": nconf.get('smtp_user'),
      "pass": nconf.get('smtp_pass')
    }
  }
  smtp_port=nconf.get('smtp_port')
  if (smtp_port) smtp_config.port = smtp_port
var smtp_transport = nodemailer.createTransport(smtp_config)
app.listen(nconf.get('listen_port'))
log.info("Server started")
