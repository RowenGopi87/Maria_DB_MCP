#!/usr/bin/env python3
"""
Test script to verify MariaDB connection and MCP server functionality
"""

import asyncio
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

async def test_mariadb_connection():
    """Test direct MariaDB connection"""
    try:
        print(f"Testing connection to MariaDB at {DB_USER}@{DB_HOST}:{DB_PORT}")
        
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT VERSION()")
            version = await cursor.fetchone()
            print(f"✅ Connected successfully!")
            print(f"   MariaDB Version: {version[0]}")
            
            await cursor.execute("SHOW DATABASES")
            databases = await cursor.fetchall()
            print(f"   Available databases: {', '.join([db[0] for db in databases])}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("MariaDB MCP Server - Connection Test")
    print("=" * 40)
    
    success = asyncio.run(test_mariadb_connection())
    
    if success:
        print("\n🎉 Database connection test passed!")
        print("You can now start the MCP server with: start_mcp_server.bat")
    else:
        print("\n❌ Database connection test failed!")
        print("Please check your MariaDB server and configuration.")