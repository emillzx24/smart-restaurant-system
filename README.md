# Smart Restaurant System

## Overview

The Smart Restaurant System is a web-based application designed to improve the restaurant ordering process for small restaurants. It allows customers to place orders digitally while allowing staff to view, manage, and update those orders in real time.

The goal of the project is to replace a manual ordering workflow with a simple digital system that improves efficiency, organization, and customer experience.

This project represents the Phase II version of the capstone project and includes finalized core functionality, testing, and documentation.

## Features

- Customers can place orders through the user interface
- Orders are stored in a SQLite database
- Staff can view and manage incoming orders
- Order workflow is supported through the staff interface
- Modular structure using pages, services, and database layers
- Unit and manual testing for core functionality

## Technologies Used

- Python
- Streamlit
- SQLite
- GitHub

## Project Structure

- app.py
- components/
- database/
- models/
- pages/
- services/
- TEST_CASES.md
- test_database_service.py
- test_staff_page.py

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

The main database files for this project are:

- database/schema.sql
- database/seed.sql

See database/teammate-guide.md for more details.

## Testing

Testing is included to validate core functionality such as:

- Order creation
- Database interactions
- Staff order viewing
- Staff workflow behavior

The project includes test files for service and staff page functionality. See TEST_CASES.md for more details.

## Notes

This project represents the Phase II capstone submission. It focuses on the digital restaurant workflow, including customer ordering, database storage, and staff-side order management.

The system is designed to be modular, maintainable, and easy to improve in future phases or extensions.

## Team

- Stephanie Dunlap
- Geraldine Osawemen
- Andrei Fajutagana
- Emilio Laboy