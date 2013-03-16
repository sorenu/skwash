$ ->

out = (m) -> console.log m

cache = {}


klassToUrl = (klass) ->
    klass = klass.replace('__', '/')
    klass = klass.replace('_', '/')
    return klass


klassToKey = (klass) ->
    return klass.split('__')[0]

changeKlassTo = (klass, replaceWith) ->
    splits = klass.split('__')
    postfix = splits[1]
    prefix = splits[0]
    prefixSplits = prefix.split('-')
    s = prefixSplits[0] + '-' + prefixSplits[1] + '-' + prefixSplits[2] + '-' + replaceWith
    s


getChallengeButtonHtml = (klass, element) ->
    url = klassToUrl klass
    key = klassToKey klass
    $.get url,
        (response) ->
            $(element).html response
            cache[key] = response
    

loadChallengeButtons = ->
    for e in $('.challenge-buttons-container')
        klass = e.classList.item(1)
        getChallengeButtonHtml klass, e


loadRankingBoard = (klass, element) ->
    $(element).fadeOut ->
        $.ajax klass,
            success: (data, textStatus, jqXHR) ->
                $(element).hide()
                $(element).html data
                $(element).fadeIn('slow')
                loadChallengeButtons()


for e in $('.board-container')
    klass = e.classList.item(1)
    loadRankingBoard klass, e


getCachedButtonHtml = (klass, element) ->
    key = klassToKey klass
    val = cache[key]
    if val
        $(element).html val
    else
        getChallengeButtonHtml klass, element


challengeButtonClicked = (btn) ->
    href = btn.attr('href')
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            p = btn.parent('.challenge-buttons-container')
            p.html(data)


$('.btn-challenge-play').live 'click', (e) ->
    btn = $(this)
    href = btn.attr('href')
    upper_li = btn.closest 'li'
    p = upper_li.children('.match-play-container:first')
    if p.html()
        p.toggle 100
    else
        $.ajax href,
            success: (data, textStatus, jqXHR) ->
                p.html(data)
                p.hide()
                p.show 100

    false

$('.btn-challenge-accept').live 'click', (e) ->
    challengeButtonClicked $(this)
    false

$('.btn-challenge-decline').live 'click', (e) ->
    challengeButtonClicked $(this)
    false

$('.btn-challenge-cancel').live 'click', (e) ->
    challengeButtonClicked $(this)
    false

$('.btn-challenge-challenge').live 'click', (e) ->
    challengeButtonClicked $(this)
    false

$('.btn-match-play-result').live 'click', (e) ->
    sectionElement = $(this).closest '.board-container'
    section = sectionElement.attr 'class'
    section = section.replace(/[\n\r\s]+/g, '?')
    section = section.split('?')[1]

    href = $(this).attr 'href'
    container = $(this).closest '.match-play-container'
    container.html('')
    li = container.closest 'li'
    span = li.children '.challenge-buttons-container:first'
    spanList = span.attr('class').replace(/[\n\r\s]+/g, '?');
    remove = spanList.split('?')[1]
    span.removeClass remove
    add = changeKlassTo(remove, 'challenge')
    span.addClass add

    getCachedButtonHtml add, span

    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            loadRankingBoard section, sectionElement

    false




