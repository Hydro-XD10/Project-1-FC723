from Utilities import Utilities_  #import renamed class from separate file


class SeatBookingSystem:
    def __init__(self):
        self.columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']  #define seat column labels including aisle
        self.total_rows = 80  #define total number of seat rows
        self.seat_map = self.initialize_seats()  #initialize the seat layout
        self.reference_gen = Utilities_()  #create reference generator instance
        self.seat_reference_map = {}  #map seat to booking reference
        self.reference_seat_map = {}  #map booking reference to seat
        self.customer_data = {}  #map booking reference to customer data
        
        

#==================================================================  Seat intialising  ==================================================================
    def initialize_seats(self):#initialize_seats creates the full seating layout with free, aisle, and storage seats
        seat_map = {}  #create a dictionary for all seats
        for row in range(1, self.total_rows + 1):  #loop through rows 1 to 80
            seat_map[row] = {}  #initialize dictionary for each row
            for col in self.columns:  #loop through columns
                if col == 'X':  #if column is aisle
                    seat_map[row][col] = 'X'  #mark as aisle
                elif (row in [77, 78]) and col in ['D', 'E', 'F']:  #check for storage seats
                    seat_map[row][col] = 'S'  #mark as storage
                else:
                    seat_map[row][col] = 'F'  #mark as free seat
        return seat_map  #return complete seat map
#==================================================================  End Seat intialising  ==================================================================





#==================================================================  show_booking_status  ==================================================================

    def show_booking_status(self):    #show_booking_status displays the current seat layout showing booked and available seats
        print("\nSeat Layout (F = Free, X = Aisle, S = Storage, R = Booked):\n")  #print layout legend
        header = "     " + "  ".join(self.columns)  #build header row
        print(header)  #print column headers
        print("    " + "---" * len(self.columns))  #print separator
        for row in range(1, self.total_rows + 1):  #loop through each row
            row_label = f"{row:>2} |"  #format row label
            row_display = "  ".join(
                'R' if self.seat_map[row][col] not in ['F', 'X', 'S'] else self.seat_map[row][col]
                for col in self.columns
            )  #build row display
            print(f"{row_label} {row_display}")  #print formatted row




#==================================================================  End show_booking_status  ==================================================================





#==================================================================  check_availability  ==================================================================


    def check_availability(self, seat):#check_availability checks if a specific seat is available, booked, or not bookable
        try:
            row = int(seat[:-1])  #extract row from seat input
            col = seat[-1].upper()  #extract column from seat input
            if col == 'X':  #cannot book aisle
                print("Invalid seat. 'X' is an aisle.")  #notify user
                return
            status = self.seat_map[row][col]  #get seat status
            if status == 'F':  #seat is free
                print(f"Seat {seat} is available.")  #notify user
            elif status in ['X', 'S']:  #seat is not bookable
                print(f"Seat {seat} is not available for booking (marked as '{status}').")  #notify user
            else:
                print(f"Seat {seat} is already booked with reference: {status}")  #seat is booked
        except:
            print("Invalid input. Use format like 10A.")  #invalid format



#================================================================== End check_availability  ==================================================================




#==================================================================  book_seat  ==================================================================



    def book_seat(self, seat):#book_seat allows the user to book a seat and enter passenger details
        try:
            row = int(seat[:-1])  #extract row from seat
            col = seat[-1].upper()  #extract column from seat
            if col == 'X':  #prevent aisle booking
                print("Cannot book an aisle.")  #notify user
                return
            if self.seat_map[row][col] == 'F':  #check if seat is free
                first = input("Enter passenger first name: ")  #get first name
                last = input("Enter passenger last name: ")  #get last name
                passport = input("Enter passport number: ")  #get passport number
                ref = self.reference_gen.generate_reference()  #generate booking reference
                seat_code = f"{row}{col}"  #create seat code
                self.seat_map[row][col] = ref  #update seat map
                self.seat_reference_map[seat_code] = ref  #map seat to reference
                self.reference_seat_map[ref] = seat_code  #map reference to seat
                self.customer_data[ref] = {  #store passenger info
                    "first_name": first,
                    "last_name": last,
                    "passport": passport,
                    "seat": seat_code
                }
                print(f"Seat {seat_code} booked successfully.")  #confirmation
                print(f"Booking reference: {ref}")  #show reference
            else:
                print(f"Seat {seat} is not available for booking.")  #seat is booked
        except:
            print("Invalid seat input. Example: 5C")  #invalid input



#==================================================================  End book_seat  ==================================================================






#==================================================================  free_seat  ==================================================================

    def free_seat(self, seat):    #free_seat frees a booked seat and removes all related passenger data

        try:
            row = int(seat[:-1])  #extract row
            col = seat[-1].upper()  #extract column
            if col == 'X':  #prevent freeing aisle
                print("Cannot free an aisle.")  #notify user
                return
            seat_code = f"{row}{col}"  #build seat code
            ref = self.seat_reference_map.get(seat_code)  #get booking reference
            if ref:  #if reference found
                self.reference_gen.used_references.discard(ref)  #remove from used
                self.seat_map[row][col] = 'F'  #mark as free
                del self.seat_reference_map[seat_code]  #remove seat map entry
                del self.reference_seat_map[ref]  #remove reference map entry
                self.customer_data.pop(ref, None)  #remove customer info
                print(f"Seat {seat_code} has been freed.")  #confirmation
            else:
                print(f"Seat {seat_code} is not currently booked.")  #not found
        except:
            print("Invalid input. Use seat like 3A.")  #invalid input
            
