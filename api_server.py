#!/usr/bin/env python3
"""
Simple REST API server for the Web UI
Separate from the MCP server to avoid conflicts
"""

import asyncio
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiomysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "9002"))

# Create FastAPI app
app = FastAPI(title="MariaDB User Management API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    username: str
    password: str
    balance: float = 0.0

class SQLRequest(BaseModel):
    query: str
    database_name: str = "user_management"

# Database connection
async def get_db_connection():
    """Get database connection"""
    return await aiomysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db="user_management"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            result = await cursor.fetchone()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/api/create-user")
async def create_user(request: UserRequest):
    """Create user and set balance using stored procedures"""
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            # Call UpdateBalance stored procedure (which calls CreateUser)
            await cursor.callproc('UpdateBalance', (request.username, request.password, request.balance))
            
        conn.close()
        return {
            "success": True,
            "message": f"User '{request.username}' created/updated with balance ${request.balance:.2f}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute-sql") 
async def execute_sql(request: SQLRequest):
    """Execute SQL query"""
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute(request.query)
            
            if request.query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = await cursor.fetchall()
                conn.close()
                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows)
                }
            else:
                affected_rows = cursor.rowcount
                conn.close()
                return {
                    "success": True,
                    "affected_rows": affected_rows
                }
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users")
async def get_all_users():
    """Get all users with their balances"""
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cursor:
            await cursor.execute("""
                SELECT u.user_id, u.username, COALESCE(b.balance, 0.00) as balance, u.created_at
                FROM users u 
                LEFT JOIN balances b ON u.user_id = b.user_id
                ORDER BY u.user_id
            """)
            columns = [desc[0] for desc in cursor.description]
            rows = await cursor.fetchall()
            
        conn.close()
        
        users = []
        for row in rows:
            user_dict = dict(zip(columns, row))
            users.append(user_dict)
            
        return {"success": True, "users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting User Management API Server on {API_HOST}:{API_PORT}")
    print(f"📖 API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"🔍 Health Check: http://{API_HOST}:{API_PORT}/health")
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)