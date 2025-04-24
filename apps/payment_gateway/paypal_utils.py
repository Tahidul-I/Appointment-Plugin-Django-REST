import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def pypal_payment(amount):
    # Customize this with actual data
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/api/v1/paypal-success/",  # PayPal will redirect to this URL after approval
            "cancel_url": "http://localhost:8000/"  # Redirect on cancel
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Test Item",
                    "sku": "12345",
                    "price": f"{amount}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": f"{amount}",
                "currency": "USD"
            },
            "description": "Payment for Test Item"
        }]
    })

    if payment.create():
        # Find and return the approval URL
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return approval_url
    else:
        print("**************************** PAYMENT CREATION FAILED *******************************")
        print(payment.error)  # Print the error for debugging
        return None