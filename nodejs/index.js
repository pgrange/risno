var path = require('path');
var express = require('express')
var ejs = require('elastic.js')

var app = express()

app.use(express.bodyParser());
app.use(express.static(path.join(__dirname, 'public')))

app.get('/', function(req, res) {
  get_pubs(function(results) {
    render(res, results, "new")
  }, ejs.QueryStringQuery('*'), ejs.MissingFilter("opinion"))
})
app.get('/like', function(req, res) {
  get_pubs(function(results) {
    render(res, results, "like")
  }, ejs.TermQuery('opinion', 'like'))
})
app.get('/dislike', function(req, res) {
  get_pubs(function(results) {
    render(res, results, "dislike")
  }, ejs.TermQuery('opinion', 'dislike'))
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



//elastic part
var nc = require('elastic.js/elastic-node-client')
ejs.client = nc.NodeClient('localhost', 9200);
var e_index = 'test-index';
var e_type = 'test-type';
function get_pubs(handle_results, query, filter) {
  if (! query) query = ejs.QueryStringQuery('*')
  if (! filter) filter = ejs.TypeFilter(e_type)
  
  // generates the elastic.js query and executes the search
  ejs.Request({indices: e_index, types: e_type})
    .query(query).size(1000).filter(filter).doSearch(handle_results)
}

function vote(id, opinion, handle_update) {
  ejs.Document(e_index, e_type, id)
    .script('ctx._source.opinion = "' + opinion + '"')
    .doUpdate(handle_update(id, opinion))
}

function extract_pubs(results) {
  var pubs = []
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

app.listen(12043)
console.log("Server started")
