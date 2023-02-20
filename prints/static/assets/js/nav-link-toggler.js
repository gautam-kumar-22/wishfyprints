/*---------- Mobile-Navbar Nav Toggler ----------*/

$(document).ready(function(){
  
    $(".main-nav-link").click(function(){
      // self clicking close
      if($(this).hasClass("active")){
        $(this).removeClass("active");
        $(this).next(".sub-nav-link").removeClass("active").slideUp()
        $(this).find("i").removeClass("fa-minus").addClass("fa-plus")	
      }

      else{
        $(".nav-link .main-nav-link").removeClass("active");
        $(".nav-link .sub-nav-link").removeClass("active").slideUp()
        $(".nav-link .main-nav-link i").removeClass("fa-minus").addClass("fa-plus");
        $(this).addClass("active");
        $(this).next(".sub-nav-link").addClass("active").slideDown()
        $(this).find("i").removeClass("fa-plus").addClass("fa-minus")
      }
    })
  })