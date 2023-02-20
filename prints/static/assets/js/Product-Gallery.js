/*---------- Product Image Gallery ----------*/

let productImage = document.querySelector(".product-des .image");
let productMain = document.querySelector(".main img");
let productAll = document.querySelectorAll(".change-btns img");

productAll.forEach(product => {

    product.addEventListener("click", () =>{

        // Active Button
        productImage.querySelector(".active").classList.remove("active");
        product.classList.add("active");

        // Active Image
        let src = product.getAttribute("src");
        productMain.src = src;
    })
})