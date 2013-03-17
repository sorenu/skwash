$ ->

out = (m) -> console.log m
    
$('.btn-add-buddy').live 'click', (e) ->
    href = $(this).attr 'href'
    out href
    klass = 
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            loadBuddyButton()
    

loadBuddyButton = ->
    klass = $('#add-buddy-container').attr 'class'
    if klass
        user_id = klass.split('__')[1]
        $.ajax '/buddies/' + user_id + '/button/',
            success: (data, textStatus, jqXHR) ->
                $('#add-buddy-container').html(data)

loadBuddyButton()

$('.btn-accept-buddy').live 'click', (e) ->
    row = $(this).closest '.buddy-request-row'
    href = $(this).attr 'href'
    $.ajax href,
        success: (data, textStatus, jqXHR) ->
            out href
            row.hide(300)