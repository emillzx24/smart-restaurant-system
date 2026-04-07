# Smart Restaurant System

## Overview
The Smart Restaurant System is a web-based application designed to improve the restaurant ordering process. It allows customers to place orders digitally while letting staff view and manage those orders in real time.

## Features
- Customer places orders through the user interface
- Orders are stored in a SQLite database
- Staff can view and manage incoming orders
- Modular structure using services and pages
- Basic testing for main functionality

## Technologies Used
- Python
- Streamlit
- SQLite
- GitHub

## Project Structure
- app.py  
- pages/
   - pages/customer.py
   - pages/staff.py
- components/  
- services/
   - services/__init__.py
   - services/database_service.py
- database/
   - database/schema.sql
   - database/seed.sql
- models/  

## Setup
1. Install dependencies:
   pip install streamlit

2. Create the database:
   sqlite3 database/restaurant.db < database/schema.sql

3. Load seed data:
   sqlite3 database/restaurant.db < database/seed.sql

4. Run the application:
   streamlit run app.py

## Database Notes
The main database files for this phase are:
- database/schema.sql
- database/seed.sql

See database/teammate-guide.md for more details.

## Testing
Test cases are included to validate core capability such as:
- Order creation
- Database interactions
- Staff order viewing

See TEST_CASES.md for more details.

## Notes
This project represents Phase I of the capstone and focuses on the main workflow:
customer places an order, order is stored in the database , and staff can view and manage the order.

## Team
- Stephanie Dunlap
- Geraldine Osawemen
- Andrei Fajutagana
- Emilio Laboy