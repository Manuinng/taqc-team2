## Product Planning

## Table of Contents

- [Test Case 1: Validate successful product submission with valid data](#test-case-1-validate-successful-product-submission-with-valid-data)
- [Test Case 2: Validate Failed submission with invalid data for the quantity](#test-case-2-validate-failed-submission-with-invalid-data-for-the-quantity)
- [Test Case 3: Validate functionality of the compare color](#test-case-3-validate-functionality-of-the-compare-color)
- [Test Case 4: Validate Buy with button](#test-case-4-validate-buy-with-button)
- [Test Case 5: Validate Categories button](#test-case-5-validate-categories-button)
- [Test Case 6: Validate Find Size button](#test-case-6-validate-find-size-button)
- [Test Case 7: Validate the option selected from the product in the cart](#test-case-7-validate-the-option-selected-from-the-product-in-the-cart)
- [Test Case 8: Validate the functionality of the wishlist option](#test-case-8-validate-the-functionality-of-the-wishlist-option)
- [Test Case 9: Validate the discount of the price](#test-case-9-validate-the-discount-of-the-price)

### Test Case 1: Validate successful product submission with valid data

#### Objective
Verify product selection of options and be able to add to cart.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product 
2. Select Color and Size
3. Input the quantity with "25"
4. Attempt to add to cart

#### Expected Result
Product is add to cart correctly

### Test Case 2: Validate Failed submission with invalid data for the quantity

#### Objective
Verify product quantity with a invalid value can't be add to cart

#### Preconditions
- User is on Product view
- User is logged in

#### Expected Result
Product can't be add to cart.

#### Test Case 2.1: Validate first name is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with "1e+2100"
4. Attempt to add to cart

#### Test Case 2.2: Validate last name is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with "M"
4. Attempt to add to cart

#### Test Case 2.3: Validate country is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with "0"
4. Attempt to add to cart

#### Test Case 2.4: Validate city is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with "1000000000000000000000000"
4. Attempt to add to cart

#### Test Case 2.5: Validate address is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with "-1"
4. Attempt to add to cart

#### Test Case 2.6: Validate phone number is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with 1
4. Attempt to add to cart

#### Test Case 2.7: Validate email is required
1. Select Product 
2. Select Color and Size
3. Input the quantity with " "
4. Attempt to add to cart

##### Expected Result (for all tests)
Product can't be add to cart.

### Test Case 3: Validate functionality of the compare color

#### Objective
Verify if the buttons compare color work and the functinality of this option.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product 
2. Click in compare color option
3. Remove every color that is in the pop up 
4. Attempt to add a color
5. Close the pop up

#### Expected Result

Can use the option and add or remove everytime that the user wants.

### Test Case 4: Validate Buy with button

#### Objective
Verify if the button open a pop up or redirect to the payment options.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product
2. Select option for the product
2. Click in Buy With options

#### Expected Result

Open a pop up or redirect to the correspondent option.

### Test Case 5: Validate Categories button

#### Objective
Verify if the button redirect to the categories page.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product 
2. Click in categories option

#### Expected Result

Redirection to categories page.

### Test Case 6: Validate Find Size button

#### Objective
Verify if the button open a pop up with the size information.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product 
2. Click in Find Size option

#### Expected Result

Open a pop up with the information required.

### Test Case 7: Validate the option selected from the product in the cart

#### Objective
Verify if the information for the product id correct in the cart.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product
2. Select the options for the product.
3. Add to the cart.
4. Verified the information of the product.

#### Expected Result

The information of the product match with the one of the cart.

### Test Case 8: Validate the functionality of the wishlist option

#### Objective
Verify if the product is add to the wishlist.

#### Preconditions
- User is on Product view
- User is logged in

#### Test Steps
1. Select Product
2. Click in the wishlist option
3. Go to the wishlist page.
4. Verify the product in the page.

#### Expected Result

The product is in the wishlist page.

### Test Case 9: Validate the discount of the price

#### Objective
Verify if the functionality of the discount in the price is correct

#### Preconditions
- User is on Product view

#### Test Steps
1. Select the product
2. Verify the discount price with the real price

#### Expected Result

The discount price is correct for the discount given.