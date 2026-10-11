from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import date, datetime 
import dbfunc

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT UserID, FirstName, LastName, Email, DateRegistered FROM USERS")
    users = cursor.fetchall()

    cursor.execute("""
        SELECT b.BookingID, b.UserID, e.EventName, b.BookingDate, b.BookingStatus, b.FinalAmount
        FROM BOOKING b
        JOIN EVENT e ON b.EventID = e.EventID
        ORDER BY b.BookingDate ASC
    """)
    bookings = cursor.fetchall()

    cursor.execute("""
        SELECT MessageID, FirstName, LastName, Email, Country, Message, MessageDate
        FROM CONTACTMESSAGE
        ORDER BY MessageID ASC
    """)
    messages = cursor.fetchall()

    cursor.execute("SELECT EventID, EventName, EventDate, EventTime, Price, Capacity FROM EVENT ORDER BY EventID DESC")
    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('BCE_admin.html', users=users, bookings=bookings, messages=messages, events=events)

@app.route('/admin_update_password')
def admin_update_password():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template('BCE_admin_update_password.html')

@app.route('/submit_admin_update_password', methods=['POST'])
def submit_admin_update_password():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT Password FROM USERS WHERE UserID = %s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user or user['Password'] != current_password:
        cursor.close()
        conn.close()
        return "Current password is incorrect"

    if new_password != confirm_password:
        cursor.close()
        conn.close()
        return "New passwords do not match"

    cursor.execute(
        "UPDATE USERS SET Password = %s WHERE UserID = %s",
        (new_password, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('BCE_admin_update_password_success.html')

@app.route('/manage_users')
def manage_users():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT UserID, FirstName, LastName, Email, DateRegistered FROM USERS")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('BCE_manage_users.html', users=users)

@app.route('/manage_bookings')
def manage_bookings():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.BookingID, b.UserID, e.EventName, b.BookingDate, b.BookingStatus, b.FinalAmount
        FROM BOOKING b
        JOIN EVENT e ON b.EventID = e.EventID
        ORDER BY b.BookingDate ASC
    """)
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('BCE_manage_bookings.html', bookings=bookings)

@app.route('/manage_messages')
def manage_messages():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT MessageID, FirstName, LastName, Email, Country, Message, MessageDate
        FROM CONTACTMESSAGE
        ORDER BY MessageID ASC
    """)
    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('BCE_manage_messages.html', messages=messages)

@app.route('/add_event', methods=['POST'])
def add_event():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    event_name = request.form['event_name']
    description = request.form['description']
    price = request.form['price']
    event_date = request.form['event_date']
    event_time = request.form['event_time']
    capacity = request.form['capacity']
    image_file = request.files['event_image']
    filename = secure_filename(image_file.filename)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_url = filename

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT MAX(EventID) AS max_id FROM EVENT")
    result = cursor.fetchone()
    new_event_id = 1 if result['max_id'] is None else result['max_id'] + 1

    cursor.execute("""
        INSERT INTO EVENT 
        (EventID, AdminID, CategoryID, VenueID, EventName, Description, EventDate, EventTime, Price, Capacity, ImageURL)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            new_event_id,
            1,
            2,
            1,
            event_name,
            description,
            event_date,
            event_time,
            price,
            capacity,
            image_url
        ))
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin', added='yes'))

@app.route('/') 
def home():
    user_id = session.get('user_id')
    has_paid_booking = False

    conn = dbfunc.getConnection()

    if conn:
        print("Connected inside Flask")

        if user_id:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT b.BookingID
                FROM BOOKING b
                JOIN EVENT e ON b.EventID = e.EventID
                WHERE b.UserID = %s
                AND b.BookingStatus = %s
                AND e.Price > 0
                LIMIT 1
                """,
                (user_id, 'Confirmed')
            )
            paid_booking = cursor.fetchone()

            if paid_booking:
                has_paid_booking = True

            cursor.close()

        conn.close()

    return render_template('index.html', has_paid_booking=has_paid_booking)

@app.route('/about')
def about():
    return render_template('BCE_about.html')

@app.route('/events')
def events():
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary = True)

    cursor.execute("""
        SELECT EventID, EventName, Description, Price, ImageURL 
        FROM EVENT
        WHERE EventID > 9
        ORDER BY EventID DESC
    """)

    events = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('BCE_allEventDetail.html', events = events)

@app.route('/contact')
def contact():
    return render_template('BCE_contact.html')

@app.route('/login')
def login():
    return render_template('BCE_login.html')

@app.route('/register')
def register():
    return render_template('BCE_register.html')

@app.route('/submit_register', methods=['POST'])
def submit_register():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("SELECT MAX(UserID) AS max_id FROM USERS")
    result = cursor.fetchone()
    new_user_id = 1 if result['max_id'] is None else result['max_id'] + 1

    sql = """
    INSERT INTO USERS (UserID, FirstName, LastName, Email, Password, DateRegistered)
    VALUES (%s, %s, %s, %s, %s, NOW())
    """

    values = (new_user_id, firstname, lastname, email, password)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('BCE_register_success.html')

