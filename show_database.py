from app import create_app, db
from app.models import Tenant, Landlord, Admin, Property, Appointment, Feedback

def show_database():
    app = create_app()
    with app.app_context():
        print("🔍 E BROKERR DATABASE LIVE VIEW")
        print("=" * 50)

        # Count statistics
        tenants = Tenant.query.all()
        landlords = Landlord.query.all()
        admins = Admin.query.all()
        properties = Property.query.all()
        appointments = Appointment.query.all()
        feedbacks = Feedback.query.all()

        print(f"📊 STATISTICS:")
        print(f"   Tenants: {len(tenants)}")
        print(f"   Landlords: {len(landlords)}")
        print(f"   Admins: {len(admins)}")
        print(f"   Properties: {len(properties)}")
        print(f"   Appointments: {len(appointments)}")
        print(f"   Feedbacks: {len(feedbacks)}")
        print()

        # Show tenants
        if tenants:
            print("👥 TENANTS:")
            for t in tenants:
                print(f"   {t.tno}: {t.tname} ({t.temail}) - Age: {t.tage}, Contact: {t.tcontact}")
            print()

        # Show landlords
        if landlords:
            print("🏢 LANDLORDS:")
            for l in landlords:
                print(f"   {l.lid}: {l.lname} ({l.lemail}) - Contact: {l.contact}")
            print()

        # Show admins
        if admins:
            print("⚙️ ADMINS:")
            for a in admins:
                print(f"   {a.aid}: {a.aname} ({a.aemail})")
            print()

        # Show properties
        if properties:
            print("🏠 PROPERTIES:")
            for p in properties:
                print(f"   {p.pno}: {p.ptype} - {p.bhk}BHK in {p.plocation}, ₹{p.carpet} ({p.no_of_tenant} tenants)")
                print(f"       Address: {p.paddress}")
                print(f"       Landlord ID: {p.lid}, Image: {'Yes' if p.img1 else 'No'}")
            print()

        # Show appointments
        if appointments:
            print("📅 APPOINTMENTS:")
            for a in appointments:
                tenant = Tenant.query.get(a.tno)
                property_obj = Property.query.get(a.pno)
                landlord = Landlord.query.get(property_obj.lid) if property_obj else None
                print(f"   {a.ano}: {tenant.tname if tenant else 'Unknown'} → {property_obj.ptype if property_obj else 'Unknown'} ({landlord.lname if landlord else 'Unknown'})")
                print(f"       Date: {a.adate}, Status: {a.astatus}")
            print()

        # Show feedbacks
        if feedbacks:
            print("⭐ FEEDBACKS:")
            for f in feedbacks:
                tenant = Tenant.query.get(f.tno)
                property_obj = Property.query.get(f.pno)
                print(f"   {f.fid}: {tenant.tname if tenant else 'Unknown'} rated {property_obj.ptype if property_obj else 'Unknown'} {f.rating}/5")
                if f.comment:
                    print(f"       Comment: {f.comment}")
            print()

        print("✅ Database view complete!")

if __name__ == '__main__':
    show_database()