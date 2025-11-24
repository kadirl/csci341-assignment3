# PostgreSQL Setup Guide for macOS

## Quick Start

PostgreSQL 16 is already installed and running on your system! Here's how to use it:

### 1. Add PostgreSQL to Your PATH (Permanent)

Add this line to your `~/.zshrc` file to make PostgreSQL commands available:

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. Verify PostgreSQL is Running

```bash
brew services list | grep postgresql
```

You should see `postgresql@16` with status `started`.

### 3. Test Connection

```bash
psql -d postgres -c "SELECT version();"
```

### 4. Database is Already Created

The `caregivers_db` database has been created. You can verify:

```bash
psql -d caregivers_db -c "\dt"
```

### 5. Run the Python Script

```bash
cd backend
pip install -r requirements.txt
python database_operations.py
```

## Default User

On macOS with Homebrew PostgreSQL, the default user is your macOS username (`macbookair`), not `postgres`. The Python script has been updated to automatically use your username.

## Common Commands

### Start/Stop PostgreSQL
```bash
brew services start postgresql@16
brew services stop postgresql@16
brew services restart postgresql@16
```

### Connect to Database
```bash
psql -d caregivers_db
```

### List All Databases
```bash
psql -d postgres -c "\l"
```

### Export Database (for submission)
```bash
pg_dump caregivers_db > caregivers_db.sql
```

## Troubleshooting

If you get connection errors:
1. Make sure PostgreSQL is running: `brew services list | grep postgresql`
2. Check if the service is started (should show `started` status)
3. If not, restart: `brew services restart postgresql@16`

If you get "command not found" for `psql`:
- Make sure you've added PostgreSQL to your PATH (step 1 above)
- Or use the full path: `/opt/homebrew/opt/postgresql@16/bin/psql`

