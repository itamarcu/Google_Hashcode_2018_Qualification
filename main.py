from typing import List, Tuple

file_names = ["a_example", "b_should_be_easy", "c_no_hurry", "d_metropolis", "e_high_bonus"]

input_file_name = file_names[1] + ".in"


class Ride:
    def __init__(self, x1, y1, x2, y2, start, finish):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.start = start
        self.finish = finish

    def time_to_complete(self):
        return self.x2 - self.x1 + self.y2 - self.y1

    def score(self):
        return self.x2 - self.x1 + self.y2 - self.y1


class Node:
    """Represents a point in space and time, and a list of already completed rides"""

    def __init__(self, x, y, step, already_completed_rides: List[int]):
        self.x = x
        self.y = y
        self.step = step
        self.already_completed_rides = already_completed_rides
        self.outs: List[Node] = []


def solve_each_trip(rides: List[Ride], num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps):
    # rides.sort(key=lambda ride: ride.start)
    # nodes = []
    # nodes.append(Node(0, 0, 0, []))
    # for i in range(num_rides):
    #     for j in range(num_rides):
    #         if i != j:
    #             ride_1 = rides[i]
    #             ride_2 = rides[j]
    #             if ride_1
    """just continuously add first possible ride, until the end of time"""
    rides.sort(key=lambda ride: ride.start)
    satisfied_rides = set()
    score = 0
    output: List[Tuple[int, List[int]]] = []

    for car_index in range(num_vehicles):
        x, y = 0, 0
        step = 0
        rides_taken = []
        for ride_i in range(0, num_rides):
            if ride_i in satisfied_rides:
                continue
            ride = rides[ride_i]
            if ride.start < step:
                continue
            if ride.finish < step:
                continue
            time_to_reach = ride.x1 - x + ride.y1 - y
            time_to_complete = ride.time_to_complete()
            if step + time_to_reach + time_to_reach > ride.finish:
                continue
            # take this ride!
            score += ride.score()
            reach_step = step + time_to_reach
            if reach_step <= ride.start:
                reach_step = ride.start
                score += bonus  # :)
            step = reach_step + time_to_complete
            x = ride.x2
            y = ride.y2
            curr_ride_i = ride_i
            satisfied_rides.add(ride_i)
            rides_taken.append(ride_i)
            # no need to break and re-loop since we're taking the first available ride every time
            if step > num_timesteps:
                break
        output.append((len(rides_taken), rides_taken))
    print(f"{len(satisfied_rides)}\{num_rides} rides completed")
    return output, score


def setup():
    rides = []

    with open(input_file_name) as file:
        num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps = map(int, file.readline().split(" "))
        for _ in range(num_rides):
            x1, y1, x2, y2, start, finish = map(int, file.readline().split(" "))
            rides.append(Ride(x1, y1, x2, y2, start, finish))

    print(f"solving: {input_file_name}")
    output, score = solve_each_trip(rides, num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps)
    print(f"SCORE: {score}")
    for tup in output:
        print(tup)



setup()
