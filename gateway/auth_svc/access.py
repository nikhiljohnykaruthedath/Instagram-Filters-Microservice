import os, requests

"""
    Login function to authenticate the user using the Auth Service.

    Args:
        request (Request): The incoming request object.

    Returns:
        tuple: A tuple containing the response text and status code.
"""
def login(request):
    auth = request.authorization

    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    # login using auth service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
