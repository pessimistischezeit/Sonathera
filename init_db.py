from app import db, app
from app import User  

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")
        
        admin_email = "nikolozikhachishvili@gmail.com"
        
if __name__ == "__main__":
    init_db()
