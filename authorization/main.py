class GraphQLAuth(object):
    """
    An object used to hold JWT settings for the
    Flask-GraphQL-Auth extension.

    Instances of :class:`GraphQLAuth` are *not* bound to specific apps, so
    you can create one in the main body of your code and then bind it
    to your app in a factory function.
    """

    def __init__(self, app=None):
        """
        Create the GraphQLAuth instance. You can either pass a flask application in directly
        here to register this extension with the flask app, or call init_app after creating
        this object (in a factory pattern).
        :param app: A flask application
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Register this extension with the flask app.

        :param app: A flask application
        """
        # Check jwt_secret_key or secret_key is defined in app config
        secret_key = app.config.get("JWT_SECRET_KEY") or app.config.get("SECRET_KEY")
        if not secret_key:
            raise Exception('\'JWT_SECRET_KEY\' missing from app configuration.')

        # Save this so we can use it later in the extension
        if not hasattr(app, "extensions"):  # pragma: no cover
            app.extensions = {}
        app.extensions["auth-reportgg"] = self

        self._set_default__configuration_options(app)

    @staticmethod
    def _set_default__configuration_options(app):
        """
        Sets the default configuration options used by this extension
        """
        app.config.setdefault(
            "JWT_TOKEN_ARGUMENT_NAME", "token"
        )

        app.config.setdefault("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))

        # These settings are related to header authentication only
        app.config.setdefault("JWT_HEADER_NAME", "Authorization")
        app.config.setdefault("JWT_HEADER_TOKEN_PREFIX", "Bearer")
