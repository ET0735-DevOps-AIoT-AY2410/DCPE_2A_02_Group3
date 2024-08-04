import Api from "./api.js";

// Instantiate the Api class
let api = new Api("https://supermarket-backend-xvd6lpv32a-uc.a.run.app/");

// Function to display items on the page

let allProducts={};
// Function to filter and display items based on search query
function searchItems() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const filteredItems = items.filter(item => item.name.toLowerCase().includes(query));
    displayItems(filteredItems);
}


function initalise(){
    displayProducts();

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
            productElement.onclick=()=>{window.location.href = `product.html?id=${product.id}`}
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
