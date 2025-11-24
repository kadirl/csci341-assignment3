# CSCI 341 Assignment 3 - Parts 1 & 2

## Setup Instructions

### Prerequisites
- PostgreSQL installed and running
- Python 3.8 or higher
- pip (Python package manager)

### Database Setup

1. **Create PostgreSQL database:**
```bash
createdb caregivers_db
```

Or using psql:
```sql
CREATE DATABASE caregivers_db;
```

2. **Set environment variables (optional, defaults provided):**
```bash
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregivers_db
```

### Python Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the database operations script:**
```bash
python database_operations.py
```

This script will:
- Create all tables (Part 2.1)
- Insert sample data (Part 2.2)
- Execute all update queries (Part 2.3)
- Execute all delete queries (Part 2.4)
- Execute all simple queries (Part 2.5)
- Execute all complex queries (Part 2.6)
- Execute query with derived attribute (Part 2.7)
- Create and query view (Part 2.8)

### Alternative: Using SQL Files Directly

If you prefer to use the SQL files directly:

1. **Create tables:**
```bash
psql -U postgres -d caregivers_db -f schema.sql
```

2. **Insert data:**
```bash
psql -U postgres -d caregivers_db -f insert_data.sql
```

### Export Database

To export the database in .sql format (as required for submission):

```bash
pg_dump -U postgres caregivers_db > caregivers_db.sql
```

## Files

- `schema.sql`: Database schema with table definitions
- `insert_data.sql`: Sample data for all tables (at least 10 instances per table)
- `database_operations.py`: Python script using SQLAlchemy for all Part 2 operations
- `requirements.txt`: Python dependencies

## Notes

- The script uses SQLAlchemy with Textual SQL for maximum flexibility
- All queries are designed to return non-empty results
- The data includes specific entries needed for update/delete queries (e.g., Arman Armanov, Amina Aminova, Kabanbay Batyr street)

