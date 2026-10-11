CREATE DATABASE IF NOT EXISTS bristol_community_events;
USE bristol_community_events;

CREATE TABLE ADMIN (
AdminID INT NOT NULL,
FirstName VARCHAR(50) NOT NULL,
LastName VARCHAR(50) NOT NULL,
Email VARCHAR(100) NOT NULL,
Password VARCHAR(255) NOT NULL,
Role VARCHAR(30) NOT NULL,
CreatedDate DATETIME,
PRIMARY KEY (AdminID)
);

CREATE TABLE CATEGORY (
CategoryID INT NOT NULL,
CategoryName VARCHAR(100) NOT NULL,
Description VARCHAR(255),
PRIMARY KEY (CategoryID)
);

CREATE TABLE VENUE (
VenueID INT NOT NULL,
VenueName VARCHAR(100) NOT NULL,
Address VARCHAR(150),
City VARCHAR(50),
Postcode VARCHAR(20),
Capacity INT NOT NULL,
ContactEmail VARCHAR(100),
ContactPhone VARCHAR(20),
PRIMARY KEY (VenueID)
);

CREATE TABLE USERS (
UserID INT NOT NULL,
FirstName VARCHAR(50) NOT NULL,
LastName VARCHAR(50) NOT NULL,
Email VARCHAR(100) NOT NULL,
Password VARCHAR(255) NOT NULL,
DateRegistered DATETIME,
PRIMARY KEY (UserID)
);

