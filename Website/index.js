
// Instantiate the Api class
let api;

// Function to display items on the page

let allProducts={};
// Function to filter and display items based on search query
function searchItems() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const filteredItems = allProducts.filter(item => item.name.toLowerCase().includes(query));
    showitems(filteredItems);
}


function initalise(){
    displayProducts();

}

// Function to fetch and display products from an API
async function displayProducts() {
    try {
        let products = await api.getProducts(); 
        console.log(products)
        allProducts=products
        showitems(products)
        
    } catch (error) {
        console.error("Failed to fetch products:", error); // Logs an error if the request fails
    }
}
function showitems(products){
    let productsContainer = document.getElementById('items-container');
    productsContainer.innerHTML = '';
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

}


// Initial display of items


