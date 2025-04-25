# Home Flow Test Planning

## Table of Contents
- [Test Case 1: Validate Quick View with all options selected](#test-case-1-validate-quick-view-with-all-options-selected)
- [Test Case 2: Validate Quick Add without selecting options](#test-case-2-validate-quick-add-without-selecting-options)
- [Test Case 3: Validate Quick View with partial options selected](#test-case-3-validate-quick-view-with-partial-options-selected)
- [Test Case 4: Validate Quick Add with all options selected](#test-case-4-validate-quick-add-with-all-options-selected)
- [Test Case 5: Validate Quick View fails without required options](#test-case-5-validate-quick-view-fails-without-required-options)
- [Test Case 6: Validate Quick Add with invalid quantity](#test-case-6-validate-quick-add-with-invalid-quantity)
- [Test Case 7: Validate Quick View handles extreme quantity](#test-case-7-validate-quick-view-handles-extreme-quantity)
- [Test Case 8: Validate Quick Add with multiple cart actions](#test-case-8-validate-quick-add-with-multiple-cart-actions)
- [Test Case 9: Validate Quick View fails with invalid quantity](#test-case-9-validate-quick-view-fails-with-invalid-quantity)

---

## Test Case 1: Validate Quick View with all options selected

### Objective
Verify that users can add a product to the cart using **Quick View**, ensuring all required selections are made.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick View** for a product.  
5. Select **color, size, and quantity**.  
6. Click **"Find Your Size"**.  
7. Add the product to **wishlist**.  
8. Add the product to **cart**.  
9. Interact with the cart (**adjust quantity, add notes**).  

### Expected Result
✅ The product is added to the cart with the correct options, and all cart interactions function properly.

---

## Test Case 2: Validate Quick Add without selecting options

### Objective
Verify that users **cannot add** a product to the cart using **Quick Add** without selecting any required options.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick Add** for a product.  
5. Attempt to **add the product to the cart** **without selecting options**.  
6. Try **adjusting the quantity in the cart**.

### Expected Result
✅ The system **blocks the addition** or displays an **error message**, preventing users from adding a product without required selections.

---

## Test Case 3: Validate Quick View with partial options selected

### Objective
Verify that users can add a product using **Quick View** with only **some** options selected.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick View** for a product.  
5. Select **only the color**.  
6. Add the product to **cart**.  
7. Interact with the cart (**estimate shipping**).  

### Expected Result
✅ The product is added with the selected options, and cart interactions work correctly.

---

## Test Case 4: Validate Quick Add with all options selected

### Objective
Verify that users can add a product to the cart using **Quick Add** while selecting all necessary options.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick Add** for a product.  
5. Select **color, size, and quantity**.  
6. Add the product to the **cart**.  
7. Interact with the cart (**add notes**).  

### Expected Result
✅ The product is added with the correct selections, and cart interactions function properly.

---

## Test Case 5: Validate Quick View fails without required options

### Objective
Verify that the system **does not allow** adding a product to the cart through **Quick View** without selecting required options.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick View** for a product.  
5. Attempt to add the product to **cart** **without selecting required options**.  

### Expected Result
✅ The system **blocks the addition** or displays an **error message**.

---

## Test Case 6: Validate Quick Add with invalid quantity

### Objective
Verify that the system correctly **handles invalid quantity entries** when adding a product via **Quick Add**.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick Add** for a product.  
5. Select **color and size**.  
6. Enter an **invalid quantity** (e.g., **-20**).  
7. Attempt to add the product to **cart**.  

### Expected Result
✅ The system **blocks the action** or displays an **error message**.

---

## Test Case 7: Validate Quick View handles extreme quantity

### Objective
Verify that Quick View correctly adds a product with an **extremely high quantity**.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick View** for a product.  
5. Select **color, size, and quantity** (e.g., **1000 items**).  
6. Add the product to **cart**.  
7. Interact with the cart (**adjust quantity**).  

### Expected Result
✅ The system processes the request successfully, handling large quantities.

---

## Test Case 8: Validate Quick Add with multiple cart actions

### Objective
Verify that users can **perform multiple actions in the cart** after adding a product using **Quick Add**.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick Add** for a product.  
5. Select **color, size, and quantity**.  
6. Add the product to the **cart**.  
7. Perform multiple interactions with the cart:  
   - **Adjust quantity**  
   - **Add notes**  
   - **Estimate shipping**  

### Expected Result
✅ All cart interactions function correctly after the product is added.

---

## Test Case 9: Validate Quick View fails with invalid quantity

### Objective
Verify that Quick View **blocks adding a product** with an invalid quantity.

### Preconditions
- User is on the **Home page**.

### Test Steps
1. Navigate to the **Home page**.  
2. Close the **newsletter popup**.  
3. Scroll down to view products.  
4. Open **Quick View** for a product.  
5. Select **color, size, and quantity** (e.g., **-1 items**).  
6. Attempt to add the product to **cart**.  

### Expected Result
✅ The system **blocks the action** or displays an **error message**.

---