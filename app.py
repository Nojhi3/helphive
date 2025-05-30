from flask import Flask, request, redirect, render_template, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",
        database="helphive"
    )
    return conn

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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Add logic to store/register the user
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

@app.route('/services')
def services():
    # You can pass a list of services to the template if needed
    services_list = [
        {'name': 'Cleaning', 'image': 'images/cleaning.jpg'},
        {'name': 'Electrician', 'image': 'images/electrician.jpg'},
        {'name': 'Doctor Visit', 'image': 'images/doctor.jpg'},
        {'name': 'Salon & Spa', 'image': 'images/salon&spa.jpg'},
        {'name': 'Home Painting', 'image': 'images/homepainting.jpg'}
    ]
    return render_template('services.html', services=services_list)





if __name__ == '__main__':
    print("Starting Flask...")
    app.run(debug=True)












