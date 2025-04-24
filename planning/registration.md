# TAQC Team Test Planning - User Registration

## Table of Contents
1. [Validate Successful Registration with Valid Data](#test-case-1-validate-successful-registration-with-valid-data)
2. [Validate Required Fields](#test-case-2-validate-required-fields)
3. [Validate Invalid Emails Are Not Accepted](#test-case-3-validate-invalid-emails-are-not-accepted)
4. [Validate Invalid Names Are Not Accepted](#test-case-4-validate-invalid-names-are-not-accepted)
5. [Validate Invalid Passwords Are Not Accepted](#test-case-5-validate-invalid-passwords-are-not-accepted)
6. [Validate Registration Fails with All Fields Missing](#test-case-6-validate-registration-fails-with-all-fields-missing)

---

## Test Case 1: Successful Registration with Valid Data


### Objective
Verify the registration form submits successfully when all required fields are filled with valid data.

### Preconditions
- User is on the registration page.

### Test Steps
1. Fill first name field with **"FirstName"**  
2. Fill last name field with **"LastName"**  
3. Fill email field with **"test9999@example.com"**  
4. Fill password field with **"12345"**  
5. Click the **"Register"** button  

### Expected Result
✅ Registration is completed successfully, and the user is redirected to the **my-account/dashboard page**.

---

## Test Case 2: Email Validation Failures

### Objective
Ensure registration fails with invalid or malformed emails.

### Preconditions
- User is on the registration page.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **2.1: Invalid email** | `"invalidemail"` | ❌ Registration should fail (**✅ PASS**) |
| **2.2: Empty email** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **2.3: Email with spaces** | `"test @domain.com"` | ❌ Registration should fail (**✅ PASS**) |
| **2.4: Invalid email format** | `"a@a"` | ❌ Should fail but passes (**❌ FAILED**) |
| **2.5: Duplicate email** | **Already registered email** | ❌ Registration should fail (**✅ PASS**) |
| **2.6: Email with special characters** | `"test!@domain.com"` | ❌ Should fail but passes (**❌ FAILED**) |
| **2.7: Email missing domain** | `"test@"` | ❌ Registration should fail (**✅ PASS**) |
| **2.8: Very long email** | **String > 256 characters** | ❌ Should fail but passes (**❌ FAILED**) |

---

## Test Case 3: Name Validation Failures

### Objective
Ensure registration fails when name fields are invalid.

### Preconditions
- User is on the registration page.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **3.1: Empty first name** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **3.2: Empty last name** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **3.3: Special characters in name** | `"First@Name"` | ❌ Should fail but passes (**❌ FAILED**) |
| **3.4: Whitespace-only first name** | `" "` | ❌ Should fail but passes (**❌ FAILED**) |
| **3.5: Whitespace-only last name** | `" "` | ❌ Should fail but passes (**❌ FAILED**) |
| **3.6: First name exceeds character limit** | `100+ characters` | ❌ Should fail but passes (**❌ FAILED**) |
| **3.7: Last name exceeds character limit** | `100+ characters` | ❌ Should fail but passes (**❌ FAILED**) |

---

## Test Case 4: Password Validation Failures

### Objective
Ensure registration fails with insecure or invalid passwords.

### Preconditions
- User is on the registration page.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **4.1: Empty password** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **4.2: Short password** | `"123"` | ❌ Should fail but passes (**❌ FAILED**) |
| **4.3: Long password** | `>30 characters` | ❌ Should fail but passes (**❌ FAILED**) |
| **4.4: Whitespace-only password** | `" "` | ❌ Should fail but passes (**❌ FAILED**) |
| **4.5: Password with only numbers** | `"12345678"` | ❌ Should fail but passes (**❌ FAILED**) |
| **4.6: Password with only letters** | `"abcdefgh"` | ❌ Should fail but passes (**❌ FAILED**) |
| **4.7: Password with only special characters** | `"!@#$%^&"` | ❌ Should fail but passes (**❌ FAILED**) |

---

## Test Case 5: Form Submission with Missing Fields

### Objective
Ensure the form cannot be submitted when all required fields are empty.

### Preconditions
- User is on the registration page.

### Test Steps
1. Leave all fields blank.  
2. Click the **"Register"** button.  

### Expected Result
✅ Registration is **blocked**, and errors are shown for all required fields (**✅ PASS**).