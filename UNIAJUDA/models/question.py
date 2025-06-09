class Question:
    def __init__(
        self,
        question_id,
        title,
        description,
        subject=None,
        votes=0,
        user_id=None,
        user_name=None,
        attachment=None,
    ):

        self.id = question_id
        self.title = title
        self.description = description
        self.subject = subject
        self.votes = votes
        self.user_id = user_id
        self.user_name = user_name
        self.attachment = attachment

    def __repr__(self):

        return (
            f"Question(id={self.id}, title={self.title}, subject={self.subject}, votes={self.votes}, user_id={self.user_id}, user_name={self.user_name}, attachment={self.attachment})"
        )