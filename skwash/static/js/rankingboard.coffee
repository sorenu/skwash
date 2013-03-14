$ ->

out = (m) -> console.log m

cache = {}

klassToUrl = (klass) ->
    klass = klass.replace('__', '/')
    klass = klass.replace('_', '/')
    return klass

klassToKey = (klass) ->
    return klass.split('__')[0]

getChallengeButtonHtml = (klass, element) ->
    url = klassToUrl klass
    key = klassToKey klass
    out url
    $.get url,
        (response) ->
            $(element).html response
            out response
            cache[key] = response
    

for e in $('.challenge-buttons-container')
    klass = e.classList.item(1)
    getChallengeButtonHtml klass, e


getCachedButtonHtml = (klass, element) ->
    key = klassToKey klass
    val = cache[key]
    if val
        $(element).html val
    else
        getChallengeButtonHtml klass, element


$('.btn-challenge-accept').live 'click', (e) ->
    btn = $(this)
    href = btn.attr('href')
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            p = btn.parent('.challenge-buttons-container')
            p.html(data)
            out(data)
    false

$('.btn-challenge-decline').live 'click', (e) ->
    btn = $(this)
    href = btn.attr('href')
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            p = btn.parent('.challenge-buttons-container')
            p.html(data)
            out(data)
    false

$('.btn-challenge-cancel').live 'click', (e) ->
    btn = $(this)
    href = btn.attr('href')
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            p = btn.parent('.challenge-buttons-container')
            p.html(data)
            out(data)
    false

$('.btn-challenge-challenge').live 'click', (e) ->
    btn = $(this)
    href = btn.attr('href')
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            p = btn.parent('.challenge-buttons-container')
            p.html(data)
            out(data)
    false



