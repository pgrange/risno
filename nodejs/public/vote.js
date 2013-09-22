function init_vote() {
  $(".btn").click(vote)
  
  function vote() {
    var opinion = $(this).hasClass('btn-success') 
      ? "like" : "dislike"
    var tr = $(this).parents('tr')
    var id = tr.attr('id')
  
    $.post("pub/" + id, {opinion: opinion}, function(data) {
      tr.removeClass("like")
      tr.removeClass("dislike")
      tr.addClass(data.opinion)
    })
  }
}
