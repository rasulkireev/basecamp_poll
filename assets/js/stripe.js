var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};

var cardElement = elements.create("card", { style: style });
cardElement.mount("#card-element");

cardElement.on('change', showCardError);

var form = document.getElementById('subscription-form');
form.addEventListener("submit", function (ev) {
  ev.preventDefault();
  stripePaymentMethod(cardElement);
});

function showCardError(event) {
  let displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
}

function stripePaymentMethod(card) {
  let billingName = "{{ user.username }}";
  console.log('starting stripePaymentMethod')
  stripe
    .createPaymentMethod({
      type: 'card',
      card: card,
      billing_details: {
        name: billingName,
      },
    })
    .then((result) => {
      if (result.error) {
        console.log("About to display error")
        showCardError(result);
      } else {
          console.log("Handling Payment")
          stripePaymentMethodHandler(result);
      }
    });
}

function stripePaymentMethodHandler(result) {
  if (result.error) {
    // Error code
    console.log("Handling Payment Error")
  } else {
    const paymentParams = {
        email: customerEmail,
        plan_id: "price_1H4864HQF19ZH0rLjubDnaZS",
        payment_method: result.paymentMethod.id,
    };
    console.log("Passing Parameters")
    fetch(createCustomerUrl, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'same-origin',
      body: JSON.stringify(paymentParams),
    }).then(function(response) {
      return response.json(); 
    }).then(function(result) {
      // todo: check and process subscription status based on the response
    }).catch(function (error) {
      // more error handling
    });
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
};

function planSelect(name, price, priceId) {
  var inputs = document.getElementsByTagName('input');

  for(var i = 0; i<inputs.length; i++){
    inputs[i].checked = false;
    if(inputs[i].name== name){

      inputs[i].checked = true;
    }
  }

  var n = document.getElementById('plan');
  var p = document.getElementById('price');
  var pid = document.getElementById('priceId');
  n.innerHTML = name;
  p.innerHTML = price;
  pid.innerHTML = priceId;
      document.getElementById("submit").disabled = false;


};
