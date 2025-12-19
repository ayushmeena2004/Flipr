from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os
from config import Config
from database import get_db_connection, init_db

app = Flask(__name__)
app.config.from_object(Config)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'projects'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'clients'), exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def crop_and_save_image(file, folder, size):
    """Crop image to specified size and save"""
    filename = secure_filename(file.filename)
    img = Image.open(file)
    
    # Convert RGBA to RGB if necessary
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Crop image to center
    width, height = img.size
    target_width, target_height = size
    
    # Calculate aspect ratios
    aspect = width / height
    target_aspect = target_width / target_height
    
    if aspect > target_aspect:
        # Image is wider than target
        new_width = int(height * target_aspect)
        offset = (width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, height))
    else:
        # Image is taller than target
        new_height = int(width / target_aspect)
        offset = (height - new_height) // 2
        img = img.crop((0, offset, width, offset + new_height))
    
    # Resize to target size
    img = img.resize(size, Image.Resampling.LANCZOS)
    
    # Save image
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    img.save(filepath)
    
    return f"uploads/{folder}/{filename}"

# Landing Page Routes
@app.route('/')
def index():
    """Render landing page"""
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    """Get all projects"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(projects)

@app.route('/api/clients')
def get_clients():
    """Get all clients"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
    clients = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(clients)

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    data = request.form
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO contact_forms (full_name, email, mobile, city)
        VALUES (%s, %s, %s, %s)
    """, (data['full_name'], data['email'], data['mobile'], data['city']))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({'success': True, 'message': 'Contact form submitted successfully!'})

@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    data = request.form
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO newsletter_subscribers (email)
            VALUES (%s)
        """, (data['email'],))
        connection.commit()
        message = 'Successfully subscribed to newsletter!'
        success = True
    except:
        message = 'Email already subscribed!'
        success = False
    
    cursor.close()
    connection.close()
    
    return jsonify({'success': success, 'message': message})

# Admin Panel Routes
@app.route('/admin')
def admin():
    """Render admin dashboard"""
    return render_template('admin.html')

@app.route('/admin/projects')
def admin_projects():
    """Render admin projects page"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_projects.html', projects=projects)

@app.route('/admin/projects/add', methods=['POST'])
def add_project():
    """Add new project"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file'})
    
    # Crop and save image
    image_path = crop_and_save_image(file, 'projects', Config.PROJECT_IMAGE_SIZE)
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO projects (name, description, image)
        VALUES (%s, %s, %s)
    """, (request.form['name'], request.form['description'], image_path))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('admin_projects'))

@app.route('/admin/clients')
def admin_clients():
    """Render admin clients page"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
    clients = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_clients.html', clients=clients)

@app.route('/admin/clients/add', methods=['POST'])
def add_client():
    """Add new client"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid file'})
    
    # Crop and save image
    image_path = crop_and_save_image(file, 'clients', Config.CLIENT_IMAGE_SIZE)
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO clients (name, description, designation, image)
        VALUES (%s, %s, %s, %s)
    """, (request.form['name'], request.form['description'], 
          request.form['designation'], image_path))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('admin_clients'))

@app.route('/admin/contacts')
def admin_contacts():
    """Render admin contacts page"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contact_forms ORDER BY submitted_at DESC")
    contacts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_contacts.html', contacts=contacts)

@app.route('/admin/subscribers')
def admin_subscribers():
    """Render admin subscribers page"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM newsletter_subscribers ORDER BY subscribed_at DESC")
    subscribers = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('admin_subscribers.html', subscribers=subscribers)

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
