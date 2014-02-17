function init_criteria() {
  $('#cities').select2({
    placeholder: "Indiquez une ou plusieurs villes",
    allowClear: true,
    multiple: true,
    width: '300px',
    ajax: {
      url: "/suggest",
      dataType: "json",
      data: function(term, page) {
        return {prefix: term}
      },
      results: function(data, page) {
        result = []
        for(var i = 0; i < data.length; i++) {
          result.push({
            id: data[i].payload,
            text: ucFirstAllWords(data[i].text)})
        }
        return {results: result}
      }
    },
    initSelection : function (element, callback) {
      var data = [];
      var value = element.val()
      $(value.split(",")).each(function () {
          data.push({id: this, text: format_city_from_id(this)});
      });
      callback(data);
    }
  })
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
function format_city_from_id(id) {
  var zip = id.replace(/fr_([0-9]+)_.*/, '$1')
  var name = id.replace(/fr_[0-9]+_/, '').replace(/_/g, ' ')
  return ucFirstAllWords(name) + ' (' + zip + ')'
}

function postpone( fun )
{
  window.setTimeout(fun,0);
}