@app.route('/submit_login', methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM USERS WHERE Email = %s AND Password = %s"
    values =(email, password)
    cursor.execute(sql, values)

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['UserID']
        session['firstname'] = user['FirstName']
        session['email'] = user['Email']

        if user['Email'] == 'admin@gmail.com':
            session['is_admin'] = True
            return redirect(url_for('admin'))
        
        return render_template('BCE_login_success.html', firstname=user['FirstName'])
    else:
        return render_template('BCE_login_failed.html')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/update_password')
def update_password():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    return render_template('BCE_update_password.html')

@app.route('/submit_update_password', methods=['POST'])
def submit_update_password():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT Password FROM USERS WHERE UserID = %s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user or user['Password'] != current_password:
        cursor.close()
        conn.close()
        return "Current password is incorrect"
    
    if new_password != confirm_password:
        cursor.close()
        conn.close()
        return "New passwords do not match"
    
    cursor.execute(
        "UPDATE USERS SET Password = %s WHERE UserID = %s",
        (new_password, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('BCE_update_password_success.html')

@app.route('/booking/<int:event_id>')
def booking(event_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary = True)

    cursor.execute("SELECT EventID, EventName, Price, EventDate FROM EVENT WHERE EventID = %s", (event_id,))
    event = cursor.fetchone()

    if not event:
        cursor.close()
        conn.close()
        return redirect(url_for('events'))
    
    if float(event['Price']) == 0.00:
        cursor.execute(
            """
            SELECT b.BookingID
            FROM BOOKING b
            JOIN EVENT e ON b.EventID = e.EventID
            WHERE b.UserID = %s
            AND b.BookingStatus = %s
            AND e.Price > 0
            LIMIT 1
            """,
            (user_id, 'Confirmed')
        )
        paid_booking = cursor.fetchone()

        if not paid_booking:
            cursor.close()
            conn.close()
            return render_template('BCE_free_workshop_locked.html')
        
    cursor.close()
    conn.close()

    return render_template('BCE_booking.html', event = event)

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    event_id = request.form['event_id']
    ticket_quantity = int(request.form['ticket_quantity'])

    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)

    # Check if the user already booked this workshop
    cursor.execute(
        "SELECT BookingID FROM BOOKING WHERE UserID = %s AND EventID = %s AND BookingStatus IN (%s, %s) LIMIT 1",
        (user_id, int(event_id), 'Pending', 'Confirmed')
    )
    existing_booking = cursor.fetchone()

    if existing_booking:
        existing_booking_id = existing_booking['BookingID']

        cursor.close()
        conn.close()

        return redirect(url_for('payment', booking_id=existing_booking_id))
    
    # Get event price and event date
    cursor.execute("SELECT Price, EventDate FROM EVENT WHERE EventID = %s", (event_id,))
    event = cursor.fetchone()

    price = float(event['Price'])
    event_date = event['EventDate']
    base_amount = price * ticket_quantity

    # calculate advance booking discount
    days_in_advance = (event_date - date.today()).days
    
    advance_discount_percent = 0.00
    if 50 <= days_in_advance <= 60:
        advance_discount_percent = 20.00
    elif 35 <= days_in_advance < 50:
        advance_discount_percent = 15.00
    elif 25 <= days_in_advance < 35:
        advance_discount_percent = 10.00
    elif 15 <= days_in_advance < 25:
        advance_discount_percent = 5.00

    # Calculate student discount
    is_student = request.form.get('is_student')
    student_discount_percent = 10.00 if is_student == 'yes' else 0.00

    # Calculate final values
    advance_discount_amount = base_amount * (advance_discount_percent / 100)
    student_discount_amount = base_amount * (student_discount_percent / 100)
    discount_amount = advance_discount_amount + student_discount_amount
    final_amount = base_amount - discount_amount

    # Get New BookingID
    cursor.execute("SELECT MAX(BookingID) AS max_id FROM BOOKING")
    result = cursor.fetchone()
    new_booking_id = 1 if result['max_id'] is None else result['max_id'] + 1

    # Insert booking into database
    sql = """
    INSERT INTO BOOKING
    (BookingID, UserID, EventID, BookingDate, TicketQuantity, BookingStatus,
    AdvanceDiscountPercent, StudentDiscountPercent, DiscountAmount, FinalAmount,
    CancellationDate, CancellationCharge, RefundAmount)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        new_booking_id,
        user_id,
        int(event_id),
        date.today(),
        ticket_quantity,
        'Pending',
        advance_discount_percent,
        student_discount_percent,
        discount_amount,
        final_amount,
        None,
        0.00,
        0.00
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('payment', booking_id=new_booking_id))

@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT b.BookingID, b.FinalAmount, e.EventName
    FROM BOOKING b
    JOIN EVENT e ON b.EventID = e.EventID
    WHERE b.BookingID = %s AND b.UserID = %s
    """

    cursor.execute(sql, (booking_id, user_id))
    booking = cursor.fetchone()

    cursor.close()
    conn.close()

    if not booking:
        return redirect(url_for('my_bookings'))
    
    return render_template('BCE_payment.html', booking=booking)

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    booking_id = request.form['booking_id']
    payment_method = request.form['payment_method']

    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT BookingID, FinalAmount
        FROM BOOKING
        WHERE BookingID = %s AND UserID = %s
    """, (booking_id, user_id))

    booking = cursor.fetchone()

    if not booking:
        cursor.close()
        conn.close()
        return redirect(url_for('my_bookings'))
    
    cursor.execute("SELECT MAX(PaymentID) AS max_id FROM PAYMENT")
    result = cursor.fetchone()
    new_payment_id = 1 if result['max_id'] is None else result['max_id'] + 1

    transaction_reference = "TXN" + str(new_payment_id)

    cursor.execute("""
        INSERT INTO PAYMENT
        (PaymentID, BookingID, AmountPaid, PaymentDate, PaymentMethod, PaymentStatus, TranscationReference)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        new_payment_id,
        booking_id,
        booking['FinalAmount'],
        date.today(),
        payment_method,
        'Paid',
        transaction_reference
    ))

    cursor.execute("""
        UPDATE BOOKING
        SET BookingStatus = %s
        WHERE BookingID = %s
    """, ('Confirmed', booking_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('receipt', payment_id=new_payment_id))

@app.route('/receipt/<int:payment_id>')
def receipt(payment_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.PaymentID, p.AmountPaid, p.PaymentDate, p.PaymentMethod,
               p.PaymentStatus, p.TranscationReference,
               b.BookingID, e.EventName, e.EventDate
        FROM PAYMENT p
        JOIN BOOKING b ON p.BookingID = b.BookingID
        JOIN EVENT e ON b.EventID = e.EventID
        WHERE p.PaymentID = %s AND b.UserID = %s
    """, (payment_id, user_id))

    payment = cursor.fetchone()

    cursor.close()
    conn.close()

    if not payment:
        return redirect(url_for('my_bookings'))
    
    return render_template('BCE_receipt.html', payment=payment)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    country = request.form['country']
    subject = request.form['subject']

    conn = dbfunc.getConnection()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("SELECT MAX(MessageID) AS max_id FROM CONTACTMESSAGE")
    result = cursor.fetchone()
    new_message_id = 1 if result['max_id'] is None else result['max_id'] + 1

    sql = """
    INSERT INTO CONTACTMESSAGE
    (MessageID, UserID, FirstName, LastName, Email, Country, Message, MessageDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (new_message_id, None, firstname, lastname, email, country, subject, date.today())

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('BCE_contact_success.html')

@app.route('/my_bookings')
def my_bookings():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary = True)

    sql = """
    SELECT b.BookingID, b.BookingDate, b.BookingStatus, b.FinalAmount,
           b.CancellationCharge, b.RefundAmount, b.CancellationDate,
           e.EventName, e.EventDate
    FROM BOOKING b
    JOIN EVENT e ON b.EventID = e.EventID
    WHERE b.UserID = %s
    ORDER BY e.EventDate ASC
    """

    cursor.execute(sql, (user_id,))
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('BCE_my_bookings.html', bookings = bookings)

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('login'))
    
    conn = dbfunc.getConnection()

    if not conn:
        return "Database connection failed"
    
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT b.BookingID, b.FinalAmount, b.BookingStatus,
           e.EventName, e.EventDate
    FROM BOOKING b
    JOIN EVENT e ON b.EventID = e.EventID
    WHERE b.BookingID = %s AND b.UserID = %s
    """
    cursor.execute(sql, (booking_id, user_id))
    booking = cursor.fetchone()

    if not booking:
        cursor.close()
        conn.close()
        return redirect(url_for('my_bookings'))
    
    if booking['BookingStatus'] != 'Confirmed':
        cursor.close()
        conn.close()
        return redirect(url_for('my_bookings'))
    
    days_before_event = (booking['EventDate'] - date.today()).days

    if days_before_event >= 40:
        cancellation_charge_percent = 0.00
    elif 25 <= days_before_event < 40:
        cancellation_charge_percent = 40.00
    else:
        cancellation_charge_percent = 100.00

    final_amount = float(booking['FinalAmount'])
    cancellation_charge = final_amount * (cancellation_charge_percent / 100)
    refund_amount = final_amount - cancellation_charge

    update_sql = """
    UPDATE BOOKING
    SET BookingStatus = %s,
        CancellationDate = %s,
        CancellationCharge = %s,
        RefundAmount = %s
    WHERE BookingID = %s
    """

    cursor.execute(update_sql, (
        'Cancelled',
        date.today(),
        cancellation_charge,
        refund_amount,
        booking_id
    ))
    conn.commit()

    cursor.close()
    conn.close()

    return render_template(
        'BCE_cancel_success.html',
        booking=booking,
        cancellation_charge=cancellation_charge,
        refund_amount=refund_amount
    )

if __name__ == '__main__':
    app.run(debug=True)
