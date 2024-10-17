class PasswordChecker:
    def __init__(self, password):
        self.password = password

    def is_min_length(self):
        return len(self.password) >= 8

    def contains_lowercase(self):
        return any(x.islower() for x in self.password)

    def contains_uppercase(self):
        return any(x.isupper() for x in self.password)

    def contains_number(self):
        return any(x.isdigit() for x in self.password)

    def validate(self):
        return (self.is_min_length() and
                self.contains_lowercase() and
                self.contains_uppercase() and
                self.contains_number())
