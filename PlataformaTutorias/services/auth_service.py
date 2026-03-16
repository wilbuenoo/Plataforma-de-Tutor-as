class AuthService:

    users = [
        {"username": "wilfredo", "password": "feid", "role": "Administrador"},
        {"username": "juan", "password": "1234", "role": "Docente"},
        {"username": "ana", "password": "1234", "role": "Estudiante"}
    ]

    def login(self, username, password, role):

        for user in self.users:
            if (
                user["username"] == username
                and user["password"] == password
                and user["role"] == role
            ):
                return user

        return None