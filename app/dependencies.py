from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    # TODO: Replace with real API key check
    if x_api_key != "your_api_key_here":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key 