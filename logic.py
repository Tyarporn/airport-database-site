#ATRS Python Flask File
#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import date, datetime
import random
import json

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
# conn = pymysql.connect(host='localhost',
#                          user='root',
#                          password='',
#                          db='air_ticket_reservation_system',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)

# Configure MySQL

conn = pymysql.connect(host='localhost',
                      user='root',
                      password='root',
                      port= 8889,
                      db='air_ticket_reservation_system',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)


def search_flights(departure_airport,arrival_airport, departure_city, arrival_city, departure_date):
    cursor = conn.cursor();
    data1=None
    if((departure_city == "" and arrival_city == "") and (departure_airport != "" and arrival_airport != "")):
        print("Case1") # airport filled but not city
        query = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date >= %s'
        cursor.execute(query, (departure_airport, arrival_airport, departure_date))
        data1 = cursor.fetchall()
    elif((departure_airport == "" and arrival_airport == "") and (departure_city != "" and arrival_city != "")):
        print("Case2") # city filled but not airport
        query = 'SELECT * FROM Flight INNER JOIN Airport as A ON Flight.departure_airport = A.name INNER JOIN Airport as B ON Flight.arrival_airport = B.name WHERE A.city = %s and B.city = %s AND departure_date >= %s'
        cursor.execute(query, (departure_city, arrival_city, departure_date))
        data1 = cursor.fetchall()
    elif((departure_city != "" and arrival_city != "") and (departure_airport != "" and arrival_airport != "")):
        print("Case3") # all field filled just search case 1
        query = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date >= %s'
        cursor.execute(query, (departure_airport, arrival_airport, departure_date))
        data1 = cursor.fetchall()
    else:
        print("Case4") # any other combination
        error = "Search Error"
        return error
    cursor.close()
    return data1

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('home_unlog.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/cancel')
def cancel():
    # session['email'] = email
    return render_template('cancel.html')

@app.route('/change_flight_status')
def change_flight_status():
    return render_template('change_flight_status.html')

@app.route('/logged_out')
def logged_out():
    return render_template('logged_out.html')

@app.route('/remove_account')
def remove_account():
    return render_template('remove_account.html')

@app.route('/remove_staff_account')
def remove_staff_account():
    return render_template('remove_staff_account.html')

@app.route('/track_spending')
def track_spending():
    return render_template('track_spending.html')
    
@app.route('/earned_revenue')
def earned_revenue():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT SUM(sold_price) FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH);'
    cursor.execute(query, (airline_name))
    #stores the results in a variable
    data = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT SUM(sold_price) FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(NOW(), INTERVAL 1 YEAR);'
    cursor.execute(query, (airline_name))
    #stores the results in a variable
    data1 = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    return render_template('earned_revenue.html', username = username, airline_name = airline_name, previous_flights = previous_flights, current_flights = current_flights, last_month = data, last_year = data1)

@app.route('/new_flight')
def new_flight():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT ID, number_of_seats, manufacturer, age FROM Airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    #stores the results in a variable
    data = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    return render_template('new_flight.html', username = username, airline_name = airline_name, previous_flights = previous_flights, current_flights = current_flights)

@app.route('/new_airport')
def new_airport():
    return render_template('new_airport.html')

@app.route('/new_airplane')
def new_airplane():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT ID, number_of_seats, manufacturer, age FROM Airplane WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    #stores the results in a variable
    data = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    return render_template('new_airplane.html', username = username, airline_name = airline_name, previous_flights = previous_flights, current_flights = current_flights, airplane = data)

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

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    return render_template('buy.html')
    
