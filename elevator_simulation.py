import time
from datetime import datetime, timedelta
from tkinter import Tk, Canvas, TclError

class Person:
    population = 0

    def __init__(self, entry_time, start_floor, target_floor):
        self.animation = None
        self.id = Person.population
        Person.population += 1
        self.entry_time = entry_time
        self.start_floor = start_floor
        self.target_floor = target_floor
        self.direction = 1 if self.start_floor < self.target_floor else -1
        self.finished = False
        self.in_elevator = False
        self.wait_time = 0
        self.elevator_spot = False

    def arrived(self, floor):
        return self.target_floor == floor

    def waiting(self):
        return not self.in_elevator and not self.finished

def single_simulation(algorithm, function_dict, data, floors, max_elevator_capacity=6, animate=True, animation_speed=1):
    def close_window():
        nonlocal animate
        animate = False
        tk.destroy()  # Safely close the window

    def process_logic(func, timestamp, elev_pop, floor_population, floors, elevator_floor, t_floor):
        return func(timestamp, elev_pop, floor_population, floors, elevator_floor, t_floor)

    
    start_lifts = time.perf_counter()
    
    if len(data) < 2 or floors < 2:
        return 0
    
    floor_height = round(600 / floors)
    total_population = []
    elevator_population = []
    floor_population = [0] * (floors + 1)
    elevator_floor = 1
    target_floor = 1
    t_floor = 1
    elevator_direction = 0.5
    elev_pop = []
    start_time = data['Timestamp'].min()
    end_time = data['Timestamp'].max()
    current_time = start_time

    if animate:
        arrivals_population = [0] * (floors + 1)
        newly_arrived = [[None]] * (floors + 1)
        elevator_animation = [0] * max_elevator_capacity
        tk = Tk()
        tk.attributes("-fullscreen", False)
        tk.protocol("WM_DELETE_WINDOW", close_window)  # Handle the window close event
        canvas = Canvas(tk, width=1000, height=1000)
        tk.title(f'Elevator - {algorithm} algorithm')
        canvas.pack()

        def enter_lift(animation, x, y):
            total_move_time = 0.15  # Total time to move the animation in seconds
            steps = 50  # Number of steps to divide the move into
            for j in range(steps):
                canvas.move(animation, x / steps, y / steps)
                tk.update()
                time.sleep(total_move_time / steps)

        def exit_lift(animation, x, y):
            total_move_time = 0.15  # Total time to move the animation in seconds
            steps = 50  # Number of steps to divide the move into
            for j in range(steps):
                canvas.move(animation, x / steps, y / steps)
                tk.update()
                time.sleep(total_move_time / steps)

        # Draw the background rectangle
        canvas.create_rectangle(50, 300 + ((floors - 1) * floor_height), 650, 300 - floor_height, fill='lightgrey')  # Adjust the dimensions as needed

        # Create building outline & lift
        canvas.create_oval(85, 70, 95, 80, fill='black')
        canvas.create_oval(85, 90, 95, 100, fill='white')
        canvas.create_oval(85, 110, 95, 120, fill='green')
        waiting_label = canvas.create_text(100, 75, text='Waiting', anchor='w')
        inside_label = canvas.create_text(100, 95, text='Inside elevator', anchor='w')
        delivered_label = canvas.create_text(100, 115, text='Arrived', anchor='w')
        canvas.create_text(625, 275, text="UPLIFT", font=("Cambria", 24, "bold"), angle=270)
        canvas.create_text(625, 425, text="CHALLENGE", font=("Cambria", 24), angle=270)

        
        clock_label = canvas.create_text(100, 135, text='Time: ' + current_time.strftime('%H:%M:%S'), anchor='w')
        for k in range(1, floors+2):
            canvas.create_line(50, 300 + (floors - k) * floor_height, 600, 300 + (floors - k) * floor_height)
            if k > 1:
                canvas.create_line(200, 300 + (floors - k) * floor_height, 200, 300 + floor_height + (floors - k) * floor_height)
                canvas.create_line(400, 300 + (floors - k) * floor_height, 400, 300 + floor_height + (floors - k) * floor_height)
            if k <= floors:
                canvas.create_text(5, 275 + (floors - k) * floor_height, text='Floor ' + str(k), anchor='w')
        
        elevator = canvas.create_rectangle(203, 300 + floor_height * (floors - 1 - elevator_floor), 397, 300 + floor_height * (floors - elevator_floor), fill='black')
        tk.update()

    while any(not person.finished for person in total_population) or current_time <= end_time:
        if animate and not tk.winfo_exists():
            animate = False  # Disable animation if the window is closed
        new_people = data[data['Timestamp'] == current_time]

        for _, row in new_people.iterrows():
            timestamp = row['Timestamp']
            start_floor = row['Entry_Floor']
            target_floor = row['Exit_Floor']
            
            if start_floor < 0 or start_floor > floors or target_floor < 0 or target_floor > floors:
                print(f"Invalid floor values: start_floor={start_floor}, target_floor={target_floor}")
                continue
            person = Person(current_time, start_floor, target_floor)
            s_f = person.start_floor
            
            if animate:
                offset = floor_population[s_f] * 13
                person.animation = canvas.create_oval(185 - offset, 290 + (floors - s_f) * floor_height, 195 - offset, 300 + (floors - s_f) * floor_height, fill='black')
                tk.update()
            
            floor_population[s_f] += 1
            total_population.append(person)

        for person in total_population:
            person.wait_time += 1 if not person.finished else 0

            if person.in_elevator and person.arrived(elevator_floor):
                person.in_elevator = False
                person.finished = True
                elevator_population.remove(person)
                elevator_buttons[person.target_floor] = False
                elev_pop = [i for i in range(len(elevator_buttons)) if elevator_buttons[i]]

                if animate:
                    # Position dots that are arriving
                    MAX_DOTS_PER_ROW = 15
                    DOT_SPACING = 13  # Horizontal spacing between dots
                    VERTICAL_SPACING = 13  # Vertical spacing between rows
                    elevator_animation[person.elevator_spot] = False
                    canvas.itemconfig(person.animation, fill='green')
                    elevator_floor = int(elevator_floor)
                    arrivals_population[elevator_floor] += 1
                    
                    # Calculate the number of dots already in the current row
                    current_row_dots = arrivals_population[elevator_floor] - 1  # Subtract one for the current one being added
                    row_number = current_row_dots // MAX_DOTS_PER_ROW  # Determine which row we're currently on
                    dot_index_in_row = current_row_dots % MAX_DOTS_PER_ROW  # Which dot position in this row
            
                    # Calculate x and y positions for the dot
                    x_position = 390 + ((dot_index_in_row + 1) * DOT_SPACING)
                    y_position = VERTICAL_SPACING * (person.elevator_spot % 2) + (row_number * -15)
            
                    exit_lift(person.animation, x_position - canvas.coords(person.animation)[0], y_position)
                    canvas.itemconfig(delivered_label, text='Arrived - ' + str((len(total_population) - sum(floor_population) - len(elevator_population))))
                    canvas.itemconfig(inside_label, text='Inside elevator - ' + str(len(elevator_population)))
                    canvas.itemconfig(waiting_label, text='Waiting - ' + str(sum(floor_population)))

        
        selected_function = function_dict.get(algorithm)
        t_floor = process_logic(selected_function, current_time, elev_pop, floor_population, floors, elevator_floor, t_floor)
        if t_floor > elevator_floor: elevator_direction = 0.5
        elif t_floor < elevator_floor: elevator_direction = -0.5
        else: elevator_direction = 0

            

        for person in reversed(total_population):
            if person.waiting() and person.start_floor == elevator_floor and len(elevator_population) < max_elevator_capacity:

                elevator_population.append(person)
                person.in_elevator = True
                floor_population[int(elevator_floor)] -= 1
                elevator_buttons = [False] * (floors + 1)
                for person in elevator_population:
                    elevator_buttons[person.target_floor] = True
                elev_pop = [i for i in range(len(elevator_buttons)) if elevator_buttons[i]]
                
                if animate:
                    for spot in range(len(elevator_animation)):
                        if not elevator_animation[spot]:
                            elevator_animation[spot] = True
                            person.elevator_spot = spot
                            enter_lift(person.animation, (275 + (spot % 3) * 13) - canvas.coords(person.animation)[0], -13 * (spot % 2))
                            break
                    canvas.itemconfig(person.animation, fill='white')
                    canvas.itemconfig(inside_label, text='Inside elevator - ' + str(len(elevator_population)))
                    canvas.itemconfig(waiting_label, text='Waiting - ' + str(sum(floor_population)))

        if animate:
            current_time += timedelta(seconds=1)
            if not tk.winfo_exists():
                break  # Exit the loop if the window has been destroyed
            canvas.itemconfig(clock_label, text='Time: ' + current_time.strftime('%H:%M:%S'))
            for i in range(floor_height):
                if not animate:  # Stop updating if animation is turned off
                    break
                tk.update()
                time.sleep(animation_speed / floor_height)
                try:
                    canvas.move(elevator, 0, -elevator_direction)
                    for person in elevator_population:
                        canvas.move(person.animation, 0, -elevator_direction)
                except TclError:
                    break  # Exit the loop if there's an error moving the canvas
        else:
            current_time += timedelta(seconds=1)
    
        elevator_floor += elevator_direction

    wait_times = [person.wait_time for person in total_population if person.finished]
    average_wait_time = sum(wait_times) / len(wait_times) if len(wait_times) > 0 else 1
    
    # Convert the timestamp string to a datetime object
    # Define 8:00 AM on the same day
    eight_am = datetime(current_time.year, current_time.month, current_time.day, 8, 0, 0)
    
    # Calculate the difference
    time_difference = current_time - eight_am
    
    # Extract hours, minutes, and seconds from the time difference
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if animate and tk.winfo_exists():
        canvas.create_text(200, 900, text=f"Total time elapsed: {hours} hours, {minutes} minutes, and {seconds} seconds", font=("Cambria", 12))
        canvas.create_text(200, 915, text=f'Shortest wait time: {min(wait_times)}s', font=("Cambria", 12))
        canvas.create_text(200, 930, text=f'Longest wait time: {max(wait_times)}s', font=("Cambria", 12))
        canvas.create_text(200, 945, text="Average wait time: " + str(round(average_wait_time, 2)), font=("Cambria", 12))
        tk.mainloop()
        
    return wait_times

        
