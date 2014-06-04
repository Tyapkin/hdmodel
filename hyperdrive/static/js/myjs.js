$(function() {
    $('ul.f-nav-tabs a').bind('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');

        CLASS_TABLE.create_dynamic_table(url);
    });
    $('.datepicker').datepicker();
    $.datepicker.setDefaults({ dateFormat: 'yy-mm-dd' });
});

var CLASS_TABLE = {};

CLASS_TABLE.create_dynamic_table = function(url_load) {
    var url_for_json = url_load;

    $.getJSON(url_for_json, function(data) {
        var html_table = $('<table>', {
            'id':'hdtable'
        });
        var thead = $('<thead>');
        var trh = $('<tr>');

        $.each(data.fields_name, function(key, value) {
            var th = $('<th>').append(value);
            $(trh).append(th);
        });
        $(html_table).append($(thead).append(trh));

        $.each(data.items, function(i, val) {
            var tr = $('<tr>');
            $.each(data.items[i], function(j, val) {
                var field_data = data.items[i][j];
                var td = $('<td>', {
                    'class': 'editable',
                    'field_type': field_data.type,
                    'field_name': field_data.name,
                    'model': data.model
                }).append(field_data.value);
                $(tr).append(td);
            });
            $(html_table).append(tr);
        });

        $('section#contentPane').html(html_table);
        $('section#formPane').load('/hd/' + url_load + '/add/');
        $('td.editable').on('click', CLASS_TABLE.inline_edit);
    });
}

CLASS_TABLE.inline_edit = function() {
    var type = $(this).attr('field_type');
    var input = $('<input>', {
        'id': 'input',
        'name': 'value',
        'value': $(this).text()
    });

    if (type != 'auto') {
        if (type == 'date') {
            input.prop({'class': 'datepicker', 'readonly': true});
        }
        $(this).empty().unbind('click').append(input);

        if (type == 'date') {
            $('#input').datepicker({dateFormat: 'yy-mm-dd'}).change(CLASS_TABLE.inline_submit).focus();
        }
        else {
            $('#input').focus().blur(CLASS_TABLE.inline_submit).keyup(CLASS_TABLE.enter_detector);
        }
    }
}

CLASS_TABLE.enter_detector = function(e) {

    if (e.which == 13) {
        $(this).blur();
    }
    return false;
}

CLASS_TABLE.inline_submit = function() {
    var model = $(this).parent().attr('model');
    var obj_id = $(this).closest('tr').find('td[field_name=id]').text();
    var td = $(this).closest('.editable');
    var field_name = td.attr('field_name');
    var value = $(this).val();
    var field_type = td.attr('field_type');

    if (field_type == 'int' && !$.isNumeric(value)) {
        td.empty().text($(this).attr('init_data')).click(CLASS_TABLE.inline_edit);
        alert('Only integer values allowed for this field, you entered: ' + value);
    }
    else {
        $.ajax({
            type: 'POST',
            url: '/hd/edit/',
            data: {
                'model': model,
                'obj_id': obj_id,
                'field_name': field_name,
                'value': value,
                'csrfmiddlewaretoken': $.cookie('csrftoken')
            },
            success: function(data) {
                td.empty().text(value).click(CLASS_TABLE.inline_edit);
            }
        });
    }
}