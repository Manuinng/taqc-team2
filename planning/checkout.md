# Checkout Test Planning

## Test Case 1: Validate successful form submission with valid data

### Objective
Verify the checkout form submits successfully when all fields are filled with valid data

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Steps
1. Fill first name field with "first"
2. Fill last name field with "last"
3. Select Spain from the country list
4. Fill city field with "city"
5. Fill address field with "address"
6. Fill phone number field with "+987654321"
7. Fill email field with "team2@taqc.com"
8. Fill notes field with "notes"
9. Fill discount code field with "discount"
10. Fill card number field with "4242424242424242"
11. Fill card expiration date field with "12/25"
12. Fill card CVC with "123"
13. Check the terms and conditions checkbox
14. Attempt to submit the form

### Expected Result

Order placement is accepted by the website

## Test Case 2: Validate required fields

### Objective
Verify checkout form is not submitted if any required field is empty

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Case 2.1: Validate first name is required
1. Leave first name field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.2: Validate last name is required
1. Leave last name field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.3: Validate country is required
1. Do not select any country
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.4: Validate city is required
1. Leave city field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.5: Validate address is required
1. Leave address field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.6: Validate phone number is required
1. Leave phone number field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.7: Validate email is required
1. Leave email field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.8: Validate card number is required
1. Leave card number field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.9: Validate card expiration date is required
1. Leave card expiration date field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 2.10: Validate card CVC is required
1. Leave card CVC field empty
2. Fill in all other fields with valid data
3. Attempt to submit the form

#### Expected Result (for all tests)

Order placement is rejected by the website and the empty field is highlighted with an error message mentioning the field is required

## Test Case 3: Validate invalid emails are not accepted by the form

### Objective
Verify checkout form is not submitted if email is invalid

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Case 3.1: Validate email local part does not start with a special character
1. Fill email field with ".email@example.com"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 3.2: Validate email local part does not have repeat special characters
1. Fill email field with "invalid..email@example.com"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 3.3: Validate email has a top level domain
1. Fill email field with "email@example"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 3.4: Validate email top level domain does not have a special character
1. Fill email field with "email@example.c-m"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 3.5: Validate email top level domain is at least 2 characters long
1. Fill email field with "email@example.c"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Expected Result

Order placement is rejected by the website and the email field is highlighted with an error message pointing out the formatting error

## Test Case 4: Validate invalid phone numbers are not accepted by the form

### Objective
Verify checkout form is not submitted if phone number is invalid, using E.164 as the formatting standard

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Case 4.1: Validate phone number does not contain invalid characters
1. Fill phone number field with "not_a_phone_number"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 4.2: Validate phone number is at least 7 digits long
1. Fill phone number field with "+999999"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 4.3: Validate phone number is at most 15 digits long
1. Fill phone number field with "+9999999999999999"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Expected Result

Order placement is rejected by the website and the phone number field is highlighted with an error message pointing out the formatting error

## Test Case 5: Validate invalid credit card data is not accepted by the form

### Objective
Verify checkout form is not submitted if credit card data is invalid

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Case 5.1: Validate credit card number is only digits
1. Fill credit card number field with "not_a_card_number"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 5.2: Validate credit card number does not fail Luhn algorithm
1. Fill credit card number field with "0000000000000001"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 5.3: Validate credit card expiration date is a date
1. Fill credit card expiration date with "not_a_date"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 5.4: Validate credit card expiration date is valid
1. Fill credit card expiration date with "13/26"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 5.5: Validate credit card has not expired
1. Fill credit card expiration date with "12/24"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Test Case 5.6: Validate credit card cvc is only digits
1. Fill credit card cvc with "abc"
2. Fill in all other fields with valid data
3. Attempt to submit the form

### Expected Result

Order placement is rejected by the website and the invalid credit card field is highlighted with an error message pointing out the error

## Test Case 6: Validate only logged in users can access the checkout page

### Objective
Verify the user can't access the checkout page if not logged in

### Preconditions
- User is not logged in
- User has items in the cart

### Test Steps
1. Attempt to navigate to the checkout page

### Expected Result

User can't access the checkout page and instead is redirected to the login page.

## Test Case 7: Validate user can't access the checkout page with an empty cart

### Objective
Verify the user can't access the checkout page if their shopping cart is empty

### Preconditions
- User is logged in
- User has no items in the cart

### Test Steps
1. Attempt to navigate to the checkout page

### Expected Result

User can't access the checkout page and instead is shown a popup pointing out their shopping cart is empty.

## Test Case 8: Validate placed order data matches the data submitted in the checkout form

### Objective
Verify the order placed in the API matches the order sent with the checkout form

### Preconditions
- User is on the checkout page
- User is logged in
- User has items in the cart

### Test Steps
1. Fill the form with valid data and take note of it
2. Take note of the cart items data
3. Attempt to submit the form
4. Obtain the order ID from the form submission response
5. Request the order data from the orders API endpoint using the order ID obtained earlier
6. Verify the retrieved data matches the data sent when placing the order

### Expected Result

Data retrieved from API matches the data used to fill the form and the data of the cart items
