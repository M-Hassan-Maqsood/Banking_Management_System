# Banking_Management_System
## Project Overview
A Banking Management System that manages banks, branches, customer accounts, and users.

---

## Phase 1: Django Foundation
**Core Models & Admin**

### Setup & Models
* Create Django project with apps: banks, accounts, users
* Models to create:
  * User (extend AbstractUser with phone, date_of_birth)
  * Bank (name, swift_code, is_islamic, established_date)
  * BankBranch (bank FK, name, branch_code, address)
  * BankAccount (user FK, bank_branch FK, account_number, account_type choices, balance, is_active)

### Admin Setup
* All models were registered in the Django admin.
* list_display, list_filter and search_fields were added for each model to improve data management.
* Sample data was created via the admin panel for testing.

### ORM Practice
* Django shell was used to practice and verify ORM operations:
  * **Create**
    ```bash
    user1 = User.objects.create_user(username="ali", password="1234", phone="03001234567", date_of_birth="1995-05-10")
    bank1 = Bank.objects.create(name="Meezan Bank", swift_code="MEZNPKKA", is_islamic=True, established_date="1997-01-01")
    branch1 = BankBranch.objects.create(bank=bank1, name="Main Branch", branch_code="MB001", address="Karachi")
    account1 = BankAccount.objects.create(user=user1, bank_branch=branch1, account_number="1234567890", account_type="savings", balance=5000)
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
