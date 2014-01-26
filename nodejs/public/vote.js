function init_vote() {
  $(".btn-vote").click(vote)
  
  function vote() {
    var opinion = $(this).hasClass('btn-success') 
      ? "like" : "dislike"
    var tr = $(this).parents('tr')
    var id = tr.attr('id')
  
    $.post("/" + user_code + "/pub/" + id, {opinion: opinion}, function(data) {
      tr.removeClass("like")
      tr.removeClass("dislike")
      tr.addClass(data.opinion)
    })
  }
}
