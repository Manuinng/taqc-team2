## End-To-End Planning

## Table of Contents

- [Test Case 1: Success Order PLace with registration in the website](#test-case-1-success-order-place-with-registration-in-the-website)
- [Test Case 2: Place an order with an user that have account](#test-case-2-place-an-order-with-an-user-that-have-account)
- [Test Case 3: Place an order with an user that isn't Login](#test-case-3-place-an-order-with-an-user-that-isnt-login)
- [Test Case 4: Select different product but eliminate one in the last check](#test-case-4-select-different-product-but-eliminate-one-in-the-last-check)

### Test Case 1: Success Order PLace with registration in the website

#### Objective
Verify the flow for a new customer with the registration, login, selection of product and the place an order.

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
The order is created and validate

### Test Case 2: Place an order with an user that have account

#### Objective
Verify the flow for a customer already register.

#### Preconditions
- User is on Home Page
- User have an account

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
The order is created and validate for the account

### Test Case 3: Place an order with an user that isn't Login 

#### Objective
Verify the flow for a customer that isn't Login

#### Preconditions
- User is on Home Page
- User isn't login

#### Test Steps
1. Select a product
2. Select the options for the product
3. Click in add to the cart option
4. Go to the checkout
5. Fill the form for the user information
6. Fill the card form
7. Place the order

#### Expected Result
The order is created and validate but without the account

### Test Case 4: Select different product but eliminate one in the last check

#### Objective
Verify the flow for a customer that have not decide clearly what buy

#### Preconditions
- User is on Home Page
- User have an account

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
The order is created and validate for the account