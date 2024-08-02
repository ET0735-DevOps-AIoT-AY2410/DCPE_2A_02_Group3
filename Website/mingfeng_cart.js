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
                <td><a href="#" onclick ="deleteRow(event)"><i class="fa fa-times"></i></a></td>
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
        let taxes = subtotal * 0.08;
        let serviceCharges = subtotal * 0.10; 
        let totalExtraCharges = taxes + serviceCharges; 
        let total = subtotal + totalExtraCharges; // total cost

        // Updates HTML values with new calculated values
        document.getElementById("taxes").textContent = `${taxes.toFixed(2)}`;
        document.getElementById("serviceCharge").textContent = `${serviceCharges.toFixed(2)}`;
        document.getElementById("subtotal").textContent = `${subtotal.toFixed(2)}`;
        document.getElementById("extraCharges").textContent = `${totalExtraCharges.toFixed(2)}`;
        document.getElementById("total").textContent = `${total.toFixed(2)}` 

    } catch (error) {
        console.error("Failed to fetch products:", error);
    }
}

    displayCart();










  //HTML values updating

  /*const TaxesElement = document.getElementById("taxes");
        const servicechargeElement = document.getElementById("serviceCharge");
        const subtotalElement = document.getElementById("subtotal");
        const extrachargeElement = document.getElementById("extraCharges");
        const TotalElement = document.getElementById("total");

        function updateValues() {
            let taxcosts = taxes;
            let servicechargecosts = serviceCharges;

            TaxesElement.textContent = taxcosts.toFixed(2);
            servicechargeElement.textContent = servicechargecosts.toFixed(2);
            subtotalElement.textContent = orderSubtotal.toFixed(2);
            extrachargeElement.textContent = totalExtraCharges.toFixed(2);
            TotalElement.textContent = total.toFixed(2);
        }

        updateValues(); */

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
