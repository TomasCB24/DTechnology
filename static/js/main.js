console.log('Sanity check!')

// Get Stripe publishable key
fetch("/payments/config/")
.then((result) => { return result.json() })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey)

  // Event handler
  setTimeout(() => {
      // Get Checkout Session ID
      fetch("/payments/create-checkout-session/")
      .then((result) => { return result.json() })
      .then((data) => {
        console.log(data)
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId, })
      })
      .then((res) => {
        console.log(res)
      })
  }, 10000)
})

