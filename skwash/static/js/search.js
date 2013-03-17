$(document).ready(function() {

    $('#typeahead').typeahead({

    source: function (query, process) {
        return $.get(
            '/search',
            { q: query, typeahead: true },
            function (data) {
                console.log(data[1])
                return process(data);
            });
    },
    updater:function (item) {
        window.location = '/profile/' + item;
        return item;
    }

    });
});