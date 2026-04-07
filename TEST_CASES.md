# Smart Restaurant System - Test Cases

## Test Scope
For testing, I focused primarily on the database/service layer since that's where most of the functionality is implemented in the project. The tests are based on the file:
services/database_service.py

## Test Cases

1. Verified that the database initializes correctly and creates the SQLite database.
2. Checked that menu categories are returned properly.
3. Confirmed that menu items can be filtered by category.
4. Tested that QR lookup returns the correct restaurant table.
5. Verified that creating an order calculates the correct total price.
6. Tested that special instructions are saved when creating an order.
7. Confirmed that an order cannot be created with an empty item list.
8. Checked that invalid payment statuses are rejected.
9. Verified that inactive tables cannot be used to create orders.
10. Tested updating an order to "completed" and confirmed the timestamp is set.
11. Tested updating an order to "cancelled" and confirmed the timestamp is set.
12. Verified that updating payment status correctly marks the order as paid.
13. Confirmed that orders can be filtered by status.
14. Checked that order details include all related line items.

## Testing Method
I used Python's built-in unittest framework to create and run the tests. I chose this because it's simple and doesn't require installing any extra libraries. The final test run completed successfully with 22 tests run, 0 failures, and 0 errors.

## How to Run Tests
Run the following command in the project folder:

python -m unittest test_database_service.py test_staff_page.py -v
