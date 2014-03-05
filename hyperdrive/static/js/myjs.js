$(function() {
    $('ul.f-nav-tabs a').click(function() {
        var url = $(this).attr('href');
        $.getJSON(url, function(data) {
            $('table#items').remove();
            var html_table = '<table id="items"></table>';
            var tr = '<tr>';

            $.each(data.fields, function(key, value) {
                tr += '<th>' + value + '</th>';
            });
            tr += '</tr>';
            var html_table = $(html_table).append(tr);

            $.each(data.qsd, function(key, value) {
                var tmp_val = value;
                var tr = '<tr id="vals">';
                $.each(tmp_val, function(key, value) {
                    tr += '<td>' + value + '</td>';
                });
                tr += '</tr>';
                html_table = $(html_table).append(tr);
            });
            $('section#contentPane').html(html_table);
        });
        return false;
    });
});