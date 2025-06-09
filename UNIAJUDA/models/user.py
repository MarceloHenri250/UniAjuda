class User:
    def __init__(self, user_id, name, registration, course, email, institution, password, avatar=None):
    
        self.id = user_id
        self.name = name
        self.registration = registration
        self.course = course
        self.email = email
        self.institution = institution
        self.password = password
        self.avatar = avatar

    def __repr__(self):
        
        return f"<User {self.name} ({self.registration})>"