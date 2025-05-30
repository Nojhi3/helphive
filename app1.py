from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

# Mock data for services and providers
services_list = [
    {'id': 1, 'name': 'Cleaning', 'image': 'images/cleaning.jpg', 'description': 'Home and office cleaning services.'},
    {'id': 2, 'name': 'Electrician', 'image': 'images/electrician.jpg', 'description': 'Expert electrical repair and installation.'},
    {'id': 3, 'name': 'Doctor Visit', 'image': 'images/doctor.jpg', 'description': 'Home doctor visits and consultations.'},
    {'id': 4, 'name': 'Salon & Spa', 'image': 'images/salon&spa.jpg', 'description': 'Salon and spa services at home.'},
    {'id': 5, 'name': 'Home Painting', 'image': 'images/homepainting.jpg', 'description': 'Professional home painting service.'}
]

users = []  # In-memory user list

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple check for mock login
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

        # Store the user in the in-memory list
        users.append({'username': username, 'email': email, 'password': password})
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

@app.route('/services')
def services():
    return render_template('services.html', services=services_list)


if __name__ == '__main__':
    app.run(debug=True)
