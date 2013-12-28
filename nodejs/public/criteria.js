function init_criteria() {
  $('body').on('focusin', ".term:last", new_keyword)
  activate_auto_completion()
  
  function new_keyword() {
    var new_keyword = $('<div><input class="term form-control" type="text" name="term" placeholder="mot clé"/></div>')
    $(this).after(new_keyword)
    activate_auto_completion()
  }

  function activate_auto_completion() {
    $('.term').attr("autocomplete", "off")
    $('.term').typeahead({source: fetch_cities_completion})
  }

  function fetch_cities_completion(prefix, completions_handler) {
    //TODO indirection through node application
    $.ajax("http://localhost:9200/cities/_suggest", 
           {type: "POST",
            data: JSON.stringify({
             city: { text: prefix,
              completion: {
               field: "name_suggest",
               size: 1000,
              }
             }
           })})
    .done(function(suggestions) {
           var options = suggestions.city[0].options
           var formatted_options = []
           for(var i = 0; i < options.length; i++) {
             formatted_options.push(ucFirstAllWords(options[i].text))
           }
           completions_handler(formatted_options)
          })
  }
}
function ucFirstAllWords( str )
{
    var pieces = str.split(" ");
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1).toLowerCase();
    }
    return pieces.join(" ");
}
