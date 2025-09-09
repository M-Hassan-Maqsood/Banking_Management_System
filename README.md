# Banking_Management_System
## Project Overview
Build a Bank Management System with banks, branches, accounts, and users.

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
* Set up relationships with proper related_name
* Run migrations

### Admin Setup
* Register all models in admin
* Add list_display, list_filter, search_fields for each model
* Create sample data via admin

### ORM Practice
* Use Django shell to practice:
  * Create
    ```bash
    user1 = User.objects.create_user(username="ali", password="1234", phone="03001234567", date_of_birth="1995-05-10")
    bank1 = Bank.objects.create(name="Meezan Bank", swift_code="MEZNPKKA", is_islamic=True, established_date="1997-01-01")
    branch1 = BankBranch.objects.create(bank=bank1, name="Main Branch", branch_code="MB001", address="Karachi")
    account1 = BankAccount.objects.create(user=user1, bank_branch=branch1, account_number="1234567890", account_type="savings", balance=5000)
    ```  
  * filter
    ```bash
     User.objects.get(username="ali")
    ```
  * get
    ```bash
    BankAccount.objects.filter(balance__gt=1000)
    ```
  * values operations
    ```bash
    User.objects.values("username", "phone")
    ```
  * Queries with relationships using select_related
    ```bash
    accounts = BankAccount.objects.select_related("bank_branch__bank")
    ```
  * Annotate banks with account counts
    ```bash
    banks = Bank.objects.annotate(account_count=Count("branches__accounts"))
    ```
  * Filter Islamic banks with active accounts
    ```bash
    islamic_banks = Bank.objects.filter(is_islamic=True, branches__accounts__is_active=True).distinct()
    ```
