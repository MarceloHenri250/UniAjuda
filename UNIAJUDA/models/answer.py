class Answer:
    def __init__(self, id, question_id, answer, user_id=None, user_name=None):
        self.id = id
        self.question_id = question_id
        self.answer = answer
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return (
            f"Answer(id={self.id}, question_id={self.question_id}, answer={self.answer}, user_id={self.user_id}, user_name={self.user_name})"
        )