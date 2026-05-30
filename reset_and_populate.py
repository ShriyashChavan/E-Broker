from app import create_app, db
from app.models import Landlord, Property, Tenant, Admin, Appointment, Feedback, PropertyImage

def reset_and_populate():
    app = create_app()
    with app.app_context():
        # Delete dependent tables first
        Feedback.query.delete()
        Appointment.query.delete()
        PropertyImage.query.delete()
        Property.query.delete()
        Tenant.query.delete()
        Landlord.query.delete()
        Admin.query.delete()
        db.session.commit()

        landlord_names = [
            'Aarav Sharma', 'Vivaan Verma', 'Aditya Singh', 'Arjun Nair', 'Vihaan Gupta',
            'Krishna Reddy', 'Ishaan Mehta', 'Kabir Joshi', 'Shaurya Rao', 'Atharv Malhotra',
            'Ayaan Bhat', 'Dev Patel', 'Reyansh Kulkarni', 'Dhruv Iyer', 'Ritvik Chawla',
            'Aniket Sood', 'Kunal Saxena', 'Harsh Vohra', 'Nikhil Agarwal', 'Siddharth Jain',
            'Manav Khanna', 'Pranav Sethi', 'Tushar Oberoi', 'Yash Bansal', 'Rohan Kapur',
            'Samar Arora', 'Vikas Chandra', 'Pankaj Mishra', 'Gautam Rawat', 'Sandeep Malhotra',
            'Amitabh Kulkarni', 'Suresh Nanda', 'Rakesh Tiwari', 'Sanjay Deshmukh', 'Naveen Pillai',
            'Deepak Vyas', 'Mohan Goyal', 'Ashok Pandey', 'Pradeep Khurana', 'Rajeev Mathur',
            'Harshit Joshi', 'Akhil Menon', 'Tarun Dutta', 'Abhishek Sinha', 'Mayank Batra',
            'Chetan Ahuja', 'Parth Shah', 'Raghav Kapoor', 'Kartik Bhatt', 'Saurabh Trivedi'
        ]

        landlords_data = []
        for index, name in enumerate(landlord_names, start=1):
            landlords_data.append({
                'lname': name,
                'lemail': f'{name.lower().replace(" ", ".")}@example.com',
                'contact': f'900000{index:04d}'
            })

        landlords = []
        for data in landlords_data:
            landlord = Landlord(lname=data['lname'], lemail=data['lemail'], contact=data['contact'])
            landlord.set_password('password123')
            landlords.append(landlord)
            db.session.add(landlord)

        db.session.commit()

        property_types = ['Apartment', 'House', 'Villa', 'Studio', 'Penthouse']
        locations = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Pune', 'Hyderabad', 'Kolkata', 'Ahmedabad']
        street_names = [
            'MG Road', 'Brigade Road', 'Residency Road', 'Linking Road', 'Bannerghatta Road',
            'Park Street', 'Golf Course Road', 'Anna Salai', 'Salt Lake Avenue', 'Ring Road'
        ]

        properties_data = []
        for index, landlord in enumerate(landlords, start=1):
            for property_number in range(2):
                property_index = (index - 1) * 2 + property_number + 1
                location = locations[(property_index - 1) % len(locations)]
                street = street_names[(property_index - 1) % len(street_names)]
                property_obj = Property(
                    ptype=property_types[(property_index - 1) % len(property_types)],
                    paddress=f'{property_index} {street}, {location}',
                    plocation=location,
                    carpet=float(600 + (property_index * 25)),
                    bhk=((property_index - 1) % 4) + 1,
                    no_of_tenant=((property_index - 1) % 4) + 1,
                    lid=landlord.lid
                )
                properties_data.append(property_obj)
                db.session.add(property_obj)

        db.session.commit()

        image_urls = [
            'https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1599423300746-b62533397364?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1605276374104-dee2a0ed3cd6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'
        ]

        property_images = []
        for index, prop in enumerate(properties_data):
            image_url = image_urls[index % len(image_urls)]
            prop.img1 = image_url
            property_image = PropertyImage(property_id=prop.pno, image_url=image_url)
            property_images.append(property_image)
            db.session.add(property_image)

        db.session.commit()

        tenant_names = [
            'Aarav Sharma', 'Vivaan Verma', 'Aditya Singh', 'Arjun Nair', 'Vihaan Gupta',
            'Krishna Reddy', 'Ishaan Mehta', 'Kabir Joshi', 'Shaurya Rao', 'Atharv Malhotra',
            'Ayaan Bhat', 'Dev Patel', 'Reyansh Kulkarni', 'Dhruv Iyer', 'Ritvik Chawla',
            'Aniket Sood', 'Kunal Saxena', 'Harsh Vohra', 'Nikhil Agarwal', 'Siddharth Jain',
            'Manav Khanna', 'Pranav Sethi', 'Tushar Oberoi', 'Yash Bansal', 'Rohan Kapur',
            'Samar Arora', 'Vikas Chandra', 'Pankaj Mishra', 'Gautam Rawat', 'Sandeep Malhotra',
            'Amitabh Kulkarni', 'Suresh Nanda', 'Rakesh Tiwari', 'Sanjay Deshmukh', 'Naveen Pillai',
            'Deepak Vyas', 'Mohan Goyal', 'Ashok Pandey', 'Pradeep Khurana', 'Rajeev Mathur',
            'Harshit Joshi', 'Akhil Menon', 'Tarun Dutta', 'Abhishek Sinha', 'Mayank Batra',
            'Chetan Ahuja', 'Parth Shah', 'Raghav Kapoor', 'Kartik Bhatt', 'Saurabh Trivedi',
            'Nitin Awasthi', 'Sahil Choudhary', 'Gaurav Pathak', 'Harpreet Singh', 'Madhav Kher',
            'Ojas Bedi', 'Bharat Joshi', 'Tejas Kulkarni', 'Naman Kapoor', 'Aman Saini',
            'Shivam Tandon', 'Ritesh Dahiya', 'Pulkit Arora', 'Yuvraj Chhabra', 'Deepanshu Rana',
            'Lokesh Vora', 'Kushal Thakur', 'Anurag Suri', 'Satyam Bansal', 'Rishabh Mallick',
            'Aryan Sethi', 'Hrithik Vohra', 'Manish Oberoi', 'Piyush Chawla', 'Aashish Trivedi',
            'Bhavesh Mehta', 'Chirag Nair', 'Dheeraj Rao', 'Eshaan Jain', 'Farhan Ali',
            'Girish Kumar', 'Himanshu Seth', 'Ishwar Kumar', 'Jatin Bhatia', 'Karan Lal',
            'Lalit Sharma', 'Mitesh Kapoor', 'Naveen Reddy', 'Omkar Joshi', 'Prashant Sinha',
            'Qasim Khan', 'Rajat Bansal', 'Sumeet Desai', 'Tanmay Singh', 'Utkarsh Gupta',
            'Varun Pillai', 'Wasim Ahmed', 'Yogesh Yadav', 'Zubin Dutta', 'Aseem Khurana'
        ]

        tenants_data = []
        for index, name in enumerate(tenant_names, start=1):
            tenants_data.append({
                'tname': name,
                'temail': f'{name.lower().replace(" ", ".")}@example.com',
                'tage': 21 + ((index - 1) % 15),
                'tcontact': f'910000{index:04d}'
            })

        for data in tenants_data:
            tenant = Tenant(tname=data['tname'], temail=data['temail'], tage=data['tage'], tcontact=data['tcontact'])
            tenant.set_password('password123')
            db.session.add(tenant)

        # Add a default admin
        admin = Admin(aname='Administrator', aemail='admin@example.com')
        admin.set_password('adminpass')
        db.session.add(admin)

        db.session.commit()

        print('Database reset complete.')
        print(f'Created {len(landlords)} landlords, {len(properties_data)} properties, {len(property_images)} property images, and {len(tenants_data)} tenants.')

if __name__ == '__main__':
    reset_and_populate()
