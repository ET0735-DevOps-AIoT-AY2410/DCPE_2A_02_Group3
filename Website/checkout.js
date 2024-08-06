import Api from "./api.js"
let api = new Api("https://supermarket-backend-xvd6lpv32a-uc.a.run.app")

function setCookie(name, value, exdays) {
    const date = new Date();
    date.setTime(date.getTime() + (exdays * 24 * 60 * 60 * 1000));  // Sets expiration date by adding the number of days in milliseconds
    let expires = "expires= " + date.toUTCString();  // Converts expiration date to UTC string format
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
  }

// let cart = [{"itemID": 1 , "price": 2.0 , "quantity": 3 }];

// setCookie("cart", JSON.stringify(cart), 5);
function createOrder(){
  if (document.getElementById("delivery-checkbox").checked){
  if (!validateCard()){
    document.getElementById("hint").style.display="block"
    return
  }
  }
  let cart=JSON.parse(getCookie("cart"))
  let newc=[]
  cart.forEach(element => {
    newc.push({"itemId":parseInt(element["itemID"]), "amount": parseInt(element["quantity"])})
  });
  console.log(
    newc
  )
  document.getElementById("pay").disabled=true;
  document.getElementById("spinner").style.display="block"
  api.createOrders(document.getElementById("delivery-checkbox").checked? 1:0, newc).then(
    response=>{
      setCookie("cart",[],365)
      addtoOrder(parseInt(response.orderId))
      if (document.getElementById("delivery-checkbox").checked){
        window.location="index.html"
      }else{
      window.location="qrcode.html?id="+response.orderId
    }
    }
  )
  
}
function addtoOrder(orderid) {
  orders.push(orderid)
  setCookie("orders", JSON.stringify(orders), 365)
}
function validateCard() {
  let number=document.getElementById("card").value
  var regex = new RegExp("^[0-9]{16}$");
  if (!regex.test(number))
      return false;

  return luhnCheck(number);
}

function luhnCheck(val) {
  var sum = 0;
  for (var i = 0; i < val.length; i++) {
      var intVal = parseInt(val.substr(i, 1));
      if (i % 2 == 0) {
          intVal *= 2;
          if (intVal > 9) {
              intVal = 1 + (intVal % 10);
          }
      }
      sum += intVal;
  }
  return (sum % 10) == 0;
}
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
  let orders;
  function configorders(){
    orders=getCookie("orders")
    if (orders==""){
      setCookie("orders", JSON.stringify([]),365)
    }else{
      orders=JSON.parse(orders)
    }
  }
  async function showReview() {
    document.getElementById("delivery-checkbox").onchange=()=>{
      console.log(document.getElementById("delivery-checkbox").checked)
      if (document.getElementById("delivery-checkbox").checked){
      document.getElementById("creditcard-text").style.display="block"
      document.getElementById("creditcard").style.display="block"
    }else{
      document.getElementById("creditcard-text").style.display="none"
      document.getElementById("hint").style.display="none"
      document.getElementById("creditcard").style.display="none"
    }
    };
    configorders()
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
        document.getElementById("pay").onclick=createOrder
    
  } catch (error) {
    console.error("Failed to fetch products:", error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
  showReview();
});
