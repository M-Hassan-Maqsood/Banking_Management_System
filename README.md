# Banking_Management_System
## Project Overview
A Banking Management System that manages banks, branches, customer accounts, and users.

---

## Phase 1: Django Foundation
**Core Models & Admin**

### Setup & Models
* Django project created with apps: `banks`, `accounts`, `users`
* Models implemented:
  * User (extend AbstractUser with phone, date_of_birth)
  * Bank (name, swift_code, is_islamic, established_date)
  * BankBranch (bank FK, name, branch_code, address)
  * BankAccount (user FK, bank_branch FK, account_number, account_type choices, balance, is_active)

### Admin Setup
* All models were registered in the Django admin.
* `list_display`, `list_filter` and `search_fields` were added for each model to improve data management.

### ORM Practice
* Django shell was used to practice and verify ORM operations:
  * **Create**
    ```bash
    user_1 = User.objects.create_user(username="ali", password="1234", phone="03001234567", date_of_birth="1995-05-10")
    bank_1 = Bank.objects.create(name="Meezan Bank", swift_code="MEZNPKKA", is_islamic=True, established_date="1997-01-01")
    branch_1 = BankBranch.objects.create(bank=bank_1, name="Main Branch", branch_code="MB001", address="Karachi")
    account_1 = BankAccount.objects.create(user=user_1, bank_branch=branch_1, account_number="1234567890", account_type="savings", balance=5000)
    ```  
  * **Filter**
    ```bash
     User.objects.get(username="ali")
    ```
  * **Get**
    ```bash
    BankAccount.objects.filter(balance__gt=1000)
    ```
  * **Values**
    ```bash
    User.objects.values("username", "phone")
    ```
  * **Queries with relationships using select_related**
    ```bash
    accounts = BankAccount.objects.select_related("bank_branch__bank")
    ```
  * **Banks were annotated with account counts**
    ```bash
    banks = Bank.objects.annotate(account_count=Count("branches__accounts"))
    ```
  * **Islamic banks with active accounts were filtered**
    ```bash
    islamic_banks = Bank.objects.filter(is_islamic=True, branches__accounts__is_active=True).distinct()
    ```
  ---

## Phase 2: Basic Django Views  
**Authentication & Simple Views**

### Authentication
* Implemented **custom login and logout views** using Django’s authentication system.  
* Added **`@login_required` decorators for views**  
* Configured `LOGIN_URL` so unauthenticated users are always redirected to the login page.  

