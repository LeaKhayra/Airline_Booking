Airline Ticket Reservation System
Overview
This is a command-line Airline Ticket Reservation System written in Python. It enables users to manage airline reservations by booking tickets, canceling reservations, viewing all reservations, and searching for reservations by passenger name. The system stores reservation data in a JSON file and includes validation for inputs such as passport numbers and seat availability.
Features

Book a Ticket: Create a new reservation with passenger details, including name, passport number, flight number, and seat selection.
Cancel a Reservation: Remove a reservation using its unique booking ID.
View All Reservations: Display all current reservations with details.
Search Reservations: Search for reservations by passenger name using a binary search algorithm.
Exit: Close the application.

Requirements

Python 3.x
Standard Python libraries: json, os, datetime, re

Installation

Ensure Python 3.x is installed on your system.
Save the airline.py file in your desired directory.
No additional dependencies are required.

Usage

Open a terminal or command prompt.
Navigate to the directory containing airline.py.
Run the script using:python airline.py


Follow the on-screen menu to interact with the system:
Select 1 to book a ticket (provide name, passport number, flight number, and seat).
Select 2 to cancel a reservation (provide booking ID).
Select 3 to view all reservations.
Select 4 to search for reservations by passenger name.
Select 5 to exit the system.



Data Storage

Reservations are stored in a JSON file named reservations.json in the same directory as the script.
The system loads existing reservations on startup and saves changes after each booking or cancellation.

Error Handling

Validates passport numbers (must be 9 alphanumeric characters).
Checks for valid flight numbers (predefined as FL101, FL102, FL103).
Ensures seat availability and validity (e.g., 1A to 10F).
Handles empty inputs, invalid choices, and EOF errors gracefully.

Author
Lea Khayra Daania
License
This project is open-source and available under the MIT License.
