# MariaDB User Management System

A complete user management system demonstrating MariaDB MCP Server integration with stored procedures.

## 🏗️ Architecture

- **MariaDB Database**: Two tables with foreign key relationship
- **Stored Procedures**: Two procedures, one calling the other
- **MCP Server**: Dual protocol (SSE for Cursor + REST API for Web UI)
- **Web UI**: Simple HTML/JavaScript frontend

## 📋 Components

### Database Schema
```sql
-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Balances table
CREATE TABLE balances (
    balance_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    balance DECIMAL(10,2) DEFAULT 0.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

### Stored Procedures
1. **CreateUser**: Creates user, returns user_id
2. **UpdateBalance**: Calls CreateUser, then manages balance

### Files
- `mcp_server.py` - MCP server with REST API
- `index.html` - Web UI
- `web_server.py` - Simple HTTP server
- `test_stored_procedures.py` - Test script
- `start_system.bat` - Easy startup

## 🚀 Quick Start

### Option 1: Easy Startup
```bash
# Double-click this file:
start_system.bat
```

### Option 2: Manual Startup
```bash
# Terminal 1: Start MCP Server
python mcp_server.py

# Terminal 2: Start Web UI
python web_server.py
```

## 🔧 Testing

### Test Stored Procedures
```bash
python test_stored_procedures.py
```

### Test via Web UI
1. Open http://localhost:8080
2. Enter username, password, balance
3. Click "Create User & Set Balance"
4. Use test buttons to verify connection

### Test MCP Integration with Cursor
Add to your `mcp.json`:
```json
{
  "mcpServers": {
    "MariaDB_Server": {
      "url": "http://localhost:9001/sse",
      "type": "sse"
    }
  }
}
```

## 📊 API Endpoints

### MCP Tools (for Cursor)
- `list_databases`
- `list_tables` 
- `get_table_schema`
- `execute_sql`
- `create_database`
- `get_server_info`

### REST API (for Web UI)
- `POST /api/tools/execute_sql` - Execute SQL queries
- `GET /health` - Health check

## 🎯 Example Usage

### Create User via Stored Procedure
```sql
CALL UpdateBalance('john_doe', 'password123', 100.50);
```

### Query Users and Balances
```sql
SELECT u.username, COALESCE(b.balance, 0.00) as balance 
FROM users u 
LEFT JOIN balances b ON u.user_id = b.user_id;
```

## 🛠️ Requirements

- Python 3.7+
- MariaDB Server
- Required packages: `fastmcp`, `aiomysql`, `python-dotenv`, `pydantic`

## 📝 Configuration

Edit `.env` file:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=

MCP_HOST=localhost
MCP_PORT=9001
```

## 🎉 Success Indicators

- ✅ MCP Server running on port 9001
- ✅ Web UI accessible on port 8080
- ✅ Database connection established
- ✅ Stored procedures working
- ✅ User creation and balance management functional
- ✅ Both SSE (Cursor) and REST (Web) protocols working