from app import create_app, db
from app.models import Tenant, Landlord, Admin, Property, Appointment, Feedback

def setup_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # Create a default admin user
        if not Admin.query.filter_by(aemail='admin@ebrokerr.com').first():
            admin = Admin(aname='Admin', aemail='admin@ebrokerr.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin@ebrokerr.com / admin123")

        print("Database setup complete!")

if __name__ == '__main__':
    setup_database()