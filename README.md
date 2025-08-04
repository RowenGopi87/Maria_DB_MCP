# MariaDB MCP Server

A comprehensive MariaDB Model Context Protocol (MCP) server implementation with web UI for user management.

## 🚀 Features

- **MCP Server Integration**: Full integration with Cursor AI via Server-Sent Events (SSE)
- **Web UI**: Simple browser-based interface for user management
- **Stored Procedures**: Database operations via MariaDB stored procedures
- **REST API**: RESTful endpoints for web UI interactions
- **Multi-Database Support**: Manage multiple databases through a single server
- **Auto-Start System**: One-click startup via batch file

## 📋 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Cursor AI     │────│   MCP Server     │────│     MariaDB         │
│   (Port N/A)    │    │   (Port 9001)    │    │   (Port 3306)       │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                          │
┌─────────────────┐    ┌──────────────────┐              │
│   Web UI        │────│   API Server     │──────────────┘
│   (Port 8080)   │    │   (Port 9002)    │
└─────────────────┘    └──────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.11+ 
- MariaDB Server (11.8+)
- Git

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RowenGopi87/Maria_DB_MCP.git
   cd Maria_DB_MCP
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MariaDB:**
   - Install MariaDB via winget (Windows) or your package manager
   - Start MariaDB service
   - Run the database setup:
   ```bash
   mysql -u root -h 127.0.0.1 --skip-ssl < create_procedures.sql
   ```

4. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Update database connection settings if needed

## ⚡ Usage

### Easy Start (Recommended)
Double-click or run:
```bash
start_system.bat
```

This automatically starts:
- **MCP Server** (Port 9001) - For Cursor AI
- **API Server** (Port 9002) - For Web UI  
- **Web UI** (Port 8080) - Browser interface

### Manual Start
```bash
# Terminal 1: MCP Server
python mcp_server.py

# Terminal 2: API Server  
python api_server.py

# Terminal 3: Web UI
python web_server.py
```

### Cursor AI Integration

Add to your Cursor `mcp.json` configuration:
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

## 🔧 Configuration

### Environment Variables (.env)
```bash
# MariaDB Connection
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=

# MCP Server
MCP_HOST=localhost
MCP_PORT=9001

# API Server  
API_HOST=localhost
API_PORT=9002
```

## 📊 Database Schema

### Tables
- **users**: User credentials and metadata
  - `user_id` (AUTO_INCREMENT, Primary Key)
  - `username` (UNIQUE)
  - `password`
  - `created_at`

- **balances**: User financial data
  - `balance_id` (AUTO_INCREMENT, Primary Key)  
  - `user_id` (Foreign Key → users.user_id)
  - `balance` (DECIMAL)
  - `updated_at`

### Stored Procedures
- **CreateUser**: Creates new user, returns user_id
- **UpdateBalance**: Creates/updates user balance (calls CreateUser)

## 🔍 Available MCP Tools

- `list_databases()` - Show all databases
- `list_tables()` - List tables in database
- `execute_sql()` - Run SQL queries
- `call_stored_procedure()` - Execute stored procedures
- `get_server_info()` - MariaDB server information

## 🌐 API Endpoints

### Health Check
- `GET /health` - Server status

### User Management  
- `POST /api/create-user` - Create user with balance
- `GET /api/users` - List all users with balances
- `POST /api/execute-sql` - Execute SQL query

## 🧪 Testing

### Connection Test
```bash
python test_connection.py
```

### Stored Procedures Test
```bash
python test_stored_procedures.py
```

### Web UI Testing
1. Open http://localhost:8080
2. Use "Test Connection" and "Test Stored Procedures" buttons

## 📁 File Structure

```
MariaDB-MCP/
├── mcp_server.py          # Main MCP server (SSE)
├── api_server.py          # REST API server for web UI
├── web_server.py          # Static file server for HTML
├── index.html             # Web UI interface
├── create_procedures.sql  # Database schema & procedures
├── start_system.bat       # Auto-start script
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── test_connection.py     # Database connectivity test
├── test_stored_procedures.py # Procedures functionality test
└── README.md             # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**: Check if ports 9001, 9002, 8080 are available
2. **MariaDB connection**: Ensure MariaDB service is running
3. **SSL errors**: Use `--skip-ssl` flag with mysql client
4. **Empty password**: Ensure `.env` allows empty DB_PASSWORD

### Debug Commands
```bash
# Check running processes
netstat -an | findstr ":9001\|:9002\|:8080"

# Test MariaDB connection
mysql -u root -h 127.0.0.1 --skip-ssl

# Check Python dependencies
pip list | findstr "fastmcp\|aiomysql\|fastapi"
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MariaDB Foundation](https://mariadb.org/) for the excellent database system
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [Cursor AI](https://cursor.sh/) for MCP protocol support

---

**Built with ❤️ for seamless AI-database integration**