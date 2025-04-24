from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_payment_for_plugin(user_id):
    try:
        amount = 15 * 100  # Amount in cents
        currency = 'usd'  # Default currency is USD
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Example Product',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/api/v1/payment-success-for-plugin/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/cancel',
            metadata={
                'transaction_id': 1234567890,  
                'user_id': user_id, 
            }
        )

        return session.url

    except Exception as e:
        return None
    


def generate_stripe_connect_account_url(email):

    account = stripe.Account.create(
        type='express',  # Change from 'express' to 'standard'
        country='US',
        email= f"{email}",
        # Additional fields can be added as needed
    )


    print("***********************************************************************")
    print(account)
    # Create an AccountLink for the user to complete their onboarding
    account_link = stripe.AccountLink.create(
        account=account.id,
        refresh_url='https://simpleisbetterthancomplex.com/references/2016/06/21/date-filter.html',  # URL to redirect if user exits midway through onboarding
        return_url='https://docs.stripe.com/api/account_links/create?lang=python',  # URL to redirect upon successful onboarding
        type='account_onboarding'
    )
    print(account_link)
    # Return both the Connect account ID and the onboarding URL
    return {
        'account_id': account.id,  # Connect account ID to store in your database
        'url': account_link.url  # URL to send to the user for onboarding
    }




     