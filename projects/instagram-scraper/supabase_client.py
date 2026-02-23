#!/usr/bin/env python3
"""
Supabase Integration for Instagram Followers Tracker
Manages username status tracking and print validation
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

class SupabaseFollowersDB:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = "instagram_followers"
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Create table if it doesn't exist"""
        try:
            # Try to query; if fails, table doesn't exist
            response = self.supabase.table(self.table_name).select("id").limit(1).execute()
            print(f"✅ Table '{self.table_name}' already exists")
        except Exception as e:
            print(f"⚠️ Table doesn't exist, creating... ({e})")
            self._create_table()
    
    def _create_table(self):
        """Create the instagram_followers table schema"""
        # Note: This is a placeholder. You'll need to create the table manually
        # via Supabase dashboard or use a migration tool.
        # Table schema should be:
        # - id: bigint (primary key)
        # - username: text (unique)
        # - status: text ('esperando' | 'print feito')
        # - file_path: text (nullable)
        # - added_at: timestamp
        # - print_at: timestamp (nullable)
        print("""
        📋 Create this table in Supabase dashboard:
        
        CREATE TABLE instagram_followers (
          id BIGSERIAL PRIMARY KEY,
          username TEXT UNIQUE NOT NULL,
          status TEXT DEFAULT 'esperando' CHECK (status IN ('esperando', 'print feito')),
          file_path TEXT,
          added_at TIMESTAMP DEFAULT NOW(),
          print_at TIMESTAMP,
          created_at TIMESTAMP DEFAULT NOW(),
          updated_at TIMESTAMP DEFAULT NOW()
        );
        
        CREATE INDEX idx_username ON instagram_followers(username);
        CREATE INDEX idx_status ON instagram_followers(status);
        """)
    
    def check_username_exists(self, username: str) -> dict:
        """Check if username exists and return status"""
        try:
            response = self.supabase.table(self.table_name).select("*").eq("username", username).execute()
            if response.data and len(response.data) > 0:
                return {"exists": True, "data": response.data[0]}
            return {"exists": False}
        except Exception as e:
            print(f"❌ Error checking username: {e}")
            return {"exists": False, "error": str(e)}
    
    def add_username(self, username: str, status: str = "esperando") -> dict:
        """Add new username with status"""
        try:
            payload = {
                "username": username,
                "status": status,
                "added_at": datetime.now().isoformat()
            }
            response = self.supabase.table(self.table_name).insert(payload).execute()
            print(f"✅ Added @{username} with status: {status}")
            return {"success": True, "data": response.data[0] if response.data else None}
        except Exception as e:
            print(f"❌ Error adding username: {e}")
            return {"success": False, "error": str(e)}
    
    def update_status(self, username: str, status: str, file_path: str = None) -> dict:
        """Update username status"""
        try:
            payload = {
                "status": status,
                "updated_at": datetime.now().isoformat()
            }
            if file_path:
                payload["file_path"] = file_path
            if status == "print feito":
                payload["print_at"] = datetime.now().isoformat()
            
            response = self.supabase.table(self.table_name).update(payload).eq("username", username).execute()
            print(f"✅ Updated @{username} status to: {status}")
            return {"success": True, "data": response.data[0] if response.data else None}
        except Exception as e:
            print(f"❌ Error updating status: {e}")
            return {"success": False, "error": str(e)}
    
    def get_pending_usernames(self) -> list:
        """Get all usernames with status 'esperando'"""
        try:
            response = self.supabase.table(self.table_name).select("username").eq("status", "esperando").execute()
            return [item["username"] for item in response.data] if response.data else []
        except Exception as e:
            print(f"❌ Error fetching pending: {e}")
            return []
    
    def get_all_with_status(self, status: str = None) -> list:
        """Get all usernames, optionally filtered by status"""
        try:
            query = self.supabase.table(self.table_name).select("*")
            if status:
                query = query.eq("status", status)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []


# Test function
if __name__ == "__main__":
    db = SupabaseFollowersDB()
    
    # Test: Check if username exists
    print("\n🔍 Testing check_username_exists:")
    result = db.check_username_exists("thiagofinch")
    print(json.dumps(result, indent=2))
    
    # Test: Add username if doesn't exist
    print("\n➕ Testing add_username:")
    existing = db.check_username_exists("thiagofinch")
    if not existing["exists"]:
        result = db.add_username("thiagofinch", "esperando")
        print(json.dumps(result, indent=2))
    else:
        print("✅ Username already exists")
    
    # Test: Get pending
    print("\n⏳ Testing get_pending_usernames:")
    pending = db.get_pending_usernames()
    print(f"Pending: {pending}")
