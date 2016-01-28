function init_vote() {
  $(".btn-vote").click(vote)
  
  function vote() {
    var opinion = $(this).hasClass('btn-success') 
      ? "like" : "dislike"
    var pub = $(this).parents(".pub")
    var id = pub.attr('id')
  
    $.post("/_/" + user_code + "/pub/" + id, {opinion: opinion}, function(data) {
      pub.removeClass("like")
      pub.removeClass("dislike")
      pub.addClass(data.opinion)
    })
    return false //avoid following link if any defined on this button
  }
}
