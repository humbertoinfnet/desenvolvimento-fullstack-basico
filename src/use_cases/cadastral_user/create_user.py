from src.entities.cadastral_user import User


class CreateUserUseCase:
    def execute(self, user_data):
        user = User(**user_data)
        # Lógica para criar usuário
        return user
