var slurp = require('../../slurp')

$(document).ready(function() {
  $('#url_sequence').change(refresh_remote)
  $('#page_number').change(refresh_remote)
  $('#region').change(refresh_remote)
  $('#ad_selector').change(show_ads)
  $('#price_selector').change(show_ads)
  $('#description_selector').change(show_ads)
  $('#location_selector').change(show_ads)
  refresh_remote()
})

function wait_for_ads () {
  if (show_ads.call($('#ad')[0]) == 0) 
    setTimeout(wait_for_ads, 500)
  else
    $('head', $('#remote').contents())
    .append('<link rel="stylesheet" type="text/css" href="/parsing.css">')
    .append('<base href="http://www.leboncoin.fr/">')
}

function refresh_remote() {
  var page_number = $('#page_number').val()
  var region = $('#region').val()
  var url_sequence = $('#url_sequence').val()
  url_sequence = encodeURIComponent(url_sequence)
  $('#remote').attr('src', 'remote' + window.location.pathname + '?url_sequence=' + url_sequence + '&page_number=' + page_number + '&region=' + region)
  wait_for_ads()
}

function show_ads2() {
  var ad_css = 'ad_parsing'
  var price_css = 'price_parsing'
  var description_css = 'description_parsing'
  var location_css = 'location_parsing'
  var remote_frame = $('#remote')

  //clear previous selection
  $('.' + ad_css, remote_frame.contents()).removeClass(ad_css)
  $('.' + price_css, remote_frame.contents()).removeClass(price_css)
  $('.' + description_css, remote_frame.contents()).removeClass(description_css)
  $('.' + location_css, remote_frame.contents()).removeClass(location_css)

  var site = {
    name: "le-bon-coin",
    host: "www.leboncoin.fr",
    url_sequence: $('#url_sequence').val().split('\n'),
    ads: $('#ad_selector').val(),
    selectors: {
      price: $('#price_selector').val(),
      location: $('#location_selector').val(),
      description: $('#description_selector').val()
    }
  }
  $('#found_ads').empty()
  var ads = slurp.find_ads(remote_frame.contents(), site)
  ads.each(function(i, item) {
    var ad = slurp.parse_ad($(item), site)
    $('#found_ads').append('<p>').append(JSON.stringify(ad))
  })
}

function show_ads() {
  show_ads2()
  var ad_css = 'ad_parsing'
  var price_css = 'price_parsing'
  var description_css = 'description_parsing'
  var location_css = 'location_parsing'
  var remote_frame = $('#remote')

  //clear previous selection
  $('.' + ad_css, remote_frame.contents()).removeClass(ad_css)
  $('.' + price_css, remote_frame.contents()).removeClass(price_css)
  $('.' + description_css, remote_frame.contents()).removeClass(description_css)
  $('.' + location_css, remote_frame.contents()).removeClass(location_css)

  var ad_selector = $('#ad_selector').val()
  var elts = remote_frame.contents().find(ad_selector)
  $('#nb_ads').text(elts.length)
  elts.addClass(ad_css)

  var price_selector = $('#price_selector').val()
  var prices = elts.find(price_selector)
  prices.addClass(price_css)

  var description_selector = $('#description_selector').val()
  var descriptions = elts.find(description_selector)
  descriptions.addClass(description_css)

  var location_selector = $('#location_selector').val()
  var locations = elts.find(location_selector)
  locations.addClass(location_css)

  return elts.length
}
