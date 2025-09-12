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
- 