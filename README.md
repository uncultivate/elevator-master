# Elevator Simulation

This project simulates the behavior of an elevator system in a building with multiple floors. The simulation is based on two different algorithms for elevator movement and provides the option to visualize the elevator's operations.

<img src="lift.jpg" alt="anime-lift" width="500"/>

## Features

- **Random Data Generation:** Generates random timestamped data to simulate elevator usage over a period.
- **Biased Floor Selection:** Allows for biased floor selection based on time of day, simulating typical elevator usage patterns.
- **Simulation Algorithms:**
  - **Efficient Algorithm:** Prioritizes passengers already in the elevator and optimizes for the closest destination.
  - **Baseline Algorithm:** Follows a simple up-and-down approach, reversing direction only at the top or bottom floors.
- **Animation:** Visualize the elevator's movements and passenger behavior using a GUI.

## Prerequisites

- Python 3.x
- Libraries: `random`, `pandas`, `datetime`, `tkinter`, `time`

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/elevator-simulation.git
cd elevator-simulation
```

## Usage

### Generating Random Data
The script generates random timestamped data representing people entering and exiting the elevator at different floors:

### Running the Simulation
To run the simulation, use the single_simulation function:

```python
single_simulation(algorithm="efficient", data=df, floors=10, max_elevator_capacity=6, animate=True, animation_speed=1)
```

* algorithm: Choose between "efficient" and "baseline", or create your own function with elevator logic
* data: Pass the generated data in a DataFrame.
* floors: Number of floors in the building.
* max_elevator_capacity: Maximum number of people the elevator can carry.
* animate: Set to True to enable the animation.
* animation_speed: Control the speed of the animation.

## Viewing the Results
The results, including total time elapsed, shortest wait time, longest wait time, and average wait time, will be displayed in the console. If the animation is enabled, these results will also appear in the GUI.
<img src="elevator_graphic.png" alt="screenshot" width="500"/>
