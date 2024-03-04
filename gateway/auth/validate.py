import os, requests

"""
    This function is used to validate the authorization token
    sent by the client in the request header using the Auth Service.

    Args:
        request (Request): The incoming request from the client.

    Returns:
        tuple: A tuple containing the user's information and an error, if any.
"""
def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    # validate if the token is valid using the auth service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
