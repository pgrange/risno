function handle_pubs(query, filter) {
  'use strict';
  var e_index = 'test-index';
  var e_type = 'test-type';

  if (! query) query = ejs.QueryStringQuery('*')
  if (! filter) filter = ejs.TypeFilter(e_type)
  // setup elastic.js client for jQuery
  ejs.client = ejs.jQueryClient('http://localhost:9200');
  
  var viewport = $('#viewport')
    
    
  // renders the results page
  var displayPubs = function (results) {
    viewport.empty()
    $.each(results.hits.hits, function(index, value) {
    var line = $('<tr>').append(
      $('<td>').append(value._source.placement),
      $('<td>').append(value._source.price),
      $('<td>').append($('<a href="' + value._source.url + '">')
        .append('<img src="' + value._source.img + '" ' +
                     'width="200px"/>')),
      $('<td>').append(
        $('<button type="button" class="btn btn-success">Bien</button>'),
        $('<button type="button" class="btn btn-danger">Bof</button>')
      )).data('value', value)
        .on('click', 'button:not(.disabled)', vote)
      if (value._source.opinion == 'like')
        line.find('button.btn-success').css('visibility', 'hidden')
      if (value._source.opinion == 'dislike')
        line.find('button.btn-danger').css('visibility', 'hidden')
      viewport.append(line)
    })
  }
  
  // generates the elastic.js query and executes the search
  ejs.Request({indices: e_index, types: e_type})
    .query(query).size(1000).filter(filter).doSearch(displayPubs)
  
  function vote() {
    var like = $(this).hasClass('btn-success')
    var buttons = $(this).siblings('button').add(this)
    var id = $(this).parents('tr').data('value')._id
  
    buttons.addClass('disabled')
  
    ejs.Document(e_index, e_type, id).script('ctx._source.opinion = "' + (like ? 'like' : 'dislike') + '"').doUpdate(
      function() {
        buttons.removeClass("disabled"); 
        buttons.css('visibility', 'visible')
        buttons.filter('.btn-success').fadeTo(500, like ? 0 : 1)
        buttons.filter('.btn-danger').fadeTo(500, like ? 1 : 0)},
      function() {buttons.removeClass("disabled")})
  }
}
