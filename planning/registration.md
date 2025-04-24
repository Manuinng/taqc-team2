# Registration Test Planning

## Table of Contents

- [Test Case 1: Validate successful registration with valid data](#test-case-1-validate-successful-registration-with-valid-data)
- [Test Case 2: Validate required fields](#test-case-2-validate-required-fields)
- [Test Case 3: Validate invalid emails are not accepted](#test-case-3-validate-invalid-emails-are-not-accepted)
- [Test Case 4: Validate invalid names are not accepted](#test-case-4-validate-invalid-names-are-not-accepted)
- [Test Case 5: Validate invalid passwords are not accepted](#test-case-5-validate-invalid-passwords-are-not-accepted)
- [Test Case 6: Validate registration fails with all fields missing](#test-case-6-validate-registration-fails-with-all-fields-missing)

---

## Test Case 1: Validate successful registration with valid data

### Objective
Verify the registration form submits successfully when all required fields are filled with valid data.

### Preconditions
- User is on the registration page.

### Test Steps
1. Fill first name field with **"Juan"**  
2. Fill last name field with **"Pérez"**  
3. Fill email field with **"juan.perez@example.com"**  
4. Fill password field with **"ValidP@ssw0rd"**  
5. Click the **"Register"** button  

### Expected Result
✅ Registration completes successfully, and the user is redirected to the **welcome/dashboard page**.

---

## Test Case 2: Validate required fields

### Objective
Ensure registration fails when required fields are missing.

### Preconditions
- User is on the registration page.

### Test Steps
1. Leave the required field empty.
2. Fill in all other fields with valid data.
3. Attempt to submit the form.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **2.1: Empty first name** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **2.2: Empty last name** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **2.3: Empty email** | `""` | ❌ Registration should fail (**✅ PASS**) |
| **2.4: Empty password** | `""` | ❌ Registration should fail (**✅ PASS**) |

---

## Test Case 3: Validate invalid emails are not accepted

### Objective
Ensure registration fails with malformed or invalid email formats.

### Preconditions
- User is on the registration page.

### Test Steps
1. Fill the email field with an invalid format.
2. Fill in all other fields with valid data.
3. Attempt to submit the form.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **3.1: Invalid email format** | `"invalidemail"` | ❌ Registration should fail (**✅ PASS**) |
| **3.2: Email with spaces** | `"juan perez@example.com"` | ❌ Registration should fail (**✅ PASS**) |
| **3.3: Invalid domain** | `"juan@"` | ❌ Registration should fail (**✅ PASS**) |
| **3.4: Email with special characters** | `"juan@pérez!.com"` | ❌ Registration should fail (**✅ PASS**) |
| **3.5: Very long email (>256 chars)** | `"test" + "a" * 250 + "@example.com"` | ❌ Registration should fail (**✅ PASS**) |

---

## Test Case 4: Validate invalid names are not accepted

### Objective
Ensure registration fails when name fields contain invalid characters or exceed limits.

### Preconditions
- User is on the registration page.

### Test Steps
1. Fill the name field with an invalid value.
2. Fill in all other fields with valid data.
3. Attempt to submit the form.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **4.1: Special characters in name** | `"@na#"` | ❌ Registration should fail (**✅ PASS**) |
| **4.2: Whitespace-only first name** | `" "` | ❌ Registration should fail (**✅ PASS**) |
| **4.3: Whitespace-only last name** | `" "` | ❌ Registration should fail (**✅ PASS**) |
| **4.4: First name exceeds character limit** | `100+ characters` | ❌ Registration should fail (**✅ PASS**) |
| **4.5: Last name exceeds character limit** | `100+ characters` | ❌ Registration should fail (**✅ PASS**) |

---

## Test Case 5: Validate invalid passwords are not accepted

### Objective
Ensure registration fails with insecure or incorrectly formatted passwords.

### Preconditions
- User is on the registration page.

### Test Steps
1. Fill the password field with an invalid value.
2. Fill in all other fields with valid data.
3. Attempt to submit the form.

### Sub-Cases
| **Scenario** | **Input** | **Expected Outcome** |
|-------------|----------|----------------------|
| **5.1: Short password** | `"12345"` | ❌ Registration should fail (**✅ PASS**) |
| **5.2: Long password (>128 chars)** | `"A" * 130` | ❌ Registration should fail (**✅ PASS**) |
| **5.3: Whitespace-only password** | `" "` | ❌ Registration should fail (**✅ PASS**) |
| **5.4: Password with only numbers** | `"12345678"` | ❌ Registration should fail (**✅ PASS**) |
| **5.5: Password with only letters** | `"abcdefgh"` | ❌ Registration should fail (**✅ PASS**) |
| **5.6: Password with only special characters** | `"!@#$%^&"` | ❌ Registration should fail (**✅ PASS**) |

---

## Test Case 6: Validate registration fails with all fields missing

### Objective
Ensure the form cannot be submitted when all required fields are left blank.

### Preconditions
- User is on the registration page.

### Test Steps
1. Leave all fields blank.
2. Click the **"Register"** button.

### Expected Result
✅ Registration is **blocked**, and errors are displayed for all required fields (**✅ PASS**).