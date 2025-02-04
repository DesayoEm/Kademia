from sqlalchemy.orm import Session

class BaseCrud:
    def __init__(self, db:Session, model):
        self.model = model
        self.db = db

    def base_query(self):
        return self.db.query(self.model).filter(self.model.is_archived != True)