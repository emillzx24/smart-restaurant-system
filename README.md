# Smart Restaurant System

## Overview
Prototype web application that allows customers to place orders digitally and enables staff to manage and track those orders.

This branch currently focuses on the initial database setup for the project.

## Tech Stack
- Python
- Streamlit
- SQLite

## Project Structure
- app.py
- pages/
- components/
- services/
- database/
  - schema.sql
  - seed.sql
- models/

## Setup
1. Install Streamlit:
   `pip install streamlit`
2. Create the local SQLite database from the schema:
   `sqlite3 database/restaurant.db < database/schema.sql`
3. Load demo seed data:
   `sqlite3 database/restaurant.db < database/seed.sql`
4. Run the app:
   `streamlit run app.py`

## Database Notes
- The main database files for this phase are `database/schema.sql` and `database/seed.sql`.
- The generated `database/restaurant.db` file is for local testing and should not be treated as source code.
- The schema includes the core project tables: restaurant tables, menu categories, menu items, orders, and order items.

## Core Functionality
- Customer order input (in progress)
- Staff order management (planned)
- Order storage and status tracking (database setup complete for initial prototype)

## Team
- Stephanie Dunlap  
- Geraldine Osawemen  
- Andrei Fajutagana  
- Emilio Laboy  
