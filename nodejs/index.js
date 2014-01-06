var path = require('path');
var express = require('express')
var ejs = require('elastic.js')

var app = express()

app.use(express.bodyParser());
app.use(express.static(path.join(__dirname, 'public')))

function price_filter(req) {
  return ejs.NumericRangeFilter("price").lte(parseInt(req.param('max_price')))
}

app.get('/', function(req, res) {
  with_criteria(req, function(filter) {
    get_pubs(function(results) {
      render(res, results, "new")
    }, ejs.QueryStringQuery('*'), filter)
  }, ejs.MissingFilter("opinion"))
})
app.get('/like', function(req, res) {
  with_criteria(req, function(filter) {
    get_pubs(function(results) {
      render(res, results, "like")
    }, ejs.TermQuery('opinion', 'like'), filter)
  })
})
app.get('/dislike', function(req, res) {
  with_criteria(req, function(filter) {
    get_pubs(function(results) {
      render(res, results, "dislike")
    }, ejs.TermQuery('opinion', 'dislike'), filter)
  })
})
app.get('/criteria', function(req, res) {
  get_criteria(function(criteria) {
    render_criteria(res, criteria)
  })
})
app.post('/criteria', function(req, res) {
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
  doc = ejs.Document("immo", "criteria", "criteria")
  doc.source(criteria).upsert(criteria)
  doc.doUpdate(function() {
    res.redirect("/criteria")
  }, function() {
    console.log("KATASTROPH")
  })
})
app.post('/pub/:id', function(req, res) {
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
var e_index = 'immo';
var e_type = 'immo';
function get_pubs(handle_results, query, filter) {
  if (! query) query = ejs.QueryStringQuery('*')
  if (! filter) filter = ejs.TypeFilter(e_type)
  
  // generates the elastic.js query and executes the search
  ejs.Request({indices: e_index, types: e_type})
    .query(query).size(100).filter(filter).doSearch(handle_results)
}

function vote(id, opinion, handle_update) {
  ejs.Document(e_index, e_type, id)
    .script('ctx._source.opinion = "' + opinion + '"')
    .doUpdate(handle_update(id, opinion))
}

function extract_pubs(results) {
  var pubs = []
  console.log("nb results: " + results.hits.total)
  for(var i = 0; i < results.hits.hits.length; i++) {
    pubs[i] = results.hits.hits[i]._source
    pubs[i].id = results.hits.hits[i]._id
  }
  return pubs
}

function render(res, results, active) {
    var pubs = extract_pubs(results)
    res.render('pubs.jade', {pubs: pubs, active: active})
}

function get_criteria(handle_results) {
  doc = ejs.Document(e_index, "criteria", "criteria")
  doc.doGet(function(result) {
    handle_results(result._source)
  }, function() {
    console.log("KATASTROPH")
  })
}

function with_criteria(req, handle, filter) {
  if (req.param('raw')) {
    handle(filter)
    return
  }
  if (! filter) filter = ejs.TypeFilter(e_type)
  filter = ejs.AndFilter(filter)
  get_criteria(function(criteria) {
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

function render_criteria(res, criteria) {
  res.render('criteria.jade', {criteria: criteria, active: 'criteria'})
}



app.listen(12043)
console.log("Server started")
