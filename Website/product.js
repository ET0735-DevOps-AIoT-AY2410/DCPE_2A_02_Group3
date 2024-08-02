let api;
let cart=[];
let products;
function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
async function setup(){
    products=(await api.getProducts())
    let pid=getParameterByName("id")

    for (id in products){

        if (parseInt(products[id].id)==parseInt(pid)){

            setfields(products[id])
            return
        }
    }
    configcooke()
}
function setfields(product){
    document.getElementById("product-name").textContent=product.name
    document.getElementById("product-img").src=product.imageUrl
    document.getElementById("quantity").max=product.quantity
}

function updateCart(){
    console.log(cart)
    setCookie("cart",JSON.stringify(cart),365);
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
}
return "";
}
function configcooke(){
    cart=getCookie("cart")
    if (cart==""){
        setCookie("cart",JSON.stringify([]),365);
    }
    cart=JSON.parse(getCookie("cart"))

}
// Function to add an item to the cart
function addToCart(itemid,quantity) {
    for (let id = 0; id<cart.length; id++){
        if (cart[id]["itemId"]==itemid){
            cart[id]["quantity"]=quantity
            updateCart()
            return
        }
    }
    for (let id = 0; id<products.length; id++){
        if (products[id]["id"]==itemid){
            cart.push({"itemId": itemid,"price": products[id]["price"], "quantity": quantity})
            updateCart();
            break
        }
    }
}
function clicked(){
    let pid=getParameterByName("id")
    addToCart(pid, document.getElementById("quantity").value)
    window.location.href = "index.html";
}