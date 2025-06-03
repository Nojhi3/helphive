from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb
import MySQLdb.cursors
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="1234",
        db="helphive",
        cursorclass=MySQLdb.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Logic to save user
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

@app.route('/services')
def services():
    services_list = [
        {'name': 'Cleaning', 'image': 'images/cleaning.jpg'},
        {'name': 'Electrician', 'image': 'images/electrician.jpg'},
        {'name': 'Doctor Visit', 'image': 'images/doctor.jpg'},
        {'name': 'Salon & Spa', 'image': 'images/salon&spa.jpg'},
        {'name': 'Home Painting', 'image': 'images/homepainting.jpg'}
    ]
    return render_template('services.html', services=services_list)

@app.route('/provider_cleaning')
def provider_cleaning():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Filter only cleaning category
    cleaning_providers = [provider for provider in provider_data if provider.get('category', '').lower() == 'cleaning']

    # Check if photo exists
    for provider in cleaning_providers:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'  # Fallback to default

    return render_template('provider_cleaning.html', providers=cleaning_providers)

@app.route('/provider_electrician')
def provider_electrician():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_electrician= [p for p in provider_data if p.get('category', '').lower() == 'electrician']

    for provider in provider_electrician:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'

    return render_template('provider_electrician.html', providers=provider_electrician)

@app.route('/provider_plumber')
def provider_plumber():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_plumber = [p for p in provider_data if p.get('category', '').lower() == 'plumber']

    for provider in provider_plumber:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'

    return render_template('provider_plumber.html', providers=provider_plumber)

@app.route('/provider_daycare')
def provider_daycare():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_daycare = [p for p in provider_data if p.get('category', '').lower() == 'daycare']

    for provider in provider_daycare:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'
    return render_template('provider_daycare.html', providers=provider_daycare)

@app.route('/provider_doctor')
def provider_doctor():
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM providers")
    provider_data = cursor.fetchall()
    cursor.close()
    conn.close()

    provider_doctor = [p for p in provider_data if p.get('category', '').lower() == 'doctor']

    for provider in provider_doctor:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], provider.get('photo_url', ''))
        if not provider.get('photo_url') or not os.path.isfile(image_path):
            provider['photo_url'] = 'images/default.jpg'
    return render_template('provider_doctor.html', providers=provider_doctor)

""" @app.route('/book/<int:provider_id>', methods=['GET', 'POST'])
def book(provider_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM providers WHERE provider_id = %s", (provider_id,))
    provider = cursor.fetchone()

    if not provider:
        return "Provider not found", 404

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']

        # Optional: Insert booking into DB
        cursor.execute("INSERT INTO bookings (provider_id, user_name, date, time) VALUES (%s, %s, %s, %s)",
                       (provider_id, name, date, time))
        conn.commit()

        cursor.close()
        conn.close()
        return f"Thank you {name}, your appointment with {provider['name']} is booked for {date} at {time}."

    cursor.close()
    conn.close()
    return render_template('book.html', provider=provider) """

@app.route('/book/<int:provider_id>', methods=['GET', 'POST'])
def book(provider_id):
    conn = get_db_connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    # Fetch provider details
    cursor.execute("SELECT * FROM providers WHERE provider_id = %s", (provider_id,))
    provider = cursor.fetchone()

    if not provider:
        cursor.close()
        conn.close()
        return "Provider not found", 404

    # ✅ Get service_name and description using service_id
    cursor.execute("SELECT service_name, description FROM services WHERE service_name = %s", (provider['category'],))
    service = cursor.fetchone()
    service_name = service['service_name'] if service else 'Unknown'
    service_description = service['description'] if service else 'No description available.'

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        date = request.form['date']
        time = request.form['time']
        scheduled_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        cursor.execute("""
            INSERT INTO bookings (customer_name, provider_name, service_name, scheduled_time)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, provider['name'], service_name, scheduled_time))
        conn.commit()

        cursor.close()
        conn.close()
        return '''
                <script>
                alert("Booking confirmed!");
                window.location.href = "/";
                </script>
                '''

    cursor.close()
    conn.close()
    return render_template('book.html', provider=provider, service_name=service_name, service_description=service_description)


if __name__ == '__main__':
    app.run(debug=True)
