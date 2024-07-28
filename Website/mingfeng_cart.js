import Api from "./api.js"
let api = new Api("https://supermarket-backend-xvd6lpv32a-uc.a.run.app/")



function setCookie(name, value, exdays) {
    const date = new Date();
    date.setTime(date.getTime() + (exdays * 24 * 60 * 60 * 1000));  // Sets expiration date by adding the number of days in milliseconds
    let expires = "expires= " + date.toUTCString();  // Converts expiration date to UTC string format
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
  }

let cart = [{"itemID": 1 , "price": 2.0 , "quantity": 3 }];
//let cart = [{"name": "Capsicum", "price": 6.0, "quantity": 3}]
setCookie("cart", JSON.stringify(cart), 5);

function getCookie(name) {
    let cstr = name + "="; // cstr = cookie string
    let cookiearray = document.cookie.split(';');

    for(let i = 0; i < cookiearray.length; i++) {
      let c = cookiearray[i]; // c is defined as the cookie

      while (c.charAt(0) == ' ') { // checks and removes empty spaces in cookie
        c = c.substring(1);
      }
      if (c.indexOf(cstr) == 0) {
        return c.substring(cstr.length, c.length); // returns cookie value
      }
    }
    return "";
  }

async function displayCart(){
    let orders = getCookie("cart");

    if (!orders){
        console.log("Cookie not found")
        return;
    }
    try {
        orders = JSON.parse(orders);
        let products = await api.getProducts(); // obtain products data
        let productslist = document.getElementById('order-list');
        let subtotal = 0;

        for (let order of orders) {
            let product = products.find(p => p.id == order.itemID); // searches for itemID in products
            console.log(product);
            if (product) {
                
                let orderSubtotal = parseFloat(order.price) * parseFloat(order.quantity);
                subtotal += orderSubtotal;

                let orderCart = document.createElement('tr');
                orderCart.innerHTML = `
                <td><a href="#"><i class="fa fa-times"></i></a></td>
                <td><img src="${product.img}" alt=''></td>
                <td><h5>${product.name}</h5></td>
                <td><h5>$${order.price}</h5></td>
                <td><h5>${order.quantity}</h5></td>
                <td><h5>$${orderSubtotal.toFixed(2)}</h5></td> 
                `;

                productslist.appendChild(orderCart);
                console.log(orderCart)
            }
            else {
                console.error('Product with itemID ${order.itemID} not found');
            }

        }

        //calculating extra charges values
        /* let taxes = orderSubtotal * 0.08;
        let serviceCharges = orderSubtotal * 0.10; 
        let totalExtraCharges = taxes + serviceCharges; 
        let total = subtotal + totalExtraCharges + delivery; // total cost
        
        const TaxesElement = document.getElementById("taxes");
        const servicechargeElement = document.getElementById("serviceCharge");
        const subtotalElement = document.getElementById("subtotal");
        const extrachargeElement = document.getElementById("extraCharges");
        const TotalElement = document.getElementById("total");

        function updateValues() {
            let taxCosts = taxes;
            let servicechargeCosts = serviceCharges; 
            let ExtraCosts = totalExtraCharges;
            let subTotal = orderSubtotal;
            let finalTotal = total;

            TaxesElement.textContent = taxCosts.toFixed(2);
            servicechargeElement.textContent = servicechargeCosts.toFixed(2);
            subtotalElement.textContent = subTotal.toFixed(2);
            extrachargeElement.textContent = ExtraCosts.toFixed(2);
            TotalElement.textContent = finalTotal.toFixed(2);
        }

        updateValues(); */

        
    // Updates HTML values with new calculated values
    document.getElementById('taxes').innerText = `$${taxes.toFixed(2)}`;
    document.getElementById('serviceCharge').innerText = `$${serviceCharges.toFixed(2)}`;
    document.getElementById('subtotal').innerText = `$${subtotal.toFixed(2)}`;
    document.getElementById('extraCharges').innerText = `$${totalExtraCharges.toFixed(2)}`;
    document.getElementById("total").innerText = `$${total.toFixed(2)}`
    document.querySelector('.total h6:nth-of-type(2) + p').innerText = `$${delivery.toFixed(2)}`; 
    } catch (error) {
        console.error("Failed to fetch products:", error);
    }
}


document.addEventListener("DOMContentLoaded", function() {
    displayCart();
  });



/*async function displayorders(){
    try {
        let orders = await api.getOrders();
        orderslist = document.getElementById('order-list');

        orders.forEach(order => {
            let orderslist = ''; 
            orderslist.innerHTML = `
                <tr>
                    <td><a href="#"><i class="fa fa-times"></i></a></td>
                    <td><img src="${order.img}" alt=''></td>
                    <td><h5>${order.name}</h5></td>
                    <td><h5></h5></td>
                </tr>
        
            `;
             

        })
    } catch (error){

    } 
} */
