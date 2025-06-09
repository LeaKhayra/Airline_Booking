import json
import os
from datetime import datetime
import re

# Passenger class to store individual passenger details
class Passenger:
    def __init__(self, name, passport, flight_no, seat):
        # Initialize passenger attributes
        self.name = name  # Passenger's full name
        self.passport = passport  # Passenger's passport number
        self.flight_no = flight_no  # Flight number for the booking
        self.seat = seat  # Assigned seat (e.g., 1A)
        self.booking_id = self.generate_booking_id()  # Unique booking ID

    def generate_booking_id(self):
        # Generate a unique booking ID based on the current timestamp
        return f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def to_dict(self):
        # Convert passenger details to a dictionary for JSON serialization
        return {
            "booking_id": self.booking_id,
            "name": self.name,
            "passport": self.passport,
            "flight_no": self.flight_no,
            "seat": self.seat
        }

# AirlineSystem class to manage reservations and flight details
class AirlineSystem:
    def __init__(self, data_file="reservations.json"):
        # Initialize the system with a JSON file for storing reservations
        self.data_file = data_file  # File to store reservation data
        self.reservations = []  # List to store all passenger reservations
        self.available_flights = ["FL101", "FL102", "FL103"]  # List of valid flight numbers
        self.seats = [f"{row}{letter}" for row in range(1, 11) for letter in "ABCDEF"]  # Generate seat numbers (1A to 10F)
        self.load_reservations()  # Load existing reservations from file

    def load_reservations(self):
        # Load reservations from the JSON file if it exists
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)  # Read JSON data
                    # Convert JSON data to Passenger objects
                    self.reservations = [Passenger(d["name"], d["passport"], d["flight_no"], d["seat"]) 
                                       for d in data]
                except json.JSONDecodeError:
                    self.reservations = []  # Initialize empty list if JSON is invalid

    def save_reservations(self):
        # Save all reservations to the JSON file
        with open(self.data_file, 'w') as f:
            json.dump([r.to_dict() for r in self.reservations], f, indent=4)  # Write reservations as JSON

    def validate_passport(self, passport):
        # Validate passport number format (9 alphanumeric characters)
        return bool(re.match(r'^[A-Z0-9]{9}$', passport))

    def book_ticket(self, name, passport, flight_no, seat):
        # Book a ticket for a passenger
        if not name.strip():
            raise ValueError("Name cannot be empty")  # Ensure name is not empty
        if not self.validate_passport(passport):
            raise ValueError("Invalid passport number (9 alphanumeric characters required)")  # Validate passport
        if flight_no not in self.available_flights:
            raise ValueError("Invalid flight number")  # Check if flight number is valid
        if seat not in self.seats:
            raise ValueError("Invalid seat")  # Check if seat is valid
        if any(r.seat == seat and r.flight_no == flight_no for r in self.reservations):
            raise ValueError("Seat already booked")  # Check for seat availability
        
        passenger = Passenger(name, passport, flight_no, seat)  # Create new passenger object
        self.reservations.append(passenger)  # Add passenger to reservations
        self.save_reservations()  # Save updated reservations
        return passenger.booking_id  # Return the booking ID

    def cancel_reservation(self, booking_id):
        # Cancel a reservation by booking ID
        initial_length = len(self.reservations)  # Store initial number of reservations
        self.reservations = [r for r in self.reservations if r.booking_id != booking_id]  # Remove matching reservation
        if len(self.reservations) < initial_length:
            self.save_reservations()  # Save changes if a reservation was removed
            return True  # Indicate successful cancellation
        return False  # Indicate no matching reservation found

    def view_reservations(self):
        # Return a list of all reservations as dictionaries
        return [r.to_dict() for r in self.reservations]

    def search_reservations(self, query, reservations=None):
        # Perform a binary search for reservations by name
        if reservations is None:
            reservations = self.reservations  # Use all reservations if none specified
        
        if not query:
            return reservations  # Return all reservations if query is empty
        
        if len(reservations) == 0:
            return []  # Return empty list if no reservations
        
        # Sort reservations by name (case-insensitive) for binary search
        reservations.sort(key=lambda x: x.name.lower())
        mid = len(reservations) // 2  # Find middle index
        mid_name = reservations[mid].name.lower()  # Get middle name (case-insensitive)
        query = query.lower()  # Convert query to lowercase

        if mid_name == query:
            return [reservations[mid]]  # Exact match found
        elif len(reservations) == 1:
            return [reservations[0]] if query in mid_name else []  # Partial match for single reservation
        
        if query < mid_name:
            return self.search_reservations(query, reservations[:mid])  # Search left half
        else:
            return self.search_reservations(query, reservations[mid:])  # Search right half

def display_menu():
    # Display the main menu options
    print("\nAirline Ticket Reservation System")
    print("1. Book a Ticket")
    print("2. Cancel a Reservation")
    print("3. View All Reservations")
    print("4. Search Reservations")
    print("5. Exit")

def main():
    # Main function to run the airline reservation system
    system = AirlineSystem()  # Initialize the airline system
    while True:
        display_menu()  # Show the menu
        try:
            choice = input("Enter your choice (1-5): ").strip()  # Get user input
            if choice == "1":
                # Book a new ticket
                print("\nAvailable flights:", ", ".join(system.available_flights))  # Show available flights
                name = input("Enter name: ").strip()  # Get passenger name
                passport = input("Enter passport number (9 alphanumeric characters): ").strip()  # Get passport number
                flight_no = input("Enter flight number: ").strip()  # Get flight number
                print("Available seats:", ", ".join(system.seats[:10]), "...")  # Show sample seats
                seat = input("Enter seat (e.g., 1A): ").strip()  # Get seat choice
                try:
                    booking_id = system.book_ticket(name, passport, flight_no, seat)  # Attempt to book ticket
                    print(f"Booking confirmed! Booking ID: {booking_id}")  # Confirm booking
                except ValueError as e:
                    print(f"Error: {e}")  # Handle booking errors

            elif choice == "2":
                # Cancel an existing reservation
                booking_id = input("Enter booking ID to cancel: ").strip()  # Get booking ID
                if system.cancel_reservation(booking_id):
                    print("Reservation cancelled successfully")  # Confirm cancellation
                else:
                    print("Booking ID not found")  # Indicate no matching reservation

            elif choice == "3":
                # View all reservations
                reservations = system.view_reservations()  # Get all reservations
                if not reservations:
                    print("No reservations found")  # Handle empty reservations
                else:
                    print("\nAll Reservations:")
                    for res in reservations:
                        # Display each reservation's details
                        print(f"ID: {res['booking_id']}, Name: {res['name']}, Passport: {res['passport']}, "
                              f"Flight: {res['flight_no']}, Seat: {res['seat']}")

            elif choice == "4":
                # Search for reservations by name
                query = input("Enter name to search: ").strip()  # Get search query
                results = system.search_reservations(query)  # Perform search
                if not results:
                    print("No matching reservations found")  # Handle no results
                else:
                    print("\nSearch Results:")
                    for res in results:
                        # Display each matching reservation
                        print(f"ID: {res.booking_id}, Name: {res.name}, Passport: {res.passport}, "
                              f"Flight: {res.flight_no}, Seat: {res.seat}")

            elif choice == "5":
                # Exit the program
                print("Exiting system. Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-5.")  # Handle invalid menu choice

        except EOFError:
            print("\nEOF detected. Exiting system.")  # Handle EOF input
            break
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle unexpected errors

if __name__ == "__main__":
    main()  # Run the main program