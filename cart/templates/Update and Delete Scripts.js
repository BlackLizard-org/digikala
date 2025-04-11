$(document).on('click', '.update-cart', function(e){
        e.preventDefault();


        var productid = $(this).data('index');
        $.ajax({
            method: 'POST',
            url: '{% url "cart_update" %}',
            data: {
                product_id : $(this).data('index'),
                product_qty : $('#select' + productid + ' option:selected').text(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                action: "post"
            },
            success: function(response) {
                //console.log(json)
                //document.getElementById('cart_quantity').textContext=json.qty
                location.reload();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

//Delete Scripts
    $(document).on('click', '.delete-product', function(e) {
        e.preventDefault();

        $.ajax({
            method: 'POST',
            url: '{% url "cart_delete" %}',
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: "{{ csrf_token }}",
                action: "post"
            },
            success: function(response) {
                //console.log(json)
               //document.getElementById('cart_quantity').textContext=json.qty
               location.reload();
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });