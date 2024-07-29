import Api from "./api.js";

// Instantiate the Api class
let api = new Api("https://supermarket-backend-xvd6lpv32a-uc.a.run.app/");

// Function to display items on the page
let cart=[];
let allProducts={};
// Function to filter and display items based on search query
function searchItems() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const filteredItems = items.filter(item => item.name.toLowerCase().includes(query));
    displayItems(filteredItems);
}


function updateCart(){
    console.log(cart)
    setCookie("cart",JSON.stringify(cart),365);
}

// Function to add an item to the cart
function addToCart(itemid) {
    for (let id = 0; id<cart.length; id++){
        if (cart[id]["itemId"]==itemid){
            cart[id]["quantity"]+=1
            updateCart()
            return
        }
    }
    for (let id = 0; id<allProducts.length; id++){
        if (allProducts[id]["id"]==itemid){
            cart.push({"itemId": itemid,"price": allProducts[id]["price"], "quantity":1})
            updateCart();
            break
        }
    }
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
    console.log(cart)
}
function initalise(){
    displayProducts();
    configcooke();
}

// Function to fetch and display products from an API
async function displayProducts() {
    try {
        let products = await api.getProducts(); // Fetches the products using the Api class
        let productsContainer = document.getElementById('items-container'); // Gets the container element where products will be displayed
        productsContainer.innerHTML = ''; // Clears the container
        allProducts=products

        products.forEach(product => {
            let productElement = document.createElement('div'); // Creates a new div element for each product
            productElement.className="item"
            productElement.onclick=()=>{addToCart(product.id)}
            productElement.innerHTML = `
                <img src="${product.imageUrl}" alt="${product.name}">
                <p>${product.name}</p>
                <p>$${parseFloat(product.price).toFixed(2)}</p>
            `; // Sets the inner HTML of the div to display the product details
            productsContainer.appendChild(productElement); // Appends the product element to the container
        });
    } catch (error) {
        console.error("Failed to fetch products:", error); // Logs an error if the request fails
    }
}


// Initial display of items

initalise()
