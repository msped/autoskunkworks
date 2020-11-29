function get_total(){
    var buildPrice = 0;
    $('.part-price').each(function () {
        current = $(this);
        if (!current.closest("tr").find("td>div>input").is(":checked")){
            buildPrice += parseFloat(current.val()) || 0;  
        }
    });
    $('#build-total').html(buildPrice.toFixed(2));
    $('input[name="total"]').val(buildPrice.toFixed(2));
}

function check_if_part_is_selected(table, part) {
    let check = false;
    $(table).find('tr td:first-child').each(function(){
        if ($(this).html() == part){
            check = true;
        }        
    });
    return check;
}

$(document).ready(function () {
    $('tbody').on('change input', '.part-price, input[type=checkbox]', function () {
        get_total();
    });

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
        event.preventDefault();
        return false;
        }
    });

    $('#add-exterior').on('click', function(){
        part_id = $('#exterior-categories').find(":selected").val();
        title = $('#exterior-categories').find(":selected").text();
        part_check = check_if_part_is_selected('.exterior-table', title);
        if (part_check) {
            alert("You can't add two of the same options!");
        } else {
            if (part_id != 'Choose an option'){
                var template = '<tr>' +
                                    '<td scope="row">' + title + '</td>' +
                                    '<td>' +
                                        '<input type="url" class="form-control input-sm" name="exterior_'+ part_id +'_link" required>' +
                                    '</td>' +
                                    '<td class="url-price">' +
                                        '<input type="number" class="form-control input-sm part-price" name="exterior_'+ part_id +'_price" step="any" required>' +
                                    '</td>' +
                                    '<td>' +
                                        '<div class="text-center">' +
                                            '<input type="checkbox" name="exterior_'+ part_id +'_purchased">' +
                                        '</div>'+
                                    '</td>' +
                                    '<td>' +
                                        '<i class="far fa-times-circle" id="delete-row"></i>' +
                                    '</td>' +
                                '</tr>';
                $('.exterior-table').append(template);
            }
        }        
    });

    $('#add-engine').on('click', function(){
        part_id = $('#engine-categories').find(":selected").val();
        title = $('#engine-categories').find(":selected").text();
        part_check = check_if_part_is_selected('.engine-table', title);
        if (part_check) {
            alert("You can't add two of the same options!");
        } else {
            if (part_id != 'Choose an option') {
            var template = '<tr>' +
                                '<td scope="row">' + title + '</td>' +
                                '<td>' +
                                    '<input type="url" class="form-control input-sm" name="engine_'+ part_id +'_link" required>' +
                                '</td>' +
                                '<td class="url-price">' +
                                    '<input type="number" class="form-control input-sm part-price" name="engine_'+ part_id +'_price" step="any" required>' +
                                '</td>' +
                                '<td>' +
                                    '<div class="text-center">' +
                                        '<input type="checkbox" name="engine_'+ part_id +'_purchased">' +
                                    '</div>'+
                                '</td>' +
                                '<td>' +
                                    '<i class="far fa-times-circle" id="delete-row"></i>' +
                                '</td>' +
                            '</tr>';
                $('.engine-table').append(template); 
            }
        }
    });

    $('#add-running-gear').on('click', function(){
        part_id = $('#running-gear-categories').find(":selected").val();
        title = $('#running-gear-categories').find(":selected").text();
        part_check = check_if_part_is_selected('.running-gear-table', title);
        if (part_check) {
            alert("You can't add two of the same options!");
        } else {
            if (part_id != 'Choose an option') {
            var template = '<tr>' +
                                '<td scope="row">' + title + '</td>' +
                                '<td>' +
                                    '<input type="url" class="form-control input-sm" name="running_'+ part_id +'_link" required>' +
                                '</td>' +
                                '<td class="url-price">' +
                                    '<input type="number" class="form-control input-sm part-price" name="running_'+ part_id +'_price" step="any" required>' +
                                '</td>' +
                                '<td>' +
                                    '<div class="text-center">' +
                                        '<input type="checkbox" name="running_'+ part_id +'_purchased">' +
                                    '</div>'+
                                '</td>' +
                                '<td>' +
                                    '<i class="far fa-times-circle" id="delete-row"></i>' +
                                '</td>' +
                            '</tr>';
                $('.running-gear-table').append(template); 
            }
        }
    });

    $('#add-interior').on('click', function(){
        part_id = $('#interior-categories').find(":selected").val();
        title = $('#interior-categories').find(":selected").text();
        part_check = check_if_part_is_selected('.interior-table', title);
        if (part_check) {
            alert("You can't add two of the same options!");
        } else {
            if (part_id != 'Choose an option') {
            var template = '<tr>' +
                                '<td scope="row">' + title + '</td>' +
                                '<td>' +
                                    '<input type="url" class="form-control input-sm" name="interior_'+ part_id +'_link" required>' +
                                '</td>' +
                                '<td class="url-price">' +
                                    '<input type="number" class="form-control input-sm part-price" name="interior_'+ part_id +'_price" step="any" required>' +
                                '</td>' +
                                '<td>' +
                                    '<div class="text-center">' +
                                        '<input type="checkbox" name="interior_'+ part_id +'_purchased">' +
                                    '</div>'+
                                '</td>' +
                                '<td>' +
                                    '<i class="far fa-times-circle" id="delete-row"></i>' +
                                '</td>' +
                            '</tr>';
                $('.interior-table').append(template); 
            }
        }
    });

    $('tbody').on('click', '#delete-row', function(){
        const model_id = $(this).next().next().val();
        const part_id = $(this).next().val();
        const row = $(this).closest('tr');
        const table = $(this).closest('tbody').attr('id');
        template = `<input type="hidden" name="` + table + `_` + part_id + `_delete" value="` + model_id +`">`;
        console.log(template + " Model: " + model_id);
        $('form').append(template);
        row.remove();
        get_total();
    });

    $('tbody').on('change paste', 'input[type=url]', function(){
        url_box = $(this);
        url = $(this).val();
        $.ajax({
            url: "/b/get-web-price",
            type: 'POST',
            data: {
                'url': url
            },
            success: function(data){
                input = url_box.closest('tr').find('.url-price').children('input.part-price');
                input.val(data);
                get_total();
            }
        });
    });
});
