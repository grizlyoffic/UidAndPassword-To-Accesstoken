from fastapi import FastAPI, Query, HTTPException
import aiohttp
import uvicorn
from typing import Optional

app = FastAPI(title="Free Fire Access Token API")

@app.get("/access_token")
async def get_access_token(
    uid: str = Query(..., description="Free Fire UID"),
    password: str = Query(..., description="Free Fire Password")
):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G965F) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "open_id": result.get("open_id"),
                        "access_token": result.get("access_token"),
                        "expires_in": result.get("expires_in"),
                        "token_type": result.get("token_type"),
                        "refresh_token": result.get("refresh_token")
                    }
                else:
                    raise HTTPException(
                        status_code=response.status,
                        detail={
                            "success": False,
                            "error": f"HTTP Error {response.status}",
                            "details": await response.text()
                        }
                    )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)