#==================================================================  End free_seat  ==================================================================

            
            
            
#==================================================================  group_booking  ==================================================================

    def group_booking(self): #books multiple adjacent seats for a group and records passenger details
        try:
            num = int(input("How many seats would you like to book together? (2-4):"))  #get number of seats
            if num < 2 or num > 4:  #check if group size is valid
                print("Group booking allowed for 2 to 4 seats only.")  #notify user
                return
            for row in range(1, self.total_rows + 1):  #loop through each row
                free = []  #create list of free seats
                for col in self.columns:  #loop through each column
                    if col == 'X':  #reset on aisle
                        free = []
                        continue # skip this column (aisle), move to next seat in the same row
                    if self.seat_map[row][col] == 'F':  #check if seat is free
                        free.append((row, col))  #add seat to free list
                        if len(free) == num:  #if enough seats found
                            booked = []  #create list for booked seats
                            for r, c in free:  #loop through selected seats
                                print(f"\nBooking for seat {r}{c}:")  #prompt passenger input
                                first = input("Enter passenger first name:")  #get first name
                                last = input("Enter passenger last name:")  #get last name
                                passport = input("Enter passport number:")  #get passport number
                                ref = self.reference_gen.generate_reference()  #generate booking reference
                                seat_code = f"{r}{c}"  #generate seat code
                                self.seat_map[r][c] = ref  #assign reference to seat
                                self.seat_reference_map[seat_code] = ref  #map seat to reference
                                self.reference_seat_map[ref] = seat_code  #map reference to seat
                                self.customer_data[ref] = {  #save passenger info
                                    "first_name": first,
                                    "last_name": last,
                                    "passport": passport,
                                    "seat": seat_code
                                }
                                booked.append((seat_code, ref))  #save booking info
                            print("\nGroup booking successful!")  #confirm booking
                            for seat_code, ref in booked:  #print seat and reference
                                print(f"Seat {seat_code} → Reference: {ref}")
                            return
                    else:
                        free = []  #reset list if seat not free
            print("Sorry, no adjacent seats available for your group.")  #notify user
        except ValueError:
            print("Please enter a valid number.")  #handle input error


#==================================================================  End group_booking  ==================================================================



#==================================================================  lookup_reference_or_seat  ==================================================================

    def lookup_reference_or_seat(self): #finds and shows booking details using either seat or reference
        print("\n--- Booking Lookup ---")  #print lookup menu
        print("1. Find booking details by seat number (e.g. 12A)")  #option 1
        print("2. Find booking details by booking reference")  #option 2
        choice = input("Choose option (1 or 2):")  #get user input
        if choice == '1':  #lookup by seat
            seat = input("Enter seat number (e.g. 12A):").upper()  #get seat input
            ref = self.seat_reference_map.get(seat)  #get reference
            if ref:  #if reference exists
                data = self.customer_data.get(ref, {})  #get passenger info
                print(f"\nSeat: {seat}")  #print seat
                print(f"Booking reference: {ref}")  #print reference
                print(f"Passenger: {data.get('first_name')} {data.get('last_name')}")  #print name
                print(f"Passport: {data.get('passport')}")  #print passport
            else:
                print("No booking found for this seat.")  #not found
        elif choice == '2':  #lookup by reference
            ref = input("Enter booking reference (8 characters):").upper()  #get reference input
            seat = self.reference_seat_map.get(ref)  #get seat from reference
            data = self.customer_data.get(ref)  #get passenger data
            if seat and data:  #if found
                print(f"\nBooking reference: {ref}")  #print reference
                print(f"Seat: {seat}")  #print seat
                print(f"Passenger: {data['first_name']} {data['last_name']}")  #print name
                print(f"Passport: {data['passport']}")  #print passport
            else:
                print("No booking found for this reference.")  #not found
        else:
            print("Invalid choice.")  #invalid option



#==================================================================  End lookup_reference_or_seat  ==================================================================


#==================================================================  run ==============================================================================================

    def run(self):#displays the main menu and handles user interaction with the system
        while True:
            print("\n--- Apache Airlines Seat Booking System ---")  #print menu
            print("1. Check availability of seat")  #option 1
            print("2. Book a seat")  #option 2
            print("3. Free a seat")  #option 3
            print("4. Show booking status")  #option 4
            print("5. Exit")  #option 5
            print("6. Group seat booking (2-4 seats together)")  #option 6
            print("7. Lookup booking reference or seat")  #option 7
            choice = input("Select an option (1-7):")  #get user input
            if choice == '1':
                seat = input("Enter seat to check (e.g. 1A):")  #get seat input
                self.check_availability(seat)  #run availability check
            elif choice == '2':
                seat = input("Enter seat to book (e.g. 2B):")  #get seat input
                self.book_seat(seat)  #run booking function
            elif choice == '3':
                seat = input("Enter seat to free (e.g. 2B):")  #get seat input
                self.free_seat(seat)  #run free seat function
            elif choice == '4':
                self.show_booking_status()  #display seat layout
            elif choice == '5':
                print("Goodbye!")  #exit message
                break  #exit loop
            elif choice == '6':
                self.group_booking()  #run group booking
            elif choice == '7':
                self.lookup_reference_or_seat()  #run lookup function
            else:
                print("Invalid choice. Try 1 to 7.")  #handle invalid input

#================================================================== End run ==============================================================================================





system = SeatBookingSystem()  #create instance of booking system
system.run()  #start the system