#Define route for register
@app.route('/view_customers')
def view_customers():
    return render_template('view_customers.html')

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

        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_number, departure_date, departure_time FROM Ticket NATURAL JOIN Flight WHERE email = %s and departure_date < CURRENT_DATE()'
        cursor.execute(query, (email))
        previous_flights = cursor.fetchall()
        session['previous_flights'] = previous_flights
        for each in previous_flights:
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
        cursor.close()

        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, flight_status FROM Ticket NATURAL JOIN Flight WHERE email = %s and departure_date >= CURRENT_DATE()'
        cursor.execute(query, (email))
        current_flights = cursor.fetchall()

        for each in current_flights: # check if departure is a day or more. Do not give option to cancel if false
            today = date.today()
            if((each['departure_date'] - today).days < 1):
                each['cancel'] = False
            else:
                each['cancel'] = True
                
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
            each['arrival_date'] = str(each['arrival_date'])
            each['arrival_time'] = str(each['arrival_time'])

        session['current_flights'] = current_flights
        print("current_flights: ", current_flights)
        cursor.close()
        return render_template('home_customer.html', previous_flights=previous_flights, current_flights = current_flights)
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
    query = 'SELECT username, password, first_name, airline_name FROM Airline_Staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    print(data)
    first_name = data['first_name']
    airline_name = data['airline_name']
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        session['first_name'] = first_name
        session['airline_name'] = airline_name
        cursor = conn.cursor()
        query = 'SELECT departure_airport, arrival_airport, airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, flight_status FROM Flight WHERE airline_name = %s AND departure_date < NOW()'
        cursor.execute(query, (airline_name))
        previous_flights = cursor.fetchall()
        for each in previous_flights:
            today = date.today()
            if((each['departure_date'] - today).days < 0):
                each['edit'] = False
            else:
                each['edit'] = True
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
            each['arrival_date'] = str(each['arrival_date'])
            each['arrival_time'] = str(each['arrival_time'])
        session['previous_flights'] = previous_flights
        cursor.close()
        """
        1. View flights: Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.

        """
        cursor = conn.cursor()
        query = 'SELECT departure_airport, arrival_airport, airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, flight_status FROM Flight WHERE  airline_name = %s AND departure_date >= NOW() AND departure_date <= DATE_ADD(NOW(), INTERVAL 30 DAY);'
        cursor.execute(query, (airline_name))
        current_flights = cursor.fetchall()

        for each in current_flights: # check if departure is a day or more. Do not give option to cancel if false
            today = date.today()
            if((each['departure_date'] - today).days < 0):
                each['edit'] = False
            else:
                each['edit'] = True
                
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
            each['arrival_date'] = str(each['arrival_date'])
            each['arrival_time'] = str(each['arrival_time'])
        session['current_flights'] = current_flights
        cursor.close()
        return render_template('home_staff.html', previous_flights=previous_flights, current_flights = current_flights)
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('staff_login.html', error=error)

#Authenticates the customer register
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
        return render_template('register.html', error = error) # Did you mean customer_register?
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