### Views
* **/banks/** – Class-based view to list all banks, having the following information:  
  - Bank name  
  - Whether the bank is *Islamic* (`is_islamic`)  
  - Number of branches  

* **/accounts/** – Class-based view to list the **logged-in user accounts**, showing:  
  - Bank name  
  - Account number  
  - Balance  

---
## Phase 3: DRF API Foundation
**Transform to REST APIs**

### Django REST Framework Setup
* Installed Django REST Framework (DRF) and added to settings
* Created serializers for Bank and Account models
* Added nested field: `bank_name` inside `AccountSerializer`

### Banks API - Learn Multiple Approaches
Implemented the same endpoints using 3 different approaches (separate branch for each):
* **APIView**
- BankListAPIView
- AccountListAPIView
- Manually handled request/response

* **Generic View** (ListAPIView)
- BankListGenericView
- AccountListGenericView

* **ViewSet** (ReadOnlyModelViewSet)
- BankViewSet
- AccountViewSet
---

# Phase 4: DRF API Deep Dive 

## Final API Implementation (Production-Ready Views)  
Replaced all the existing code in `apis/urls.py` with the following Generic views:
- **Banks** `ListCreateAPIView` (`GET/POST /api/banks/`)  
- **Bank Detail** `RetrieveUpdateDestroyAPIView` (`GET/PATCH/DELETE /api/banks/{id}/`)  
- **Accounts** `ListCreateAPIView` (`GET/POST /api/accounts/`)  
- **Account Detail** `RetrieveUpdateDestroyAPIView` (`GET/PATCH/DELETE /api/accounts/{id}/`)  

---

## Required APIs  

### Banks  
- `GET /api/banks/` → List all banks  
- `POST /api/banks/` → Create new bank  
- `GET /api/banks/{id}/` → Retrieve bank detail  
- `PATCH /api/banks/{id}/` → Update bank  
- `DELETE /api/banks/{id}/` → Delete bank  

### Accounts  
- `GET /api/accounts/`  List user’s accounts (with `bank_name`)  
- `POST /api/accounts/`  Create account (via username + branch name)  
- `GET /api/accounts/{id}/`  Retrieve account detail  
- `PATCH /api/accounts/{id}/`  Update account  
- `DELETE /api/accounts/{id}/`  Delete account  

---

## Postman Testing  
- A **[Postman collection](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262)** was created including all above endpoints.  
- APIs tested successfully with `GET`, `POST`, `PATCH`, and `DELETE` requests.  

---
## Phase 5: Authentication & Permissions
**Secure API Access**

### Token Authentication
* Configured **Token Authentication** in settings
* Configured `rest_framework.authtoken` and ran migrations
* Added Login API to return token
* Added endpoint:  
  * `POST /api/auth/login/` - accepts username/password, returns token

### Protected APIs
* Added APIs accessible only to authenticated users:
  * `GET /api/accounts/` - lists **only the requesting user's accounts**
  * `PATCH /api/accounts/{id}/balance/` - update **account balance (owner only)**

### Staff-only APIs
* Added staff-level access with custom permissions:
  * `GET /api/accounts/{id}/` - retrieve **any account details (staff only)**
  * `DELETE /api/accounts/{id}/` - delete **any account (staff only)**
  * `PATCH /api/accounts/{id}/balance/` - update **any account balance (staff only)**

### Postman
* Created and tested all authentication & permission based APIs in **[Postman](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262)**  
* Verified behavior for both **normal users** and **staff users**

---
## Phase 6: Advanced Features
**Production-ready APIs**

### Filtering & Search
* Installed `django-filter` and integrated with DRF.
* Modified **Account List API** with advanced querying options:
  * **Filter by**:
    * `bank`, `account_type`, `is_islamic`
  * **Search by**:
    * `first_name`, `last_name`, `username` of user
  * **Order by**:
    * `balance`, `created_at`, `username` of user

* **APIs**
* All APIs have been tested and documented in [**Postman**](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262).
* `GET /api/accounts/?account_type=current`
* `GET /api/accounts/?branch__bank__is_islamic=true`
* `GET /api/accounts/?search=waleed54`
* `GET /api/accounts/?ordering=balance`

### Pagination
* Added pagination support to **Account List API**
* Default page size: **10 items**

---
## Phase 7: Configuration & Middleware
**Enterprise Features**

### Constance Setup
* Installed `django-constance` with `MemoryBackend`
* Added configuration variable:  
  * `MAINTENANCE_MODE = False` (default)

### Custom Middleware
* Implemented custom middleware to enforce **maintenance mode**.
* Behavior:
  * If `MAINTENANCE_MODE = True`, all requests return **503 Service Unavailable** with message:  
    `"The system is currently under maintenance. Please try again later."`
  * Staff users can bypass maintenance mode.
  * Normal users and anonymous requests are blocked during maintenance mode.

### Postman
* Verified using **[Postman](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262)** with different tokens:
  * **Superuser and Staff token** - bypasses maintenance mode.
  * **Normal user token** - blocked with 503 response.
  * **No token / Anonymous** - blocked with 503 response.

-----
# Phase 9: Transactions Model & Sample Data

**Extend Domain Models & Seed Data for Analytics**

---

## Setup & Models

- Introduced a new **`Transaction`** model with the following fields:
  - `account` - FK to `accounts.Account` (with `related_name="transactions"`, `on_delete=models.CASCADE`)  
  - `date` - `DateField`  
  - `amount` - `DecimalField(max_digits=12, decimal_places=2)`  
  - `type` - `CharField` with choices:  
    - `("deposit", "Deposit")`  
    - `("withdrawal", "Withdrawal")`  

- Applied migrations to update the schema  
- Registered the `Transaction` model in **Django Admin**

---

## Sample Data Generation

- Installed **`django-extensions`** for `shell_plus`  
- Wrote a script to bulk-generate random but realistic data  

The script performs the following:  

- Create **4 Banks**  
- Create **10 Users**, each linked to **2 Accounts** in different banks  
- Create **30–50 Transactions per Account**, with:  
  - Random dates limited to **2024 & 2025**  
  - Mixed **Deposits** and **Withdrawals**

 The transactions file is placed inside the **`scripts/`** folder for reuse  

---
## Phase 10 : Account Summary Reports (Aggregates & Window Functions)

This phase introduces a financial summary API that leverages advanced Django ORM features such as `aggregates`, `annotations`, and `window functions` to provide analytical insights into account transactions.

Endpoint
GET /api/reports/{account_id}/summary/?year=YYYY&month=MM


* **Query Parameters**
- year (Optional) - Filter transactions by year.
- month (Optional) - Filters transactions within that month.

* **Scenarios**

- Year + Month - Summary for that specific month.
- Year only - Summary for the entire year.

### **Implementation Details**

- **Filtering Transactions**
- Transactions are retrieved for a given account_id.
- Optional filters (year, month) refine the dataset.

- **Aggregations**
- Total Deposits and Withdrawals computed via Case/When + Sum.
- Maximum Transaction Amount determined using Max.

- **Running Balance**
- Calculated using Window() ordered by transaction date and id.
- Ensures cumulative balance is tracked over time.
- From this, the minimum running balance is extracted.

- **Opening Balance**
- Derived from transactions before the reporting period.
- Provides consistency in financial reporting.

### **Postman**

Tested endpoint with different query combinations in [Postman](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262):

- Year only (2024) - returned correct summary for all months of 2023
- Year + Month (2025-07) - restricted transactions to July 2023
---
## Phase 11: Cross-Bank Analytics

This part provides a **Cross-Bank Analytics API** built with Django REST Framework.  
It aggregates transaction data across multiple banks and their branches to deliver financial insights.

---

### **Features**

- **Filter by Year** - Transactions can be filtered using a `year` query parameter.  
- **Bank-level Analytics** - Provides per-bank totals:  
  - Total Deposits  
  - Total Withdrawals  
  - Net Inflow (Deposits - Withdrawals)  
- **Branch-level Analytics** - Provides per-branch breakdowns with the same financial metrics.
- **No Loops or List Comprehensions** - All calculations done at the database level.
- **Test with Postman** - Easily test the API endpoints by importing them into [Postman](https://lively-sunset-851161.postman.co/workspace/Team-Workspace~b615434a-b98d-482a-8dfc-b8a2b4bff805/collection/43201262-d063c160-450e-449f-9c66-3b0407aab5d1?action=share&source=copy-link&creator=43201262)
---

# Phase 12 – Background Tasks

## Introduction
Asynchronous task processing has been integrated into the **Banking Management System (BMS)** using **Celery** with **Redis** as the message broker.  
The purpose of this is to efficiently handle time consuming tasks, such as sending emails, and to automate scheduled jobs, like daily interest calculation, in the background without blocking the main application.

---

## Setup
- **Install Tools**: Celery, Redis, Django-Celery-Beat  
- **Broker & Backend**: Redis running at `127.0.0.1:6380`
- **Settings Update**: Add `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`. 

---

## Features Implemented
### 1. Asynchronous Email Sending
- When a **new account** is create, an **email notification** is sent asynchronously.  
- Emails are logged in the console (Django console email backend).  

### 2. Periodic Daily Interest
- **0.1% interest per day** apply automatically to all savings accounts.  
- Schedule to run daily at **midnight** using **Celery Beat**.  

### 3. Admin Integration
- **Django Admin -> Periodic Tasks** (via `django-celery-beat`).  
- Admin users can create, edit, and manage schedule jobs.

---
# Phase 13: Testing – Quality Assurance

This phase focuses on ensuring the **reliability, accuracy, and security** of the Banking Management System (BMS) API's through **automated testing** and **coverage analysis**.  
Testing validates that the system behaves as expected across user roles, authentication layers, and core business logic.

---

## Testing Framework & Tools

- **Framework**:  Django Test Framework
- **Authentication**:  Token Authentication
- **Coverage Tool**:  `coverage.py`

---

## API Test Cases

### 1. User Access Control
**Goal:** Ensure that a normal user can only view and manage their own accounts.  
- **Expected Result:**
  - `GET /api/accounts/` -> returns only the logged-in user’s accounts.  
  - `403 Forbidden` if accessing another user’s account.

### 2. Staff Access Control
**Goal:** Validate that staff (admin) users can access and manage all accounts.  
- **Expected Result:**
  - `GET /api/accounts/` -> returns all accounts.

### 3. Authentication Requirement
**Goal:** Verify that protected endpoints require authentication.  
- **Expected Result:**
  - Unauthenticated requests → `401 Unauthorized`.  
  - Authenticated requests → `200 OK`.

### 4. Account Balance Update
**Goal:** Confirm that balance updates work correctly.  
- **Expected Result:**
  - Authenticated users can update their own balance.  
  - Staff can update any account’s balance.  
  - Unauthorized updates → `403 Forbidden`.

### 5. Filtering and Search
**Goal:** Validate backend filtering and search logic using `DjangoFilterBackend`.  
- **Expected Result:**
  - Filtering by `account_type`, `branch__bank__name`, or `is_islamic` returns correct results.  
  - Searching by user’s name or username works correctly.  
  - Invalid filters → `400 Bad Request`.

---