#ATRS Python Flask File
#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        db='air_ticket_reservation_system',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# Configure MySQL
"""
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       port= 8889,
                       db='Air Ticket Reservation System',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
"""
#Define a route to hello function
@app.route('/')
def hello():
    return render_template('home_unlog.html')

#Define route for customer login
@app.route('/customer_login')
def customer_login():
    return render_template('customer_login.html')

#Define route for staff login
@app.route('/staff_login')
def staff_login():
    return render_template('staff_login.html')

#Define route for customer register
@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')

#Define route for customer register
@app.route('/staff_register')
def staff_register():
    return render_template('staff_register.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the customer login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    email = request.form['username']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT email, password FROM Customer WHERE email = %s and password = %s'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = email
        return redirect(url_for('home_customer'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)

#Authenticates the staff login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT username, password FROM Airline_Staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home_unlog'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('staff_login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s)'
        cursor.execute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')

@app.route('/home_unlog')
def home_unlog():
    return render_template('home_unlog.html')
    
@app.route('/home_customer')
def home_customer():
    return render_template('home_customer.html')


@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
