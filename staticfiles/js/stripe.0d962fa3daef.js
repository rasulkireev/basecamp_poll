
// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys

const STRIPE_PUBLIC_KEY = JSON.parse(document.getElementById('STRIPE_PUBLIC_KEY').textContent);

var stripe = Stripe(STRIPE_PUBLIC_KEY);
var elements = stripe.elements();

