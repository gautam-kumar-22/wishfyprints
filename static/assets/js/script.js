$(document).ready(function(){

    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    };

  $('.scroll-top').hide();
  
  /*---------- Mobile-Navbar Toggler ----------*/
  let sideBar = document.querySelector('.mobile-menu');

  document.querySelector('.header #menu-btn').onclick = () =>{
      sideBar.classList.add('active');
  }
 
  document.querySelector('#close-side-bar').onclick = () =>{  
      sideBar.classList.remove('active');
      $(".nav-link .main-nav-link").removeClass("active");
      $(".nav-link .sub-nav-link").removeClass("active").slideUp()
      $(".nav-link .main-nav-link i").removeClass("fa-minus").addClass("fa-plus");
  }
  
  // On Load/Scroll
  $(window).on('load scroll',function(){
    sideBar.classList.remove('active');
    $(".nav-link .main-nav-link").removeClass("active");
    $(".nav-link .sub-nav-link").removeClass("active").slideUp()
    $(".nav-link .main-nav-link i").removeClass("fa-minus").addClass("fa-plus");	

    /*--------------- Sticky Header ---------------*/
    if($(window).scrollTop() > 68){
      $('header .header-2').addClass('active');
    }else{
      $('header .header-2').removeClass('active');
    }

    /*--------------- Scroll-Top ---------------*/
    if ($(this).scrollTop() > 100) {
      $('.scroll-top').fadeIn();
    } else {
      $('.scroll-top').fadeOut();
    }

  
  });

    // shipping-billing-address-manage
    $(document).ready(function(){
        if($("#is_billing_same").prop('checked') == true){
            $(".billing_address").hide();
        }

        if($("#is_billing_same").click(function(){
         if($(this).prop('checked') == true){
            $(".billing_address").hide();
         }else{
            $(".billing_address").show();
         }
        }));

        // list view and grid view setting
        $(".grid").hide();
        var location = window.location.href;
        if (location.indexOf('grid') > -1){
            $(".list").hide();
            $(".grid").show();
            $("#grid-view").addClass("active");
            $("#list-view").removeClass("active");
        }
        if (location.indexOf('list') > -1){
            $(".grid").hide();
            $(".list").show();
            $("#list-view").addClass("active");
            $("#grid-view").removeClass("active");
        }

        $("#list-view").click(function(){
            $(".grid").hide();
            $(".list").show();
            $("#list-view").addClass("active");
            $("#grid-view").removeClass("active");
            var location = window.location.href;
            if (location.indexOf('view') > -1){
                location = location.replace("grid", "list");
            }else{
                if (location.indexOf('?') > -1){
                    location += "&view=list";
                }else{
                    location += "?view=list";
                }
            }
            window.location.href = location;
        });

        $("#grid-view").click(function(){
            $(".list").hide();
            $(".grid").show();
            $("#grid-view").addClass("active");
            $("#list-view").removeClass("active");
            var location = window.location.href;
            if (location.indexOf('view') > -1){
                location = location.replace("list", "grid");
            }else{
                if (location.indexOf('?') > -1){
                    location += "&view=grid";
                }else{
                    location += "?view=grid";
                }
            }
            window.location.href = location;
        });

        // Apply sorting
        $("#sort").change(function(){
            var val = ($(this).val()).split(",");
            var location = window.location.href;
            var sortby = val[0];
            var orderby = val[1];
            var category_name = "";
            var view = "";
            urls = location.split("?");
            endpoint = urls[0];
            if(location.indexOf('&') > -1){
                parameters = urls[1].split("&");
                for(var i=0; i<parameters.length; i++){
                    console.log(parameters[i]);
                    if (parameters[i].indexOf('category') > -1){
                        category_name = parameters[i].split("=")[1]
                    }
                    if (parameters[i].indexOf('view') > -1){
                        view = parameters[i].split("=")[1]
                    }
                }
            }
            if((sortby != "default") && (orderby != "default")){
                location = "?sortby=" + sortby + "&orderby=" + orderby;
            }else{
                location = "";
            }

            if (category_name){
                if(location){
                    location +=  "&category=" + category_name;
                }else{
                    location +=  "?category=" + category_name;
                }
            }
            if (view){
                if(location){
                    location +=  "&view=" + view;
                }else{
                    location +=  "?view=" + view;
                }
            }

            window.location.href = location;
        });

        var location = window.location.href;
        if ((location.indexOf('name') > -1) && ((location.indexOf('asc') > -1))){
            $("#sort").val("name,asc");
        }
        if ((location.indexOf('name') > -1) && ((location.indexOf('desc') > -1))){
            $("#sort").val("name,desc");
        }
        if ((location.indexOf('price') > -1) && ((location.indexOf('asc') > -1))){
            $("#sort").val("price,asc");
        }
        if ((location.indexOf('price') > -1) && ((location.indexOf('desc') > -1))){
            $("#sort").val("price,desc");
        }

        // Delete from cart
        $(".delete-cart").click(function(){
            if(confirm("Are you sure, you want to remove from cart?")){
                return true;
            }else{
                return false;
            }
        });

        // Delete from wishlist
        $(".delete-wishlists").click(function(){
            if(confirm("Are you sure, you want to remove from wishlist?")){
                return true;
            }else{
                return false;
            }
        });
    });

  // success-alert
        $(".alert-success").fadeTo(5000, 500).slideUp(500, function() {
            $(".alert-success").slideUp(500);
        });

    // Wishlist add button
    $(".add-wishlist").click(function(){
        var href = $(this).attr("href");
        if(href){
            $.ajax(href, {
               type: 'GET',
                success: function (data, status) {
                    console.log(data);
                    if(data.status == 302){
                        window.location.href = "/login/?next="+window.location.pathname;
                    }
                    else{
                        toastr.info(data.message);
                        return false;
                    }
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    // console.log(status);
                }

            });
            return false;
        }
    });

});


