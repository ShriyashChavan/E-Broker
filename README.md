# E BROKERR - Rental Property Management System

A production-ready Python web application for managing rental properties, built with Flask and MySQL.

## Features

### User Roles
- **Tenant**: Search properties, book appointments, leave feedback
- **Landlord**: Add/manage properties, handle appointments, view feedback
- **Admin**: Full system management and monitoring

### Core Functionality
- Secure user authentication with JWT tokens
- Property CRUD operations with image uploads
- Advanced property search with filters
- Appointment booking and management
- Feedback and rating system
- REST API for mobile app integration
- Responsive Bootstrap UI

## Tech Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 
- **Database**: MySQL
- **Authentication**: Flask-Login + JWT
- **Security**: bcrypt password hashing, CSRF protection

## Project Structure

```
e-brokerr/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/              # Blueprint modules
│   │   ├── auth.py          # Authentication routes
│   │   ├── properties.py    # Property management
│   │   ├── appointments.py  # Appointment handling
│   │   ├── feedback.py      # Feedback system
│   │   └── admin.py         # Admin dashboard
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── database_setup.py        # Database initialization
├── requirements.txt          # Python dependencies
└── README.md               # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### 1. Clone/Download the Project
```bash
cd /path/to/your/projects
# Copy the project files to your desired location
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database
```sql
CREATE DATABASE e_brokerr;
CREATE USER 'ebrokerr_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON e_brokerr.* TO 'ebrokerr_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+mysqlconnector://ebrokerr_user:your_password@localhost/e_brokerr
JWT_SECRET_KEY=your-jwt-secret-key
```

Or update `config.py` with your database credentials.

### 6. Initialize Database
```bash
python database_setup.py
```

This creates all tables and a default admin user:
- **Email**: admin@ebrokerr.com
- **Password**: admin123

### 7. Run the Application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Default Admin Login
- URL: `http://localhost:5000/login`
- User Type: Admin
- Email: admin@ebrokerr.com
- Password: admin123

### API Endpoints

The application provides REST API endpoints for mobile app integration:

#### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration

#### Properties
- `GET /api/properties` - Get all properties
- `POST /api/properties/search` - Search properties with filters

#### Appointments
- `POST /api/appointments/book` - Book appointment
- `GET /api/appointments/landlord` - Get landlord appointments
- `POST /api/appointments/update_status` - Update appointment status

#### Feedback
- `POST /api/feedback/add` - Add feedback
- `GET /api/feedback/property/<pno>` - Get property feedback

#### Admin
- `GET /api/stats` - Get system statistics
- `GET /api/tenants` - Get all tenants
- `GET /api/landlords` - Get all landlords

### File Uploads
- Property images are stored in `app/static/images/`
- Maximum file size: 16MB
- Supported formats: JPG, PNG, GIF

## Security Features

- Password hashing with bcrypt
- CSRF protection
- SQL injection prevention via SQLAlchemy
- XSS protection
- Secure file uploads with validation
- JWT token authentication for API
- Session management

## Development

### Adding New Features
1. Create new routes in appropriate blueprint
2. Add database models if needed
3. Create/update templates
4. Update API endpoints if required

### Database Migrations
When changing models:
```bash
# Backup your data first!
# Then recreate tables (development only)
python database_setup.py
```

### Testing
```bash
# Run with debug mode
python run.py
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql+mysqlconnector://user:password@host:port/database
JWT_SECRET_KEY=your-production-jwt-secret
FLASK_ENV=production
```

### Nginx Configuration (example)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 1y;
    }
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL server is running
   - Verify database credentials in config.py
   - Ensure database and user exist

2. **Import Errors**
   - Activate virtual environment
   - Install all requirements: `pip install -r requirements.txt`

3. **File Upload Issues**
   - Check upload folder permissions
   - Verify folder exists: `app/static/images/`

4. **Template Not Found**
   - Ensure all template files are in `app/templates/`
   - Check file naming and paths

### Logs
Check console output for error messages when running `python run.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use and modify as needed.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.