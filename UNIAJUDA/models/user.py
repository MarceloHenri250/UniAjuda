class User:
    def __init__(self, id, nome, matricula, curso, email, instituicao, senha):
        # Inicializa um novo usuário com os atributos fornecidos
        self.id = id  # Identificador único do usuário
        self.nome = nome  # Nome do usuário
        self.matricula = matricula  # Número de matrícula do usuário
        self.curso = curso  # Curso do usuário
        self.email = email  # Email do usuário
        self.instituicao = instituicao  # Instituição do usuário
        self.senha = senha  # Senha do usuário

    def __repr__(self):
        # Retorna uma representação legível do objeto User
        return f"<User {self.nome} ({self.matricula})>"