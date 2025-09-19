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
