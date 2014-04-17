$(function() {
    $('ul.f-nav-tabs a').bind('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');

        CLASS_TABLE.create_dynamic_table(url);
    });
});

var CLASS_TABLE = {};

CLASS_TABLE.create_dynamic_table = function(url_load) {
    var url_for_json = url_load;

    $.getJSON(url_for_json, function(data) {
        $(html_table).remove();

        var dynamic_form = $('<form>', {
            'id': 'great_form',
            'method': 'post',
            'action': '/hd/test_url/'
        });
        var html_table = $('<table>', {
            'id':'editable',
            'class':'data-items'
        });
        var thead = $('<thead>');
        var trh = $('<tr>');

        $.each(data.fields, function(key, value) {
            var th = $('<th>').append(value);
            $(trh).append(th);
        });
        $(html_table).append($(thead).append(trh));

        $.each(data.qsd, function(key, value) {
            var tr = $('<tr>');
            var tmp_val = value;

            $.each(tmp_val, function(key, value) {
                var td = $('<td>').append(value);
                $(tr).append(td);
            });
            $(html_table).append(tr);
        });
        $('section#contentPane').html($(dynamic_form).append(html_table));
        CLASS_TABLE.add_edit_button_to_row(html_table);
        $('section#formPane').load('/hd/' + url_load + '/add/');
    });
}

CLASS_TABLE.add_edit_button_to_row = function(table) {
    var tables = $(table)

    tables.each(function() {
        var _table = $(this);
        _table.find('thead tr').append(
            $('<th class="edit">&nbsp;</th>')
        );
        _table.find('tbody tr').append(
            $('<td class="edit"><input type="button" value="Edit" /></td>')
        );
    });

    tables.find('.edit :button').on('click', function(e) {
        CLASS_TABLE.edit_table_row(this);
        e.preventDefault();
    });
}

CLASS_TABLE.edit_table_row = function(button) {
    var button = $(button);
    var row = button.parents('tbody tr');
    var cells = row.children('td').not('.edit');

    if (row.data('flag')) { // режим редактирования, переход в режим таблиці
        // cell methods
        cells.each(function() {
            var _cell = $(this);
            _cell.html(_cell.find('input').val())
        });

        row.data('flag', false);
        button.val('Edit');
    }
    else { // режим таблицы, переход в режим редактирования
        // cell methods
        cells.each(function() {
            var _cell = $(this);
            _cell.data('text', _cell.html()).html('');

            var input = $('<input type="text" />').val(_cell.data('text')).width(_cell.width() - 16);

            _cell.append(input);
        });

        row.data('flag', true);
        button.val('Save');
    }
}
