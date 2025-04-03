class SeatBookingSystem:
    def __init__(self):
        self.columns = ['A', 'B', 'C', 'X', 'D', 'E', 'F']  # Aisle between C and D
        self.total_rows = 80
        self.seat_map = self.initialize_seats()

    def initialize_seats(self):
        seat_map = {}
        for row in range(1, self.total_rows + 1):
            seat_map[row] = {}
            for col in self.columns:
                if col == 'X':
                    seat_map[row][col] = 'X'  # Aisle
                elif (row in [77, 78]) and col in ['D', 'E', 'F']:
                    seat_map[row][col] = 'S'  # Storage
                else:
                    seat_map[row][col] = 'F'  # Free
        return seat_map

    def show_booking_status(self):
        print("\nSeat Layout (R = Booked, F = Free, X = Aisle, S = Storage):\n")
        header = "     " + "  ".join(self.columns)
        print(header)
        print("    " + "---" * len(self.columns))

        for row in range(1, self.total_rows + 1):
            row_label = f"{row:>2} |"
            row_display = "  ".join(self.seat_map[row][col] for col in self.columns)
            print(f"{row_label} {row_display}")

    def check_availability(self, seat):
        try:
            row = int(seat[:-1])
            col = seat[-1].upper()
            if col == 'X':
                print("Invalid seat. 'X' is an aisle.")
                return
            status = self.seat_map[row][col]
            if status == 'F':
                print(f"Seat {seat} is available.")
            elif status == 'R':
                print(f"Seat {seat} is already booked.")
            else:
                print(f"Seat {seat} is not available for booking (marked as '{status}').")
        except:
            print("Invalid input. Use format like 10A.")

    def book_seat(self, seat):
        try:
            row = int(seat[:-1])
            col = seat[-1].upper()
            if col == 'X':
                print("Cannot book an aisle.")
                return
            if self.seat_map[row][col] == 'F':
                self.seat_map[row][col] = 'R'
                print(f"Seat {seat} has been successfully booked.")
            else:
                print(f"Seat {seat} is not available for booking.")
        except:
            print("Invalid seat input. Example: 5C")

    def free_seat(self, seat):
        try:
            row = int(seat[:-1])
            col = seat[-1].upper()
            if col == 'X':
                print("Cannot free an aisle.")
                return
            if self.seat_map[row][col] == 'R':
                self.seat_map[row][col] = 'F'
                print(f"Seat {seat} has been freed.")
            else:
                print(f"Seat {seat} is not currently booked.")
        except:
            print("Invalid input. Use seat like 3A.")

    def group_booking(self):
        try:
            num_seats = int(input("How many seats would you like to book together? (2-4): "))
            if num_seats < 2 or num_seats > 4:
                print("Group booking allowed for 2 to 4 seats only.")
                return

            for row in range(1, self.total_rows + 1):
                free_seats = []
                for i in range(len(self.columns)):
                    if self.columns[i] == 'X':
                        free_seats = []  # reset sequence across aisle
                        continue

                    seat_status = self.seat_map[row][self.columns[i]]
                    if seat_status == 'F':
                        free_seats.append((row, self.columns[i]))
                        if len(free_seats) == num_seats:
                            for r, c in free_seats:
                                self.seat_map[r][c] = 'R'
                            booked = [f"{r}{c}" for r, c in free_seats]
                            print(f"Group booking successful! Seats booked: {', '.join(booked)}")
                            return
                    else:
                        free_seats = []  # reset if seat is not free

            print("Sorry, no adjacent seats available for your group.")
        except ValueError:
            print("Please enter a valid number.")

    def run(self):
        while True:
            print("\n--- Apache Airlines Seat Booking System ---")
            print("1. Check availability of seat")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking status")
            print("5. Exit")
            print("6. Group seat booking (2-4 seats together)")

            choice = input("Select an option (1-6): ")

            if choice == '1':
                seat = input("Enter seat to check (e.g. 1A): ")
                self.check_availability(seat)
            elif choice == '2':
                seat = input("Enter seat to book (e.g. 2B): ")
                self.book_seat(seat)
            elif choice == '3':
                seat = input("Enter seat to free (e.g. 2B): ")
                self.free_seat(seat)
            elif choice == '4':
                self.show_booking_status()
            elif choice == '5':
                print("Goodbye!")
                break
            elif choice == '6':
                self.group_booking()
            else:
                print("Invalid choice. Try 1 to 6.")


# Run the program
system = SeatBookingSystem()
system.run()
