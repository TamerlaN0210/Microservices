class Offer:
    def __init__(self, dict_: dict):
        self.user_id = dict_.get("user_id")
        self.title = dict_.get("title")
        self.text = dict_.get("text")
        self.created_at = dict_.get("created_at")

    def is_valid(self):
        if self.user_id is not None and type(self.user_id) is int and\
                self.title is not None and type(self.title) is str and\
                self.text is not None and type(self.text) is str and\
                self.created_at is not None and type(self.created_at) is int:
            return True
        else:
            return False
