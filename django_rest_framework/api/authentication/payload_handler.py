

# Override JWT response so as to not return any data in the response body
# in a successful login (or refresh)
def jwt_response_payload_handler(token, user=None, request=None):
    return {}