# Smart Electronics Laboratory Equipment Management System (SELEMS)

## 📌 Project Overview
The **Smart Electronics Laboratory Equipment Management System (SELEMS)** is a relational database-driven web application engineered to streamline the tracking, organization, and auditing of hardware assets within an electronics laboratory. Built using **Python, Flask, SQLite, SQLAlchemy, and Bootstrap 5**, SELEMS bridges the gap between backend data integrity and a clean, minimalist user interface tailored for academic presentation.

---

## 🛠️ Technology Stack
* **Backend:** Python, Flask framework
* **Database & ORM:** SQLite, Flask-SQLAlchemy (ORM)
* **Frontend:** HTML5, Bootstrap 5, Custom CSS
* **Architecture:** Model-View-Controller (MVC) pattern with relational foreign-key constraints

---

## 🗄️ Database Schema & Architecture
The database is structured around normalized relational entities to eliminate data redundancy and ensure data integrity:
1. **User Table:** Manages system operators and administrative roles.
2. **Category Table:** Groups equipment into logical classifications (e.g., *Measuring Instruments, Power Supplies, Microcontrollers*).
3. **Equipment Table:** Stores specific asset details including total quantity, available stock, physical location, and operational condition. Linked to the Category table via a foreign key (`category_id`).

---

## ✨ Core Features
* **Full CRUD Operations:** 
  * **Create:** Add new laboratory equipment with specific categories, quantities, and bench locations.
  * **Read:** View all inventory items in a responsive, styled tabular dashboard.
  * **Update:** Modify existing asset parameters dynamically through pre-populated edit forms.
  * **Delete:** Safely remove decommissioned or outdated records from the database.
* **Case-Insensitive Search Filtering:** Instantly query and filter equipment records by name using optimized backend filters (`ilike`).
* **Relational Integrity:** Foreign key enforcement ensuring records cannot orphan category dependencies.
* **Modern Minimalist UI:** Custom slate-gray aesthetics, soft container borders, and clean typography designed for optimal academic review.

---

## 📂 Project Directory Structure
```text
SELEMS/
│
├── instance/
│   └── selems.db         # SQLite database file
├── templates/
│   ├── index.html        # Styled landing page dashboard
│   ├── equipment.html    # Inventory data table & search interface
│   ├── add_equipment.html  # Form to add new assets
│   └── edit_equipment.html # Form to modify existing records
│
├── app.py                # Core Flask application, routes, and ORM models
├── seed.py               # Database initialization & sample data script
└── README.md             # Project documentation"# selems" 
