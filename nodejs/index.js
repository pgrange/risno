var path = require('path');
var express = require('express')
var ejs = require('elastic.js')

var app = express()

var user_code="12043"

app.use(express.bodyParser());
app.use(express.static(path.join(__dirname, 'public')))

function price_filter(req) {
  return ejs.NumericRangeFilter("price").lte(parseInt(req.param('max_price')))
}

app.get('/', function(req, res) {
  res.redirect('/new/' + user_code)
})
app.get('/new/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "new")
    }, new_query(user_code), filter)
  }, new_filter(user_code))
})
app.get('/like/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "like")
    }, like_query(user_code), filter)
  }, like_filter(user_code))
})
app.get('/dislike/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  with_criteria(req, user_code, function(filter) {
    get_pubs(function(results) {
      render(res, user_code, results, "dislike")
    }, dislike_query(user_code), filter)
  }, dislike_filter(user_code))
})
app.get('/criteria/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  get_criteria(user_code, function(criteria) {
    render_criteria(res, user_code, criteria)
  })
})
app.post('/criteria/:user_code', function(req, res) {
  var user_code = req.param('user_code')
  criteria = {
    max_price: parseInt(req.param('max_price')),
    cities: req.param('cities').split(',')
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
    res.redirect("/criteria")
  }, function() {
    console.log("KATASTROPH")
  })
})
app.post('/pub/:user_code/:id', function(req, res) {
  var user_code = req.param('user_code')
  var id = req.param('id')
  var opinion = req.param('opinion')
  console.log("vote for " + 
              id + ": " + 
              opinion)
  if (opinion != "like" && opinion != "dislike") {
    var msg = "That's not an opinion: " + opinion
    console.log(msg)
    res.send(400, msg)
  } else {
    vote(id, opinion, function() {
      res.send({id: id, opinion: opinion})
    })
  }
})
app.get('/suggest', function(req, res) {
  var prefix = req.param('prefix')
  client.suggest({
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
  client.suggest({
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

//new elasticsearch client part
var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
  host: 'localhost:9200'
});

//elastic part
var nc = require('elastic.js/elastic-node-client')
ejs.client = nc.NodeClient('localhost', 9200);
var e_index = 'ads_2.0';
var e_type = 'immo';

function new_query(user_code) {
  return ejs.QueryStringQuery('*')
}

function new_filter(user_code) {
  return ejs.AndFilter([
    ejs.TypeFilter('immo'),
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

function vote(id, opinion, handle_update) {
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
  doc = ejs.Document(e_index, "criteria", "criteria_" + user_code)
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
      filter.filters(ejs.NumericRangeFilter("price").lte(criteria.max_price))
      filter.filters(cities_filter(criteria.cities))
    }
    handle(filter)
  })
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



app.listen(12043)
console.log("Server started")
