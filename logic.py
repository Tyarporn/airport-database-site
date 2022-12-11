#ATRS Python Flask File
#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import date, datetime

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
                       db='air_ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
"""

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

        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_number, departure_date FROM Ticket NATURAL JOIN Flight WHERE email = %s and departure_date < CURRENT_DATE()'
        cursor.execute(query, (email))
        previous_flights = cursor.fetchall()
        session['previous_flights'] = previous_flights
        print(previous_flights)
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
        print(current_flights)
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
        query = 'SELECT airline_name, flight_number, departure_date FROM Ticket NATURAL JOIN Flight WHERE departure_date < CURRENT_DATE()'
        cursor.execute(query)
        previous_flights = cursor.fetchall()
        session['previous_flights'] = previous_flights
        print(previous_flights)
        cursor.close()
        """
        1. View flights: Defaults will be showing all the future flights operated by the airline he/she works for the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see all the customers of a particular flight.

        """
        cursor = conn.cursor()
        query = 'SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM Ticket NATURAL JOIN Flight WHERE  airline_name = %s AND departure_date >= CURRENT_DATE() AND  departure_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline_name))
        current_flights = cursor.fetchall()

        for each in current_flights: # check if departure is a day or more. Do not give option to cancel if false
            each['edit'] = True
        session['current_flights'] = current_flights
        print(current_flights)
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
    return_date = request.form['return_date']
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
        # for each in data:
        #     print(each['flight_number'])
        return render_template('home_staff.html', username = username, previous_flights = previous_flights, current_flights = current_flights, searched_flights_1 = data)
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
        delete_query = "DELETE FROM Airline_Staff WHERE username=%s;"
        cursor.execute(delete_query, username)
        conn.commit()
        cursor.close()
        return redirect('/home_unlog')
    except:
        return render_template('remove_account.html', error="There was a problem with deleting your account")

@app.route('/customer_back', methods=['GET','POST'])
def customer_back():
    first_name = session['first_name']
    previous_flights = session['previous_flights']
    current_flights = session['current_flights']
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

@app.route('/cancel_flight', methods = ['GET', 'POST'])
def cancel_flight():
    ticket_ID = request.form['ticket_ID']
    flight_number = request.form['flight_number']
    deletion = '' # to do tomorrow!
    return render_template('cancel.html')

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
        query = 'SELECT airline_name, flight_number, departure_date, arrival_date, flight_status FROM Ticket NATURAL JOIN Flight WHERE  airline_name = %s AND departure_date >= CURRENT_DATE() AND  departure_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)'
        cursor.execute(query, (airline_name))
        current_flights = cursor.fetchall()

        for each in current_flights: # check if departure is a day or more. Do not give option to cancel if false
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
        error = "This flight does not exit"
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
