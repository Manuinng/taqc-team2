# End-To-End Planning

## Table of Contents

- [Test Case 1: New user registers and successfully places an order](#test-case-1-new-user-registers-and-successfully-places-an-order)
- [Test Case 2: Existing user logs in and places an order](#test-case-2-existing-user-logs-in-and-places-an-order)
- [Test Case 3: User places an order without being logged in](#test-case-3-user-places-an-order-without-being-logged-in)
- [Test Case 4: User adds product to cart then replaces it with another product](#test-case-4-user-adds-product-to-cart-then-replaces-it-with-another-product)
- [Test Case 5: User adds two different products in separate instances](#test-case-5-user-adds-two-different-products-in-separate-instances)
- [Test Case 6: User enters wrong credit card number then corrects it](#test-case-6-user-enters-wrong-credit-card-number-then-corrects-it)

### Test Case 1: New user registers and successfully places an order

#### Objective
Verify the user flow for a new customer making a purchase, going through registration, login, product selection and placing an order.

#### Preconditions
- User is on Home Page

#### Test Steps
1. Select the account icon 
2. Select new customer option
3. Input the from for the new account
4. Click in the register button
5. Login in the account
6. Go to the Home Page
7. Select a product
8. Select the options for the product
9. Click in add to the cart option
10. Go to the checkout
11. Fill the form for the user information
12. Fill the card form
13. Place the order

#### Expected Result
The order is created correctly and validated with the backend API

### Test Case 2: Existing user logs in and places an order

#### Objective
Verify the user flow for an existing customer making a purchase, going through login, product selection and placing an order.

#### Preconditions
- User is on Home Page
- User has an account

#### Test Steps
1. Select the account icon 
2. Login in the account
3. Go to the Home Page
4. Select a product
5. Select the options for the product
6. Click in add to the cart option
7. Go to the checkout
8. Fill the form for the user information
9. Fill the card form
10. Place the order

#### Expected Result
The order is created correctly and validated with the backend API

### Test Case 3: User places an order without being logged in

#### Objective
Verify the user flow for a customer that is making a purchase without logging in, going through product selection and placing an order.

#### Preconditions
- User is on Home Page
- User isn't logged in

#### Test Steps
1. Select a product
2. Select the options for the product
3. Click in add to the cart option
4. Go to the checkout
5. Fill the form for the user information
6. Fill the card form
7. Place the order

#### Expected Result
The order is created correctly and validated with the backend API

### Test Case 4: User adds product to cart then replaces it with another product

#### Objective
Verify the user flow for a customer that at first is going to purchase a product, but then changes his/her mind and decides to purchase a different product instead, removing the first product from the cart.

#### Preconditions
- User is on Home Page
- User has an account

#### Test Steps
1. Select the account icon 
2. Login in the account
3. Go to the Home Page
4. Select a product
5. Select the options for the product
6. Click in add to the cart option
7. Go to the Home Page
8. Select a teh second product
9. Select the options for the second product
10. Click in add to the cart option
11. Remove the first product
12. Go to the checkout
13. Fill the form for the user information
14. Fill the card form
15. Place the order

#### Expected Result
The order is created correctly and validated with the backend API

### Test Case 5: User adds two different products in separate instances

#### Objective
Verify the user flow for a customer that at first is going to purchase a product, but then before placing an order decides to go back and add another product to the cart, purchasing 2 different products in 1 order.

#### Preconditions
- User is on Home Page
- User is logged in

#### Test Steps
1. Select a product
2. Select the options for the product
3. Click in add to the cart option
4. Go to the checkout
5. Fill the form for the user information
6. Fill the card form
7. Go to te home page
8. Select the second product
9. Select the options for the second product
10. Go to the checkout
11. Fill the form for the user information
12. Fill the card form
13. Place the order

#### Expected Result
The order is created correctly and validated with the backend API

### Test Case 6: User enters wrong credit card number then corrects it

#### Objective
Verify the user flow for a customer that is making a purchase but enters wrong credit card information in the checkout form, but then corrects it and completes the purchase.

#### Preconditions
- User is on Home Page
- User is logged in

#### Test Steps
1. Select a product
2. Select the options for the product
3. Click in add to the cart option
4. Go to the checkout
5. Fill the form for the user information
6. Fill the card form with wrong details
7. Place the order
8. Fill the card form with the right details
9. Place the order

#### Expected Result
The order is not placed with the wrong credit card number at first, but then once the correct number is entered the order is placed correctly and validated with the backend API
