# Portfolio Flask Application

A full-stack portfolio management application built with Flask, MySQL, HTML, and CSS.

## Features

### Landing Page
- **Our Projects Section**: Display all projects with images, names, descriptions, and read more buttons
- **Happy Clients Section**: Display client testimonials with images, names, descriptions, and designations
- **Contact Form**: Allow users to submit contact information (name, email, mobile, city)
- **Newsletter Subscription**: Allow users to subscribe with their email address

### Admin Panel
- **Project Management**: Add new projects with image upload (auto-cropped to 450x350)
- **Client Management**: Add client testimonials with image upload (auto-cropped to 450x350)
- **Contact Form Details**: View all contact form submissions
- **Newsletter Subscribers**: View all newsletter subscribers

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher

### Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MySQL database**:
   - Create a MySQL database or let the application create it automatically
   - Update the `.env` file with your database credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=your_password
     DB_NAME=portfolio_db
     SECRET_KEY=your-secret-key
     ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Landing Page: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin

## Project Structure

```
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database connection and initialization
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── static/
│   ├── style.css         # CSS styles
│   └── uploads/          # Uploaded images (auto-created)
│       ├── projects/
│       └── clients/
└── templates/
    ├── index.html        # Landing page
    ├── admin.html        # Admin dashboard
    ├── admin_projects.html      # Project management
    ├── admin_clients.html       # Client management
    ├── admin_contacts.html      # Contact form details
    └── admin_subscribers.html   # Newsletter subscribers
```

## Features Implementation

### Image Cropping (Bonus Feature)
- Automatically crops uploaded images to 450x350 pixels
- Uses PIL (Pillow) for image processing
- Maintains aspect ratio during cropping
- Saves optimized images to the server

### Database Tables
- **projects**: id, name, description, image, created_at
- **clients**: id, name, description, designation, image, created_at
- **contact_forms**: id, full_name, email, mobile, city, submitted_at
- **newsletter_subscribers**: id, email (unique), subscribed_at

## API Endpoints

### Public Endpoints
- GET `/` - Landing page
- GET `/api/projects` - Get all projects
- GET `/api/clients` - Get all clients
- POST `/api/contact` - Submit contact form
- POST `/api/newsletter` - Subscribe to newsletter

### Admin Endpoints
- GET `/admin` - Admin dashboard
- GET `/admin/projects` - Projects management page
- POST `/admin/projects/add` - Add new project
- GET `/admin/clients` - Clients management page
- POST `/admin/clients/add` - Add new client
- GET `/admin/contacts` - View contact submissions
- GET `/admin/subscribers` - View newsletter subscribers

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Image Processing**: Pillow (PIL)
- **Other**: python-dotenv for environment variables

## Notes

- The database is automatically initialized on first run
- Images are automatically cropped to the specified dimensions (450x350)
- The admin panel has no authentication (add authentication for production use)
- All forms include client-side and server-side validation
