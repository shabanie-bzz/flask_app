class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def authenticate(users, username, password):
        """Authenticate a user based on username and password."""
        for user in users:
            if user.username == username and user.password == password:
                return user
        return None
