$ ->

out = (m) -> console.log m

$.ajax '/',
    type: 'GET'
    dataType: 'html'
    error: (jqXHR, textStatus, errorThrown) ->
        out 'error'
    success: (data, textStatus, jqXHR) ->
        out 'hell'

$('.btn-challenge-accept').click ->
    out 'btn accept'
    false

$('.btn-challenge-decline').click ->
    out 'btn decline'
    false

$('.btn-challenge-cancel').click ->
    out 'btn cancel'
    false

$('.btn-challenge-challenge').click ->
    out 'btn challenge'
    false