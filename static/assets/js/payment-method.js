/*---------- Payment Methods ----------*/

$(document).ready(function(){
    $(".payment label").click(function(){
     // self clicking close
     if($(this).next(".payment-body").hasClass("active")){
       $(this).next(".payment-body").removeClass("active")
     }
   else{
     $(".payment .payment-body").removeClass("active");
   }
  })
})
