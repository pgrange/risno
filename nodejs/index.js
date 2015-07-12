var path = require('path');
var express = require('express')
//TODO get rid of ejs, replace it with elasticsearch
var ejs = require('elastic.js')
var crypto = require('crypto')
var nconf = require('nconf')
var nodemailer = require('nodemailer')


var es_port = 'localhost:9200'
if (process.env.ELASTICSEARCH_PORT_9200_TCP_ADDR)
  es_port = process.env.ELASTICSEARCH_PORT_9200_TCP_ADDR
          + ':'
          + process.env.ELASTICSEARCH_PORT_9200_TCP_PORT

nconf.argv()
     .env()
     .file({ file: '/etc/opt/risno.json' })
     .defaults({ listen_port: 12043,
                 elastic_db: es_port})

var app = express()
app.locals.pretty = true


app.use(express.bodyParser());
app.use(express.static(path.join(__dirname, 'public')))

function price_filter(req) {
  return ejs.NumericRangeFilter("price").lte(parseInt(req.param('max_price')))
}

app.get('/', function(req, res) {
  var user_code = req.param('user_code')
  if (user_code) res.redirect(user_code)
  else { 
    user_code = crypto.randomBytes(10).toString('hex')
    res.render('welcome.jade', {user_code: user_code})
  }
})
app.get('/:user_code/new', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "new")
    }, new_query(user_code), filter)
  }, new_filter(user_code))
})
app.get('/:user_code/like', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "like")
    }, like_query(user_code), filter)
  }, like_filter(user_code))
})
app.get('/:user_code/dislike', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "dislike")
    }, dislike_query(user_code), filter)
  }, dislike_filter(user_code))
})
app.get('/:user_code/criteria', function(req, res) {
  var user_code = req.param('user_code')
  get_criteria(user_code, function(criteria) {
    render_criteria(res, user_code, criteria)
  })
})
app.post('/:user_code/criteria', function(req, res) {
  var user_code = req.param('user_code')
  var criteria = {
    max_price: parseInt(req.param('max_price')),
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
  console.log(criteria)
  doc = ejs.Document(e_index, "criteria", "criteria_" + user_code)
  doc.source(criteria).upsert(criteria)
  doc.doUpdate(function() {
    res.redirect("/" + user_code + "/new")
  }, function() {
    console.log("KATASTROPH")
  })
})
app.post('/:user_code/pub/:id', function(req, res) {
  var user_code = req.param('user_code')
  var id = req.param('id')
  var opinion = req.param('opinion')
  console.log("vote for " + 
              id + ": " + 
              opinion + 
              " by user_code: " + user_code)
  if (opinion != "like" && opinion != "dislike") {
    var msg = "That's not an opinion: " + opinion
    console.log(msg)
    res.send(400, msg)
  } else {
    vote(user_code, id, opinion, function() {
      res.send({id: id, opinion: opinion})
    })
  }
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
        send_new_id(mail, user_code)
        res.redirect(user_code + '/criteria')
      },
      function() {
        console.log("KATASTROPH")
      })
})
app.get('/check_mail', function(req, res) {
  var mail = req.param('email')
  var query = ejs.TermQuery('mail', mail)
  ejs.Request({indices: 'users', types: 'user'})
  .query(query).size(1000)
  .doSearch(function(result) {
    if (result.error) {
      console.log(result)
      res.send(false)
    } else if (result.hits.hits.length > 0) {
      res.send(true)
    } else {
      console.log("unknown email " + mail)
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
      console.log(result)
      res.send(500, '')
    }
    else if (result.hits.hits.length <= 0) {
      console.log("unknown email " + mail)
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
            console.log("Unable to send ids " +
                        "[" + mail + "]" + 
                        " " + error)
            res.send(500, '')
          } else {
            console.log("ids sent " +
                        "[" + mail + "]" + 
                        " " + response.message);
            res.send(200, '')
          }
        }
      )
    }
  },function(error) {
    console.log(error)
  })
})
app.get('/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  res.redirect(user_code + '/new')
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

function get_pubs(handle_results, query, filter) {
  if (! query) query = ejs.QueryStringQuery('*')
  if (! filter) filter = ejs.TypeFilter(e_type)
  
  // generates the elastic.js query and executes the search
  ejs.Request({indices: e_index, types: e_type})
    .query(query).size(100).filter(filter)
    .doSearch(handle_results,function(error) {
      console.log(error)
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
  console.log("nb results: " + results.hits.total)
  for(var i = 0; i < results.hits.hits.length; i++) {
    pubs[i] = results.hits.hits[i]._source
    pubs[i].id = results.hits.hits[i]._id
    pubs[i].opinion = opinion
  }
  return pubs
}

function render(res, user_code, results, active) {
    if (results.error) console.log(results)
    var pubs = extract_pubs(results, active)
    res.render('pubs.jade', {user_code: user_code, pubs: pubs, active: active})
}

function get_criteria(user_code, handle_results) {
  var criteria_id = "criteria_" + user_code
  doc = ejs.Document(e_index, "criteria", criteria_id)
  console.log('user_code: ' + user_code)
  console.log('criteria: ' + criteria_id)
  doc.doGet(function(result) {
    handle_results(result._source)
  }, function() {
    console.log("KATASTROPH")
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
        filter.filters(ejs.NumericRangeFilter("price").lte(criteria.max_price))
      if (criteria.cities)
        filter.filters(cities_filter(criteria.cities))
      if (criteria.types)
        filter.filters(types_filter(criteria.types))
    }
    handle(filter)
  })
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

function send_new_id(to, id) {
smtp_transport.sendMail(
 {
  from: "contact@risno.org",
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
     console.log("Unable to send new id " +
                 "[" + id + "]" + "[" + to + "]" + 
                 " " + error)
   } else {
     console.log("New id sent " +
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
    text += "http://risno.org/" + user_codes[i] + "\n"
  }
  return {
    from: "contact@risno.org",
    to: mail,
    subject: "Rappel de vos identifiants Risno",
    text: text
  }
}

var smtp_config = nconf.get('smtp')
if (! smtp_config.host)
  smtp_config = {
    "host": nconf.get('smtp_host'),
    "auth": {
      "user": nconf.get('smtp_user'),
      "pass": nconf.get('smtp_pass'),
    }
  }
  smtp_config = JSON.parse(smtp_config)
var smtp_transport = nodemailer.createTransport(smtp_config)
app.listen(nconf.get('listen_port'))
console.log("Server started")
