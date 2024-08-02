import Api from "./api.js"
let api = new Api("https://supermarket-backend-xvd6lpv32a-uc.a.run.app/")

function setCookie(name, value, exdays) {
    const date = new Date();
    date.setTime(date.getTime() + (exdays * 24 * 60 * 60 * 1000));  // Sets expiration date by adding the number of days in milliseconds
    let expires = "expires= " + date.toUTCString();  // Converts expiration date to UTC string format
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
  }

// let cart = [{"itemID": 1 , "price": 2.0 , "quantity": 3 }];

// setCookie("cart", JSON.stringify(cart), 5);

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

  async function showReview() {
    let reviews = getCookie("cart");

    if (!reviews){
        console.log("Cookie not found")
        return;
    }
    try {
        reviews = JSON.parse(reviews);
        let products = await api.getProducts(); // obtain products data
        let productslist = document.getElementById('cart-review');
        let subtotal = 0; 

        for (let review of reviews) {
            let product = products.find(p => p.id == review.itemID);
            console.log(product)

            if (product) {
                let orderSubtotal = parseFloat(review.price) * parseFloat(review.quantity);
                subtotal += orderSubtotal;

                let reviewCart = document.createElement('div');
                reviewCart.innerHTML = `
                    <div class="d-flex justify-content-between">
                        <h6>X${review.quantity}</h6>
                        <h6>${product.name}</h6>
                        <p>$${review.price.toFixed(2)}</p>
                    </div>
                `;

                productslist.appendChild(reviewCart);
                console.log(reviewCart)
            }
            else {
                console.error('Product with itemID ${order.itemID} not found');
            }
        }

        //calculate HTML values
        let taxes = subtotal * 0.08;
        let serviceCharges = subtotal * 0.10; 
        let newTotal = subtotal + taxes + serviceCharges;
        let deliveryFee = 3.00;

        const carttotalElement = document.getElementById("cart-total");
        const deliveryFeeElement = document.getElementById("delivery-fees");
        const totalElement = document.getElementById("total");

        const deliveryCheckbox = document.getElementById("delivery-checkbox");

        function updateTotal() {
            let deliveryCost = deliveryCheckbox.checked ? deliveryFee : 0.00;
            let total = newTotal + deliveryCost;
            let carttotal = newTotal; 

            carttotalElement.textContent = carttotal.toFixed(2);
            deliveryFeeElement.textContent = deliveryCost.toFixed(2);
            totalElement.textContent = total.toFixed(2);
        } 

        deliveryCheckbox.addEventListener("change", updateTotal); //calls function when checkbox is checked
        updateTotal();
    
  } catch (error) {
    console.error("Failed to fetch products:", error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
  showReview();
});
