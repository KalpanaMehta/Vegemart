$(document).ready(function(){
       // Review 
       $("#review-form").submit(function(e) { 
        e.preventDefault();

        $.ajax({
            data : $(this).serialize,
            method:$(this).attr("method"),
            url: $(this).attr("action"),
            dataType:'json',
            
            success: function(response){
               console.log("saved  successfully ");
               
            },
            
        })
      });
    








    $(".filter-checkbox").on("click",function(){
        console.log("cb have been clicked");

        let filter_object = {}

        $(".filter-checkbox").each(function(){
            let filter_key = $(this).data("filter")   // vendor, category

            
            filter_object[filter_key + '[]'] = $("input[data-filter='" + filter_key + "']:checked").map(function () {
                return $(this).val();
              }).get();
            
        })
        // 127.0.0.1/filter-products/? 
        console.log("filter object is ", filter_object);
        $.ajax({
            url: '/filter-products',
            data : filter_object,
            dataType:'json',
            beforeSend: function(){
                console.log("trying data")
            },
            success: function(response){
                console.log(response);
                console.log("Data filter successfully ");
                $(".filtered-product").html(response.data);
            },
            error: function (error) {
                console.log("Error occurred while filtering data: ", error);
              }
        })
    })
        // Add to cart functionality

    $(".add-to-cart-btn").on("click",function(){

        let this_val = $(this);
        let index = this_val.attr("data-index");

        let quantity = $(".product-quantity-" + index).val();
        let product_title = $(".product-title-" + index).val();
        let product_id = $(".product-id-" + index).val();
        let product_price = $(".current-product-price-" + index).text();
        let product_pid = $(".product-pid-" + index).val();
        let product_image = $(".product-image-" + index).val();
        
        console.log("Index:", index);
        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Product ID:", product_id);
        console.log("Product Price:", product_price);
        console.log("Product PID:", product_pid);
        console.log("Product Image:", product_image);

        $.ajax({
            url:'/add-to-cart',
            data : {
                'id': product_id,
                'pid': product_pid,
                'qty': quantity,
                'title':product_title,
                'price':product_price,
                'image': product_image,
               
            },
            dataType:'json',
            beforeSend: function(){
                console.log("Adding products to the cart");
            },
            success: function(response) {
                this_val.html("✔");
                console.log("Added products to the cart");
                $(".cart-items-count").text(response.totalcartitems);
            }
            
        })
    })

    // delete functionality
    $(".delete-product").on("click",function(){
        let product_id = $(this).attr("data-product")
        let this_val =$(this)
    
        console.log("Product id:", product_id);
        var timestamp = new Date().getTime();

       
        var url = '/cart?_=' + timestamp;
        
        
        $.ajax({
            url:'/delete-from-cart',
            data:{
                "id":product_id,
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                $(".cart-items-count").text(response.totalcartitems)
                console.log(response.success)
                this_val.show()
                console.log(response.data);
                $(".new-cart-list").html(response.data);
                // if (response.success) {
                //     this_val.show()
                   
                //     $(".new-cart-list").html(response.data);
                // }
                // else {
                //     console.log("Deletion was not successful.");
                                  
                //     }
    
            }
        })
    })
    
    // adding to wishlist
    $(document).on("click",".add-to-wishlist",function(){
        let product_id = $(this).attr("data-product-item")
        let this_val= $(this)

        console.log("product id is:", product_id);
        $.ajax({
            url:'/add-to-wishlist',
            data : {
                'id': product_id,
               
            },
            dataType:'json',
            beforeSend: function(){
                console.log("Adding products to wishlist");
            },
            success: function(response) {
                if(response.bool==true){
                    console.log("Added products to wishlist");
                    this_val.html("✔");
               
               
                }
               
            }
            
        })
    })
    
    //remove from wishlist

    // $(document).on("click",".delete-wishlist-product",function(){
    //     let wishlist_id = $(this).attr("data-wishlist-product")
    //     let this_val= $(this)

    //     console.log("wishlist",wishlist_id);
    //     $.ajax({
    //         url:'/remove-from-wishlist',
    //         data : {
    //             'id':wishlist_id,
               
    //         },
    //         dataType:'json',
    //         beforeSend: function(){
    //             console.log("deleting products to wishlist");
    //         },
    //         success: function(response) {
    //             $("#wishlist-list").html(response.data)
               
    //         }
            
    //     })

    // })
    $(document).on("click", ".delete-wishlist-product", function() {
        let wishlist_id = $(this).attr("data-wishlist-product");
        let this_val = $(this);
    
        console.log("wishlist", wishlist_id);
        $.ajax({
            url: '/remove-from-wishlist',
            data: {
                'id': wishlist_id,
            },
            dataType: 'json',
            beforeSend: function() {
                console.log("deleting products from wishlist");
            },
            success: function(response) {
                if (response && response.data) {
                    $("#wishlist-list").html(response.data);
                    console.log("Updated wishlist HTML:", response.data);
                } else {
                    console.log("Empty or invalid response from the server.");
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log("Error while making the request:", errorThrown);
            }
        });
    });
    

});



