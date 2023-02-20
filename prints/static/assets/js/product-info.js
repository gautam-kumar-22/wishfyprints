/*---------- Product Information ----------*/

var productTabs = document.querySelector('.product-info .product-info-tabs');

productTabs.addEventListener('click', function(e){

    if(e.target.classList.contains('info-btn') && !e.target.classList.contains('active')){
        
        var target = e.target.getAttribute('data-target');
        productTabs.querySelector('.active').classList.remove('active');
        e.target.classList.add('active');

        var productSection = document.querySelector('.product-info');
        productSection.querySelector('.product-info-gallery.active').classList.remove('active');
        productSection.querySelector(target).classList.add('active');

    }
})