CREATE TABLE EVENT (
EventID INT NOT NULL,
AdminID INT NOT NULL,
CategoryID INT NULL,
VenueID INT NULL,
EventName VARCHAR(100) NOT NULL,
Description TEXT,
EventDate DATE NOT NULL,
EventTime TIME NOT NULL,
Price DECIMAL(10,2) NOT NULL,
Capacity INT NOT NULL,
ImageURL VARCHAR(255),
CreatedDate DATETIME,
PRIMARY KEY (EventID),
FOREIGN KEY (AdminID)
	REFERENCES ADMIN(AdminID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
FOREIGN KEY (CategoryID)
	REFERENCES CATEGORY(CategoryID)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
FOREIGN KEY (VenueID)
	REFERENCES VENUE(VenueID)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE BOOKING (
BookingID INT NOT NULL,
UserID INT NOT NULL,
EventID INT NOT NULL,
BookingDate DATE,
TicketQuantity INT NOT NULL,
BookingStatus VARCHAR(30),
AdvanceDiscountPercent DECIMAL(5,2),
StudentDiscountPercent DECIMAL(5,2),
DiscountAmount DECIMAL(10,2),
FinalAmount DECIMAL(10,2),
CancellationDate DATE NULL,
CancellationCharge DECIMAL(10,2),
RefundAmount DECIMAL(10,2),
PRIMARY KEY (BookingID),
FOREIGN KEY (UserID)
	REFERENCES USERS(UserID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
FOREIGN KEY (EventID)
	REFERENCES EVENT(EventID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE PAYMENT (
PaymentID INT NOT NULL,
BookingID INT NOT NULL,
AmountPaid DECIMAL(10,2) NOT NULL,
PaymentDate DATE,
PaymentMethod VARCHAR(50),
PaymentStatus VARCHAR(30),
TranscationReference VARCHAR(100),
PRIMARY KEY (PaymentID),
UNIQUE (BookingID),
FOREIGN KEY (BookingID)
	REFERENCES BOOKING(BookingID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE RECEIPT (
ReceiptID INT NOT NULL,
BookingID INT NOT NULL,
PaymentID INT NOT NULL,
IssueDate DATE,
Subtotal DECIMAL(10,2),
AdvanceDiscountAmount DECIMAL(10,2),
StudentDiscountAmount DECIMAL(10,2),
FinalTotal DECIMAL(10,2),
PRIMARY KEY (ReceiptID),
UNIQUE (BookingID),
UNIQUE (PaymentID),
FOREIGN KEY (BookingID)
	REFERENCES BOOKING(BookingID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
FOREIGN KEY (PaymentID)
	REFERENCES PAYMENT(PaymentID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE CONTACTMESSAGE (
MessageID INT NOT NULL,
UserID INT NULL,
FirstName VARCHAR(50),
LastName VARCHAR(50),
Country VARCHAR(50),
Message TEXT NOT NULL,
MessageDate DATE,
PRIMARY KEY (MessageID),
FOREIGN KEY (UserID)
	REFERENCES USERS(UserID)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

INSERT INTO ADMIN
(AdminID, FirstName, LastName, Email, Password, Role, CreatedDate)
VALUES
(1, 'BCE', 'Admin', 'admin@bce.com', 'admin123', 'Admin', NOW());

INSERT INTO CATEGORY
(CategoryID, CategoryName, Description)
VALUES
(1, 'Art', 'Art and design workshops'),
(2, 'Craft', 'Craft and handmade workshops');

INSERT INTO VENUE
(VenueID, VenueName, Address, City, Postcode, Capacity, ContactEmail, ContactPhone)
VALUES
(1, 'UWE Student Union (Frenchay Campus)', 'Coldharbour Ln, Frenchay Campus', 'Bristol', 'BS16 1QY', 100, 'su@uwe.ac.uk', '01173280000');
SELECT * FROM VENUE;

INSERT INTO EVENT
(EventID, AdminID, CategoryID, VenueID, EventName, Description, EventDate, EventTime, Price, Capacity, ImageURL, CreatedDate)
VALUES
(1, 1, 2, 1, 'Origami Workshop', 'Learn creative paper folding techniques in a fun hands-on session.', '2026-09-20', '10:00:00', 15.00, 50, 'origami_workshop.jpg', NOW()),
(2, 1, 1, 1, 'Drawing Workshop', 'Join us for a fun and creative drawing workshop where you can explore your artistic side.', '2026-09-21', '11:00:00', 20.00, 50, 'drawing_workshop.jpg', NOW()),
(3, 1, 2, 1, 'Candle Craft Workshop', 'Discover the art of candle making in this hands-on workshop where you can create your own candles.', '2026-09-22', '12:00:00', 25.00, 50, 'candle_workshop.jpg', NOW()),
(4, 1, 2, 1, 'Wood Carving Workshop', 'Discover the art of wood carving in this hands-on workshop where you can create your own unique pieces.', '2026-09-23', '13:00:00', 30.00, 50, 'woodcarving_workshop.jpg', NOW()),
(5, 1, 2, 1, 'Soap Making Workshop', 'Learn the art of soap making in this hands-on workshop where you can create your own unique soaps.', '2026-09-24', '14:00:00', 30.00, 50, 'soap_workshop.jpg', NOW()),
(6, 1, 2, 1, 'Pottery Workshop', 'Join us for a hands-on pottery workshop where you can create your own ceramic masterpiece.', '2026-09-25', '15:00:00', 35.00, 50, 'pottery_workshop.jpg', NOW()),
(7, 1, 2, 1, 'Jewellery Workshop', 'Discover the art of jewellery making in this hands-on workshop where you can create your own unique pieces.', '2026-09-26', '16:00:00', 40.00, 50, 'jewellery_workshop.jpg', NOW()),
(8, 1, 2, 1, 'Crochet Workshop', 'Learn the art of crochet in this relaxing workshop where you can create your own cozy items.', '2026-09-27', '17:00:00', 0.00, 50, 'crochet_workshop.jpg', NOW()),
(9, 1, 2, 1, 'Embroidery Workshop', 'Explore embroidery techniques and create your own beautiful stitched designs.', '2026-09-28', '18:00:00', 0.00, 50, 'embroidery_workshop.jpg', NOW());


SHOW TABLES;

SELECT * FROM USERS;
SELECT * FROM CONTACTMESSAGE;
SELECT * FROM BOOKING;
SELECT * FROM EVENT;
SELECT * FROM PAYMENT;
SELECT * FROM CONTACTMESSAGE;
