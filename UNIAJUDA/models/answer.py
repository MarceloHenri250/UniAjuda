class Answer:
    def __init__(self, answer_id, question_id, answer_text, user_id=None, user_name=None):

        self.id = answer_id
        self.question_id = question_id
        self.answer = answer_text
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):

        return (
            f"Answer(id={self.id}, question_id={self.question_id}, answer={self.answer}, user_id={self.user_id}, user_name={self.user_name})"
        )