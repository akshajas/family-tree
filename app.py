from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# A dictionary to store user data (for demonstration purposes)
users = {}

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        # Save user data
        users[username] = {
            'email': email,
            'active': False,
            'family': []
        }
        
        session['username'] = username
        
        return redirect('/family-details')

    return render_template('signup.html')

# Route for the family details page
@app.route('/family-details', methods=['GET', 'POST'])
def family_details():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    user = users[username]
    
    if request.method == 'POST':
        name = request.form['name']
        relationship = request.form['relationship']
        
        # Add family member to user's family
        user['family'].append({
            'name': name,
            'relationship': relationship
        })
        
        return redirect('/family-tree')

    return render_template('family_details.html')

# Route for the family tree page
@app.route('/family-tree')
def family_tree():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    user = users[username]
    family = user['family']
    
    return render_template('family_tree.html', family=family)

# Route for the admin panel
@app.route('/admin')
def admin_panel():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin/login')
    
    return render_template('admin_panel.html', users=users)

# Route for the admin login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error='Invalid username or password.')

    return render_template('admin_login.html')

# Route to activate or deactivate a user
@app.route('/admin/activate/<username>')
def activate_user(username):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin/login')
    
    if username in users:
        users[username]['active'] = not users[username]['active']
    
    return redirect('/admin')

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
