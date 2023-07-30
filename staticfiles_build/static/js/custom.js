$(document).ready(function () {
    $('.increase').click(function (e) {
        e.preventDefault();

        var inc_val = $(this).closest('.product_data').find('.quantity-input').val();
        var value = parseInt(inc_value,10);
        value = isNan(value) ? 0 : value;
        if(value < 10){
            value++;
            $(this).closest('.product_data').find('.quantity-input').val(value);
        }


    });


    $('.decrease').click(function (e) {
        e.preventDefault();

        var dec_val = $(this).closest('.product_data').find('.quantity-input').val();
        var value = parseInt(dec_value,10);
        value = isNan(value) ? 0 : value;
        if(value > 1){
            value--;
            $(this).closest('.product_data').find('.quantity-input').val(value);
        }


    });

});