#Authenticates the register
@app.route('/registerStaffAuth', methods=['GET', 'POST'])
def registerStaffAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']  # STRAIGHT UP STORING PASSWORD. CHANGE LATER!!!!
    email = request.form['email']
    phone_number = request.form['phone_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Airline_Staff WHERE username = %s AND airline_name = %s'
    cursor.execute(query, (username, airline_name))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('staff_register.html', error = error)
    else:
        ins = """INSERT INTO Airline_Staff (username, password, first_name, last_name, date_of_birth, airline_name)VALUES
                (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
        ins = """INSERT INTO Airline_Staff_Email (username, email)VALUES
                (%s, %s)"""
        cursor.execute(ins, (username, email))
        ins = """INSERT INTO Work_For (airline_name, username)VALUES
                (%s, %s)"""
        cursor.execute(ins, (airline_name, username))
        if (phone_number != ""):
            ins = """INSERT INTO Airline_Staff_Phone_Number (username, phone_number)VALUES
                (%s, %s)"""
            cursor.execute(ins, (username, phone_number))

        conn.commit()
        cursor.close()
        return render_template('staff_login.html')

@app.route('/home_unlog')
def home_unlog():
    return render_template('home_unlog.html')

@app.route('/home_customer')
def home_customer():
    return render_template('home_customer.html')

@app.route('/home_staff')
def home_staff():
    return render_template('home_staff.html')

@app.route('/search_unlog', methods=['GET', 'POST'])
def search_unlog():
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    departure_date = request.form['departure_date']
    # return_date = request.form['return_date']
    data1 = search_flights(departure_airport, arrival_airport,departure_city,arrival_city, departure_date)
    if data1:
        for each in data1:
            print(each['flight_number'])
        return render_template('home_unlog.html', flights = data1)
    else:
        error = "No Flights Found"
        return render_template('home_unlog.html', error = error)

@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    email = session['email']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    departure_date = request.form['departure_date']
    return_date = request.form['return_date']

    data = search_flights(departure_airport, arrival_airport, departure_city, arrival_city, departure_date)
    # print(data)
    data_return = search_flights(arrival_airport, departure_airport, arrival_city, departure_city, return_date)
    for each in data:
        each['departure_date'] = str(each['departure_date'])
        each['departure_time'] = str(each['departure_time'])
        each['arrival_date'] = str(each['arrival_date'])
        each['arrival_time'] = str(each['arrival_time'])
        # json.dumps(each, indent=4, sort_keys=True, default=str())
    for each in data_return:
        each['departure_date'] = str(each['departure_date'])
        each['departure_time'] = str(each['departure_time'])
        each['arrival_date'] = str(each['arrival_date'])
        each['arrival_time'] = str(each['arrival_time'])
    print(data)
    session['searched_flights_1'] = data
    session['searched_flights_2'] = data_return
    if data:
        # for each in data:
        #     print(each['flight_number'])
        return render_template('home_customer.html', email = email, previous_flights = previous_flights, current_flights = current_flights, searched_flights_1 = data, searched_flights_2 = data_return)
    else:
        error = "Search Error"
        return render_template('home_customer.html', email = email, previous_flights = previous_flights, current_flights = current_flights, error = error)

@app.route('/search_staff', methods=['GET', 'POST'])
def search_staff():
    username = session['username']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    departure_date = request.form['departure_date']
    return_date = request.form['return_date']

    data = search_flights(departure_airport, arrival_airport, departure_city, arrival_city, departure_date)
    # print(data)
    data_return = search_flights(arrival_airport, departure_airport, arrival_city, departure_city, return_date)
    if data:
        for each in data: # check if departure is a day or more. Do not give option to cancel if false
            today = date.today()
            if((each['departure_date'] - today).days < 0):
                each['edit'] = False
            else:
                each['edit'] = True
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
            each['arrival_date'] = str(each['arrival_date'])
            each['arrival_time'] = str(each['arrival_time'])
        for each in data_return: # check if departure is a day or more. Do not give option to cancel if false
            today = date.today()
            if((each['departure_date'] - today).days < 0):
                each['edit'] = False
            else:
                each['edit'] = True
            each['departure_date'] = str(each['departure_date'])
            each['departure_time'] = str(each['departure_time'])
            each['arrival_date'] = str(each['arrival_date'])
            each['arrival_time'] = str(each['arrival_time'])
        return render_template('home_staff.html', username = username, previous_flights = previous_flights, current_flights = current_flights, searched_flights_1 = data, searched_flights_2 = data_return)
    else:
        error = "Search Error"
        return render_template('home_staff.html', username = username, previous_flights = previous_flights, current_flights = current_flights, error = error)

@app.route('/sum_spending', methods=['GET', 'POST'])
def sum_spending():
    email = session['email']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    query = 'SELECT sum(sold_price) FROM Ticket WHERE email = %s and DATEDIFF(purchase_date, CURDATE()) < 365 ;'
    cursor = conn.cursor();
    cursor.execute(query, email);
    data = cursor.fetchone();
    t_sum = data['sum(sold_price)']
    session['t_sum'] = t_sum
    cursor.close()

    return render_template('track_spending.html', email = email, t_sum = t_sum, current_flights = current_flights, previous_flights = previous_flights)

@app.route('/input_review', methods=['GET', 'POST'])
def input_review():
    email = request.form['email']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    airline_name = request.form['airline_name']
    stars = request.form['stars']
    comments = request.form['comments']
    td = date.today()
    d_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
    print("d_date", d_date, type(d_date))
    if td <= d_date:
        error = "Date is not in the past!"
        return render_template('review.html', error=error)
    else:
        cursor = conn.cursor();
        query = 'SELECT * FROM Flight NATURAL JOIN Ticket WHERE flight_number = %s and departure_date = %s and departure_time = %s and email = %s'
        cursor.execute(query, (flight_number, departure_date, departure_time,email))
        data = cursor.fetchone()
        cursor.close()
        if(data):
            cursor = conn.cursor();
            ins = """INSERT INTO Rates (email, flight_number, departure_date, departure_time, airline_name,
                            stars, comments) VALUES
                            (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(ins, (email, flight_number, departure_date, departure_time, airline_name, stars, comments))
            conn.commit()
            cursor.close()
            complete = "Complete!"
            return render_template('review.html', complete = complete)
        else:
            error = "Flight not found!"
            return render_template('review.html', error=error)

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    try:
        email = session['email']
        cursor = conn.cursor();
        delete_query = "DELETE FROM Customer WHERE email=%s;"
        cursor.execute(delete_query, email)
        conn.commit()
        cursor.close()
        return redirect('/home_unlog')
    except:
        return render_template('remove_account.html', error="There was a problem with deleting your account")

@app.route('/staff_delete_account', methods=['GET', 'POST'])
def staff_delete_account():
    try:
        username = session['username']
        cursor = conn.cursor();
        delete_query = "DELETE FROM Airline_Staff_Email WHERE username=%s;"
        cursor.execute(delete_query, username)
        delete_query = "DELETE FROM Airline_Staff_Phone_Number WHERE username=%s;"
        cursor.execute(delete_query, username)
        delete_query = "DELETE FROM Airline_Staff WHERE username=%s;"
        cursor.execute(delete_query, username)
        conn.commit()
        cursor.close()
        return redirect('/home_unlog')
    except:
        return render_template('remove_staff_account.html', error="There was a problem with deleting your account")

@app.route('/customer_back', methods=['GET','POST'])
def customer_back():
    first_name = session['first_name']
    email = session['email']
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_number, departure_date FROM Ticket NATURAL JOIN Flight WHERE email = %s and departure_date < CURRENT_DATE()'
    cursor.execute(query, (email))
    previous_flights = cursor.fetchall()
    session['previous_flights'] = previous_flights
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM Ticket NATURAL JOIN Flight WHERE email = %s and departure_date >= CURRENT_DATE()'
    cursor.execute(query, (email))
    current_flights = cursor.fetchall()
    for each in current_flights: # check if departure is a day or more. Do not give option to cancel if false
        today = date.today()
        if((each['departure_date'] - today).days < 1):
            each['cancel'] = False
        else:
            each['cancel'] = True
    session['current_flights'] = current_flights
    cursor.close()

    return render_template('home_customer.html', first_name = first_name, previous_flights=previous_flights, current_flights=current_flights)

@app.route('/staff_back', methods=['GET','POST'])
def staff_back():
    first_name = session['first_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    return render_template('home_staff.html', first_name = first_name, previous_flights=previous_flights, current_flights=current_flights)

@app.route('/date_spending', methods =['GET', 'POST'])
def date_spending():
    email = session['email']
    t_sum = session['t_sum']
    cursor = conn.cursor();
    date1 = request.form['date1']
    date2 = request.form['date2']
    query = 'SELECT ticket_ID, airline_name, flight_number, purchase_date, sold_price from Flight NATURAL JOIN Ticket WHERE purchase_date > %s and purchase_date < %s and email = %s'
    cursor.execute(query, (date1, date2, email))
    data = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor();
    query = 'SELECT sum(sold_price) from Flight NATURAL JOIN Ticket WHERE purchase_date > %s and purchase_date < %s and email = %s'
    cursor.execute(query, (date1, date2, email))
    sum_res = cursor.fetchone()
    sum = sum_res['sum(sold_price)']
    return render_template('track_spending.html', date_spending = data, sum = sum, t_sum = t_sum)

@app.route('/buy_ticket', methods =['GET', 'POST'])
def buy_ticket():
    # print(session)
    # get form VALUES
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    departure_airport = request.form['departure_airport']
    arrival_date = request.form['arrival_date']
    arrival_time = request.form['arrival_time']
    arrival_airport = request.form['arrival_airport']
    card_type = request.form['card_type']
    card_number = request.form['card_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    expiration_date = request.form['expiration_date']
    security_code = request.form['security_code']
    email = session['email']
    # generate new ticket ID
    ticket_ID = random.randrange(100000,999999)


    # check if credit card is in credit card. if not add to credit card
    cursor = conn.cursor();
    credit_query = 'SELECT * FROM Card WHERE card_number = %s AND email = %s AND expiration_date = %s AND card_type = %s'
    cursor.execute(credit_query, (card_number, email, expiration_date, card_type))
    card_data = cursor.fetchall()
    cursor.close()

    if not card_data: # card_data is empty
        cursor = conn.cursor()
        insert_query = """INSERT INTO Card (card_number, email, expiration_date, first_name, last_name, card_type)
                        VALUES (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(insert_query, (card_number, email, expiration_date, first_name, last_name, card_type))
        conn.commit()
        cursor.close()

    # find number of tickets on flight
    try:
        cursor = conn.cursor();
        ticket_sum_query = 'SELECT COUNT(ticket_ID) FROM Ticket WHERE flight_number = %s and departure_date = %s and departure_time = %s;'
        cursor.execute(ticket_sum_query, (flight_number, departure_date, departure_time))
        ticket_count_data = cursor.fetchone()
        ticket_count = ticket_count_data['COUNT(ticket_ID)']
        cursor.close()

    # find flight capacity
        cursor = conn.cursor();
        flight_query = 'SELECT * FROM Airplane inner join Flight on Airplane.ID = Flight.airplane_id WHERE flight_number = %s and departure_date = %s and departure_time = %s and departure_airport = %s and arrival_airport = %s;'
        # print(flight_query%(flight_number, departure_date, departure_time, departure_airport, arrival_airport) )
        cursor.execute(flight_query, (flight_number, departure_date, departure_time, departure_airport, arrival_airport))
        flight_data = cursor.fetchone()
        # print(flight_data)
        cursor.close()

    # calculate ticket price
        capacity = flight_data['number_of_seats']
        base_price = flight_data['base_price']
        if(ticket_count > (capacity*.6)):
            sold_price = base_price + (base_price * .25)
        else:
            sold_price = base_price

    # get purchase date and time
        today = date.today()
        purchase_date = today.strftime("%Y-%m-%d")
        now = datetime.now()
        purchase_time = now.strftime("%H:%M:%S")

    # add ticket to Ticket and purchased_buy
        print(ticket_ID, flight_data['airline_name'], flight_number, sold_price, purchase_date, purchase_time, email)

        cursor = conn.cursor();
        ticket_insert = """INSERT INTO Ticket(ticket_ID, airline_name, flight_number, sold_price, purchase_date, purchase_time, departure_date, departure_time, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
        cursor.execute(ticket_insert, (ticket_ID, flight_data['airline_name'], flight_number, sold_price, purchase_date, purchase_time, departure_date, departure_time, email))
        conn.commit()
        cursor.close()

        cursor = conn.cursor();
        purchase_insert = """INSERT INTO Purchased_With(ticket_ID, email, card_number, payment_date, payment_time)
                            VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(purchase_insert, (ticket_ID, email, card_number, purchase_date, purchase_time))
        conn.commit()
        cursor.close()

        return render_template('buy.html', price = sold_price, flight_number = flight_number)
    except:
        error = "There was an error processing your request"
        return render_template('buy.html', error =error)
@app.route('/cancel_flight', methods = ['GET', 'POST'])
def cancel_flight():
    ticket_ID = request.form['ticket_ID']
    flight_number = request.form['flight_number']
    email=session['email']
    cursor = conn.cursor();
    query = "SELECT * FROM Ticket WHERE email=%s AND ticket_ID = %s AND flight_number = %s;"
    cursor.execute(query, (email, ticket_ID, flight_number))
    data = cursor.fetchall()
    cursor.close()
    if(data):
        cursor = conn.cursor();
        deletion_query = "DELETE FROM Purchased_With WHERE email=%s AND ticket_ID = %s;"
        cursor.execute(deletion_query, (email, ticket_ID))
        conn.commit()
        cursor.close()

        cursor = conn.cursor();
        deletion_query = "DELETE FROM Ticket WHERE email=%s AND ticket_ID = %s AND flight_number = %s;"
        cursor.execute(deletion_query, (email, ticket_ID, flight_number))
        conn.commit()
        cursor.close()
        return render_template('cancel.html', success = "success")
    else:
        error = "Flight not found"
        return render_template('cancel.html', error = error)

@app.route('/see_flight_customers', methods = ['GET', 'POST'])
def see_flight_customers():
    username = session['username']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT first_name, last_name FROM Ticket NATURAL JOIN Customer WHERE airline_name = %s AND flight_number = %s AND departure_date = %s AND departure_time = %s'
    cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
    #stores the results in a variable
    data = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        print(data)
        return render_template('view_customers.html', username = username, previous_flights = previous_flights, current_flights = current_flights, customers = data)
    else:
        #If the previous query doesn't return data, then throw error
        error = "This flight does not exist or has no customers"
        return render_template('view_customers.html', error = error)

@app.route('/add_new_airplane', methods = ['GET', 'POST'])
def add_new_airplane():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    ID = request.form['ID']
    number_of_seats = request.form['number_of_seats']
    manufacturer = request.form['manufacturer']
    age = request.form['age']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT airline_name, username FROM Work_For WHERE airline_name = %s AND username = %s'
    cursor.execute(query, (airline_name, username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if (data):
        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT ID, number_of_seats, manufacturer, age FROM Airplane WHERE airline_name = %s AND ID = %s'
        cursor.execute(query, (airline_name, ID))
        #stores the results in a variable
        data1 = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if (data1):
            error = "This airplane already exists"
            return render_template('new_airplane.html', error = error)
        else:
            cursor = conn.cursor();
            ins = """INSERT INTO Airplane (airline_name, ID, number_of_seats, manufacturer, age) VALUES
                                (%s, %s, %s, %s, %s)"""
            cursor.execute(ins, (airline_name, ID, number_of_seats, manufacturer, age))
            conn.commit()
            cursor.close()
            return render_template('new_airplane.html', username = username, previous_flights = previous_flights, current_flights = current_flights, customers = data ,success = "Your new airplane has successfully been added!")
    else:
        error = "YOU ARE UNAUTHORIZED TO MAKE THIS ADDITION"
        return render_template('new_airplane.html', error = error)

@app.route('/add_new_airport', methods = ['GET', 'POST'])
def add_new_airport():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    name = request.form['airport_name']
    city = request.form['airport_city']
    country = request.form['country']
    airport_type = request.form['airport_type']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT airline_name, username FROM Work_For WHERE airline_name = %s AND username = %s'
    cursor.execute(query, (airline_name, username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if (data):
        cursor = conn.cursor();
        query = 'SELECT * FROM Airport WHERE name = %s AND city = %s AND country = %s'
        cursor.execute(query, (name, city, country))
        data1 = cursor.fetchone()
        cursor.close()
        error = None
        if (data1):
            error = "This airport already exists"
            return render_template('new_airport.html', error = error)
        else:
            cursor = conn.cursor();
            ins = """INSERT INTO Airport (name, city, country, airport_type) VALUES
                                (%s, %s, %s, %s)"""
            cursor.execute(ins, (name, city, country, airport_type))
            conn.commit()
            cursor.close()
            return render_template('new_airport.html', success = "Your new airport has successfully been added!")
    else:
        error = "YOU ARE UNAUTHORIZED TO MAKE THIS ADDITION"
        return render_template('new_airport.html', error = error)
    
@app.route('/create_new_flight', methods = ['GET', 'POST'])
def create_new_flight():
    username = session['username']
    airline_name = session['airline_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
    flight_number = request.form['flight_number']
    departure_airport = request.form['departure_airport']
    departure_city = request.form['departure_city']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    arrival_airport = request.form['arrival_airport']
    arrival_city = request.form['arrival_city']
    arrival_date = request.form['arrival_date']
    arrival_time = request.form['arrival_time']
    base_price = request.form['base_price']
    airplane_id = request.form['airplane_id']
    flight_status = request.form['flight_status']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT airline_name, username FROM Work_For WHERE airline_name = %s AND username = %s'
    cursor.execute(query, (airline_name, username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if (data):
        cursor = conn.cursor();
        query = 'SELECT airline_name, ID FROM Airplane WHERE airline_name = %s AND ID = %s'
        cursor.execute(query, (airline_name, airplane_id))
        data1 = cursor.fetchone()
        cursor.close()
        error = None
        if (data1):
            cursor = conn.cursor();
            query = 'SELECT name, city FROM Airport WHERE name = %s AND city = %s'
            cursor.execute(query, (departure_airport, departure_city))
            data2 = cursor.fetchone()
            cursor.close()
            error = None
            if (data2):
                cursor = conn.cursor();
                query = 'SELECT name, city FROM Airport WHERE name = %s AND city = %s'
                cursor.execute(query, (arrival_airport, arrival_city))
                data3 = cursor.fetchone()
                cursor.close()
                error = None
                if (data3):
                    cursor = conn.cursor();
                    ins = """INSERT INTO Flight (airline_name, flight_number, departure_airport, departure_city, departure_date, departure_time, arrival_airport, arrival_city, arrival_date, arrival_time, base_price, airplane_id, flight_status) VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(ins, (airline_name, flight_number, departure_airport, departure_city, departure_date, departure_time, arrival_airport, arrival_city, arrival_date, arrival_time, base_price, airplane_id, flight_status))
                    conn.commit()
                    cursor.close()
                    cursor = conn.cursor()
                    query = 'SELECT departure_airport, arrival_airport, airline_name, flight_number, departure_date, departure_time, arrival_date, arrival_time, flight_status FROM Flight WHERE  airline_name = %s AND departure_date >= NOW() AND departure_date <= DATE_ADD(NOW(), INTERVAL 30 DAY)'
                    cursor.execute(query, (airline_name))
                    current_flights = cursor.fetchall()
    
                    for each in current_flights:
                        each['edit'] = True
                    session['current_flights'] = current_flights
                    print(current_flights)
                    cursor.close()
                    return render_template('new_flight.html',  username = username, airline_name = airline_name, previous_flights = previous_flights, current_flights = current_flights ,success = "Your new flight has successfully been created!")
                else:
                    error = "The arrival airport or city does not exist"
                    return render_template('new_flight.html', error = error)
            else:
                error = "The departure airport or city does not exist"
                return render_template('new_flight.html', error = error)
        else:
            error = "The airplane does not exist"
            return render_template('new_flight.html', error = error)
        
    else:
        error = "YOU ARE UNAUTHORIZED TO MAKE THIS ADDITION"
        return render_template('new_flight.html', error = error)
    

@app.route('/edit_flight_status', methods = ['GET', 'POST'])
def edit_flight_status():
    username = session['username']
    previous_flights = session['previous_flights']
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    flight_status = request.form['flight_status']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT airline_name, flight_number, departure_date, departure_time FROM Flight WHERE airline_name = %s AND flight_number = %s AND departure_date = %s AND departure_time = %s'
    cursor.execute(query, (airline_name, flight_number, departure_date, departure_time))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data and (flight_status == "Delayed" or flight_status == "On-Time")):
        ins = """UPDATE Flight SET flight_status = %s WHERE airline_name = %s AND flight_number = %s AND departure_date = %s AND departure_time = %s"""
        cursor.execute(ins, (flight_status, airline_name, flight_number, departure_date, departure_time))
        conn.commit()
        cursor.close()
        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM Flight WHERE  airline_name = %s AND departure_date >= NOW() AND departure_date <= DATE_ADD(NOW(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline_name))
        current_flights = cursor.fetchall()
    
        for each in current_flights:
            each['edit'] = True
        session['current_flights'] = current_flights
        print(current_flights)
        cursor.close()
        return render_template('home_staff.html', username = username, previous_flights = previous_flights, current_flights = current_flights)
    elif(flight_status != "Delayed" or flight_status != "On-time"):
        error = "This is not a valid flight status"
        return render_template('change_flight_status.html', error = error)
    else:
        #If the previous query doesn't return data, then throw error
        error = "This flight does not exist"
        return render_template('change_flight_status.html', error = error)

@app.route('/logout')
def logout():
    session.pop('username')
    session.clear()
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
