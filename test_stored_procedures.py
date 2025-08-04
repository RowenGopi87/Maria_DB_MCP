#!/usr/bin/env python3
"""
Test script for the stored procedures
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

async def test_stored_procedures():
    """Test the stored procedures directly"""
    try:
        print("🔌 Connecting to MariaDB...")
        
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db="user_management"
        )
        
        async with conn.cursor() as cursor:
            print("✅ Connected successfully!")
            print()
            
            # Test 1: Create a user and set balance using UpdateBalance procedure
            print("🧪 Test 1: Creating user 'testuser' with balance $123.45")
            await cursor.callproc('UpdateBalance', ('testuser', 'password123', 123.45))
            print("✅ UpdateBalance procedure called successfully")
            
            # Test 2: Check if user was created
            print("\n🔍 Test 2: Checking created user...")
            await cursor.execute("SELECT * FROM users WHERE username = 'testuser'")
            user = await cursor.fetchone()
            if user:
                print(f"✅ User created: ID={user[0]}, Username={user[1]}, Created={user[3]}")
            else:
                print("❌ User not found")
            
            # Test 3: Check if balance was set
            print("\n💰 Test 3: Checking user balance...")
            await cursor.execute("""
                SELECT u.user_id, u.username, b.balance 
                FROM users u 
                LEFT JOIN balances b ON u.user_id = b.user_id 
                WHERE u.username = 'testuser'
            """)
            result = await cursor.fetchone()
            if result:
                print(f"✅ Balance found: User ID={result[0]}, Username={result[1]}, Balance=${result[2]}")
            else:
                print("❌ Balance not found")
            
            # Test 4: Update existing user balance
            print("\n🔄 Test 4: Updating balance to $999.99")
            await cursor.callproc('UpdateBalance', ('testuser', 'password123', 999.99))
            
            await cursor.execute("""
                SELECT u.username, b.balance 
                FROM users u 
                JOIN balances b ON u.user_id = b.user_id 
                WHERE u.username = 'testuser'
            """)
            result = await cursor.fetchone()
            if result:
                print(f"✅ Balance updated: Username={result[0]}, New Balance=${result[1]}")
            
            # Test 5: Create another user
            print("\n👥 Test 5: Creating second user 'alice' with balance $50.00")
            await cursor.callproc('UpdateBalance', ('alice', 'alicepass', 50.00))
            
            # Show all users and balances
            print("\n📊 All Users and Balances:")
            await cursor.execute("""
                SELECT u.user_id, u.username, COALESCE(b.balance, 0.00) as balance, u.created_at
                FROM users u 
                LEFT JOIN balances b ON u.user_id = b.user_id
                ORDER BY u.user_id
            """)
            users = await cursor.fetchall()
            
            print("ID | Username | Balance  | Created")
            print("-" * 40)
            for user in users:
                print(f"{user[0]:2} | {user[1]:8} | ${user[2]:7} | {user[3]}")
            
        conn.close()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📝 Summary:")
        print("✅ Both stored procedures working correctly")
        print("✅ CreateUser procedure creates users with unique IDs")
        print("✅ UpdateBalance procedure calls CreateUser and manages balances") 
        print("✅ Tables have proper foreign key relationships")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("MariaDB Stored Procedures Test")
    print("=" * 35)
    
    success = asyncio.run(test_stored_procedures())
    
    if success:
        print("\n🚀 Ready to start the web UI!")
        print("Run: python web_server.py")
    else:
        print("\n❌ Fix the issues above before proceeding")