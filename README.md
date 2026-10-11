# Bristol Community Events

Bristol Community Events is a full-stack web development project I created during my first year of BSc Computer Science at the University of the West of England (UWE Bristol) as part of the Web Development and Database module.

The idea behind this project was to create a website where people could explore community workshops in Bristol, register for an account, book events and manage their bookings.

I developed the frontend using HTML, CSS, and JavaScript while Python and Flask were used for the backend. I also used MySQL to store information about users, workshops, bookings and payments.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## Main Features

### User Features

- Register and log in to an account
- Browse available workshops
- View workshop details and prices
- Book workshops and select ticket quantities
- Receive advance booking discounts depending on the event date
- Apply a student discount
- Complete a simulated payment process
- View payment receipts
- Check booking history
- Cancel bookings with calculated cancellation charges and refund amounts
- Send messages through the contact form
- Update account passwords

### Admin Features

- Access an admin dashboard
- View registered users
- View booking records
- View contact messages
- View workshop information
- Add new workshops with images

## Workshops

The website includes different types of workshops, such as drawing, pottery, crochet, origami, candle making, wood carving, soap making, jewellery making, and embroidery.

Some workshops are free, while others require a booking payment.

## Database

I used MySQL to design a relational database with nine tables:

- ADMIN
- CATEGORY
- VENUE
- USERS
- EVENT
- BOOKING
- PAYMENT
- RECEIPT
- CONTACTMESSAGE

I used primary keys and foreign keys to connect related tables and organise the data.

The database structure and sample workshop information can be found in `Progress review 2.sql`.

## How to Run the Project

This project was developed locally using Flask and MySQL. It has not been deployed online.

To run the project locally:

1. Clone or download the repository.
2. Install Python and MySQL.
3. Install the required Python libraries:

   `pip install flask mysql-connector-python`

4. Open MySQL Workbench and run `Progress review 2.sql` to create the database and sample data.
5. Configure the database connection and Flask secret key using the environment variables listed in `.env.example`.
6. Set up local test accounts as needed.
7. Run the application using:

   `python app.py`

8. Open `http://127.0.0.1:5000` in your browser.

**Note:** Some database and demo-account setup adjustments may be needed when running the project from a fresh installation.

## What I Learned

Through this project, I gained practical experience in connecting frontend and backend development.

I learned how to use Flask to handle routes, forms, and user sessions, and how to connect a Python application to a MySQL database. I also gained experience writing SQL queries, designing related database tables and implementing booking, discount, and cancellation logic.

This project helped me understand how different parts of a web application work together.

## Future Improvements

There are several areas I would like to improve as I continue developing my software engineering skills:

- Improve password security and admin authentication
- Add better form validation and error handling
- Improve mobile responsiveness and accessibility
- Add automated testing
- Make the application easier to set up locally
- Deploy the website online

## Project Information

**University:** University of the West of England (UWE Bristol)

**Course:** BSc Computer Science

**Module:** Web Development and Database

**Academic Year:** First Year (2025–2026)

**Project Status:** Completed academic project, developed locally and not publicly deployed.