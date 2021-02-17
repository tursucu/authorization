from flask import _app_ctx_stack as ctx_stack, current_app, request
from functools import wraps
import jwt


def decode_jwt(encoded_token, secret, algorithm):
    """
    Decodes an encoded JWT

    :param encoded_token: The encoded JWT string to decode
    :param secret: Secret key used to encode the JWT
    :param algorithm: Algorithm used to encode the JWT
    :return: Dictionary containing contents of the JWT
    """
    # This call verifies the ext, iat, and nbf claims
    data = jwt.decode(encoded_token, secret, algorithms=[algorithm])

    return data


def get_jwt_data(token):
    """
    Decodes encoded JWT token by using extension setting and validates token type

    :param token: The encoded JWT string to decode
    :return: Dictionary containing contents of the JWT
    """
    jwt_data = decode_jwt(
        encoded_token=token,
        secret=current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    return jwt_data


def verify_jwt_in_argument(token):
    """
    Verify access token

    :param token: The encoded access type JWT string to decode
    :return: Dictionary containing contents of the JWT
    """
    jwt_data = get_jwt_data(token)
    ctx_stack.top.jwt = jwt_data


def verify_refresh_jwt_in_argument(token):
    """
    Verify refresh token

    :param token: The encoded refresh type JWT string to decode
    :return: Dictionary containing contents of the JWT
    """
    jwt_data = get_jwt_data(token)
    ctx_stack.top.jwt = jwt_data


def _extract_header_token_value(request_headers):
    """
    Header Token Control

    Extract token value from the request headers.

    It uses the token found in the header specified in the
    JWT_HEADER_NAME configuration variable and requires
    the token to have the prefix specified in the
    JWT_HEADER_TOKEN_PREFIX variable

    :param request_headers: Request headers as dict
    :return: Token value as a string (None if token is not found)
    """
    authorization_header = request_headers.get(current_app.config["JWT_HEADER_NAME"])
    token_prefix = current_app.config["JWT_HEADER_TOKEN_PREFIX"].lower()
    if authorization_header and authorization_header.lower().startswith(token_prefix):
        return authorization_header.split()[-1]
    return None


def header_jwt_required(fn):
    """
    A decorator to protect a mutation.

    If you decorate a mutation with this, it will ensure that the requester
    has a valid access token before allowing the mutation to be called. This
    does not check the freshness of the access token.
    """

    @wraps(fn)
    def wrapper(cls, *args, **kwargs):
        token = _extract_header_token_value(request.headers)

        try:
            verify_jwt_in_argument(token)
        except:
            raise Exception("TOKEN_BULUNAMADI")

        return fn(cls, *args, **kwargs)

    return wrapper


def header_jwt_role_detect(fn, UserModel):
    """
    Gerekli role sahip olmayan kullanıcıları engeller.
    """

    @wraps(fn)
    def wrapper(cls, *args, **kwargs):

        user = UserModel.objects.get(email=ctx_stack.top.jwt["email"])

        if user["role"] == "ADMIN":
            return fn(cls, *args, **kwargs)
        else:
            raise Exception("KULLANICI_ROL_HATASI")

    return wrapper
