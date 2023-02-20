/*---------- Faqs Accordion ----------*/
$(document).ready(function(){
  
    $(".accordion").click(function(){

      // self clicking close
      if($(this).hasClass("active")){
        $(this).removeClass("active");
        $(this).find("i").removeClass("fa-minus").addClass("fa-plus")	
      }

      else{
        $(".accordion").removeClass("active");
        $(".accordion .accordion-heading i").removeClass("fa-minus").addClass("fa-plus");
        $(this).addClass("active");
        $(this).find("i").removeClass("fa-plus").addClass("fa-minus")
      }
    })
  })