from app import create_app, db
from app.models import Landlord, Property, Tenant, Admin
import random

def add_sample_data():
    app = create_app()
    with app.app_context():
        # Create sample landlords
        landlords_data = [
            {'lname': 'Rajesh Kumar', 'lemail': 'rajesh@example.com', 'contact': '9876543210'},
            {'lname': 'Priya Sharma', 'lemail': 'priya@example.com', 'contact': '9876543211'},
            {'lname': 'Amit Singh', 'lemail': 'amit@example.com', 'contact': '9876543212'},
            {'lname': 'Sneha Patel', 'lemail': 'sneha@example.com', 'contact': '9876543213'},
            {'lname': 'Vikram Joshi', 'lemail': 'vikram@example.com', 'contact': '9876543214'},
        ]

        landlords = []
        for data in landlords_data:
            landlord = Landlord(
                lname=data['lname'],
                lemail=data['lemail'],
                contact=data['contact']
            )
            landlord.set_password('password123')
            landlords.append(landlord)
            db.session.add(landlord)

        db.session.commit()

        # Property data templates
        property_types = ['Apartment', 'House', 'Villa', 'Studio', 'Penthouse']
        locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Pune', 'Hyderabad', 'Kolkata', 'Ahmedabad']
        addresses = [
            '123 MG Road, Near Central Mall',
            '456 Brigade Road, Opposite Park',
            '789 Residency Road, Close to Metro',
            '321 Cunningham Road, Near Hospital',
            '654 Richmond Road, Opposite School',
            '987 Koramangala, Near IT Park',
            '147 Indiranagar, Close to Market',
            '258 Jayanagar, Near Temple',
            '369 Whitefield, Opposite Mall',
            '741 HSR Layout, Near BTM'
        ]

        # Create sample properties
        properties_data = []
        for i in range(20):  # Create 20 sample properties
            landlord = random.choice(landlords)
            ptype = random.choice(property_types)
            location = random.choice(locations)
            address = random.choice(addresses)
            bhk = random.randint(1, 4)
            carpet = random.randint(5000, 50000)  # Rent between 5k-50k
            no_of_tenant = random.randint(1, 4)

            property_obj = Property(
                ptype=ptype,
                paddress=f'{address}, {location}',
                plocation=location,
                carpet=float(carpet),
                bhk=bhk,
                no_of_tenant=no_of_tenant,
                lid=landlord.lid
            )
            properties_data.append(property_obj)
            db.session.add(property_obj)

        db.session.commit()

        # Create sample tenants
        tenants_data = [
            {'tname': 'Arun Kumar', 'temail': 'arun@example.com', 'tage': 28, 'tcontact': '9123456789'},
            {'tname': 'Meera Iyer', 'temail': 'meera@example.com', 'tage': 25, 'tcontact': '9123456790'},
            {'tname': 'Rohan Gupta', 'temail': 'rohan@example.com', 'tage': 32, 'tcontact': '9123456791'},
            {'tname': 'Kavita Rao', 'temail': 'kavita@example.com', 'tage': 29, 'tcontact': '9123456792'},
            {'tname': 'Suresh Menon', 'temail': 'suresh@example.com', 'tage': 35, 'tcontact': '9123456793'},
        ]

        for data in tenants_data:
            tenant = Tenant(
                tname=data['tname'],
                temail=data['temail'],
                tage=data['tage'],
                tcontact=data['tcontact']
            )
            tenant.set_password('password123')
            db.session.add(tenant)

        db.session.commit()

        print("Sample data added successfully!")
        print(f"Created {len(landlords)} landlords")
        print(f"Created {len(properties_data)} properties")
        print(f"Created {len(tenants_data)} tenants")

if __name__ == '__main__':
    add_sample_data()