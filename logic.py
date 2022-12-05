#ATRS Python Flask File
#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
 # conn = pymysql.connect(host='localhost',
 #                        user='root',
 #                        password='',
 #                        db='air_ticket_reservation_system',
 #                        charset='utf8mb4',
 #                        cursorclass=pymysql.cursors.DictCursor)

# Configure MySQL

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       port= 8889,
                       db='Air Ticket Reservation System',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

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
    email = request.form['email']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT email, password, first_name FROM Customer WHERE email = %s and password = %s'
    cursor.execute(query, (email, password))
    #stores the results in a variable
    data = cursor.fetchone()
    print(data)
    first_name = data['first_name']
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['email'] = email
        session['first_name'] = first_name
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
@app.route('/registerCustomer', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']  # STRAIGHT UP STORING PASSWORD. CHANGE LATER!!!!
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Customer WHERE first_name = %s AND last_name = %s AND phone_number = %s'
    cursor.execute(query, (first_name, last_name, phone_number))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = """INSERT INTO Customer (first_name, last_name, email, password,
                building_number, street, city, state, phone_number,
                passport_number,passport_expiration, passport_country,
                date_of_birth)VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(ins, (first_name, last_name, email, password,
                        building_number, street, city, state, phone_number,
                        passport_number, passport_expiration, passport_country,
                        date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('customer_login.html')

@app.route('/home_unlog')
def home_unlog():
    return render_template('home_unlog.html')

@app.route('/home_customer')
def home_customer():
    return render_template('home_customer.html')


@app.route('/search', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    # departure_date = request.form['departure_date']
    # return_date = request.form['return_date']
    query = 'SELECT * FROM Flight WHERE departure_airport = %s and arrival_airport = %s'
    cursor.execute(query, (departure_airport, arrival_airport))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['flight_number'])
    cursor.close()
    return render_template('home_customer.html', username = username, flights = data1)

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
