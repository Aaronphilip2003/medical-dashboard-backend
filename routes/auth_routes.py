from fastapi import APIRouter, HTTPException
from database.connection import client
import hashlib

router = APIRouter()

@router.post("/login")
async def login(body: dict):
    try:
        username = body["username"]
        password = body["password"]
        
        # Get stored credentials for the username
        query = f"SELECT password_hash, salt FROM Admins WHERE username = '{username}'"
        result = client.query(query)
        
        if not result.result_rows:
            return {"success": False, "message": "Invalid credentials"}
            
        stored_hash, stored_salt = result.result_rows[0]
        
        # Hash the input password with stored salt
        input_password = password + stored_salt
        input_hash = hashlib.sha256(input_password.encode()).hexdigest()
        
        # Compare hashes
        if input_hash == stored_hash:
            return {
                "success": True,
                "message": "Login successful",
                "username": username
            }
        else:
            return {"success": False, "message": "Invalid credentials"}

    except Exception as e:
        return {"success": False, "message": str(e)} 