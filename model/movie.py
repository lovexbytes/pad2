import uuid

class Movie:
    
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        
    def generate_id(self):
        self.id = uuid.uuid4().hex

    def set_id(self, id):
        self.id = id

    def set_description(self, description):
        self.description = description
        
    def set_title(self, title):
        self.title = title
        
    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    