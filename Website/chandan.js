import Api from "./api.js"
let api=new Api("http://localhost:5000")

function displayItems(filteredItems) {
    const itemsContainer = document.getElementById('items-container');
    itemsContainer.innerHTML = '';

    filteredItems.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';

        itemDiv.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p>${item.price}</p>
            <input type="number" class="quantity-input" value="1" min="1">
            <button onclick="addToCart('${item.name}')">Add to Cart</button>
        `;

        itemsContainer.appendChild(itemDiv);
    });
}

function displayItems(filteredItems) {
    const itemsContainer = document.getElementById('items-container');
    itemsContainer.innerHTML = '';

    filteredItems.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';

        itemDiv.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <h3>${item.name}</h3>
            <p>${item.price}</p>
            <input type="number" class="quantity-input" value="1" min="1">
            <button onclick="addToCart('${item.name}')">Add to Cart</button>
        `;

        itemsContainer.appendChild(itemDiv);
    });
}

function searchItems() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const filteredItems = items.filter(item => item.name.toLowerCase().includes(query));
    displayItems(filteredItems);
}

function addToCart(itemName) {
    alert(`${itemName} added to cart!`);
}

async function displayProducts() {
    try {
        let products = await api.getProducts(); // Fetches the products using the Api class
        let productsContainer = document.getElementById('products-container'); // Gets the container element where products will be displayed
        productsContainer.innerHTML = ''; // Clears the container

        products.forEach(product => {
            let productElement = document.createElement('div'); // Creates a new div element for each product
            productElement.innerHTML = `
                <div class="product">
                    <img src="${product.img}" alt="${product.name}">
                    <h2>${product.name}</h2>
                    <p>${product.price}</p>
                </div>
            `; // Sets the inner HTML of the div to display the product details
            productsContainer.appendChild(productElement); // Appends the product element to the container
        });
    } catch (error) {
        console.error("Failed to fetch products:", error); // Logs an error if the request fails
    }
}
// Initial display of items
displayItems(items)
