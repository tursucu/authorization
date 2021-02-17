from flask import current_app


def _get_jwt_manager():
    try:
        return current_app.extensions["authorization"]
    except KeyError:  # pragma: no cover
        raise RuntimeError(
            "You must initialize a JWTManager with this flask "
            "application before using this method"
        )
