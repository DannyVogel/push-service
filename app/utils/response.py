def success_response(data=None, message="Success", status_code=200):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
    } 