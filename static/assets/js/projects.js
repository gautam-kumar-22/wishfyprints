$(document).ready(function(){

    $(".projects .button").click(function(){
        $(this).addClass("active").siblings().removeClass("active");

        var filter = $(this).attr("data-filter");
    
        if (filter == "all"){
            $(".projects .image").show(400);
        }
        else{
            $(".projects .image").not("."+filter).hide(200);
            $(".projects .image").filter("."+filter).show(400);
        }
    })

    //MAGNIFIC-POPUP
    $(".projects").magnificPopup({
        
        delegate: ".view",
        type: "image",
        removalDelay: 500, //delay removal by X to allow out-animation
        gallery:{
            enabled: true
        },

    })


});