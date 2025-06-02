class Question:
    def __init__(
        self,
        id,
        title,
        description,
        disciplina=None,
        votes=0,
        user_id=None,
        user_name=None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.disciplina = disciplina
        self.votes = votes
        self.user_id = user_id
        self.user_name = user_name  # Nome do usuário dono da pergunta

    def __repr__(self):
        return (
            f"Question(id={self.id}, title={self.title}, disciplina={self.disciplina}, votes={self.votes}, user_id={self.user_id}, user_name={self.user_name})"
        )