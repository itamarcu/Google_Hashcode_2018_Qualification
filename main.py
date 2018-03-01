from typing import List, Tuple

import heapq

file_names = ["a_example", "b_should_be_easy", "c_no_hurry", "d_metropolis", "e_high_bonus"]


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Ride:
    def __init__(self, x1, y1, x2, y2, start, finish):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.start = start
        self.finish = finish
        self.completed = False

    def time_to_complete(self):
        return distance(self.x1, self.y1, self.x2, self.y2)

    def score(self):
        return distance(self.x1, self.y1, self.x2, self.y2)


class Car:
    def __init__(self, time, x, y):
        self.time = time
        self.x = x
        self.y = y
        self.rides = []

    def add_ride(self, ride):
        self.rides.append(ride)


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
    rides = list(enumerate(rides))
    rides.sort(key=lambda tup: tup[1].start)
    satisfied_rides = set()
    score = 0
    bonus_count = 0
    output: List[Tuple[int, List[int]]] = []

    for car_index in range(num_vehicles):
        x, y = 0, 0
        step = 0
        rides_taken = []
        for ride_i, ride in rides:
            if ride_i in satisfied_rides: #TEMP TEMP TEMP
                continue
            if ride.finish <= step:
                continue
            time_to_reach = distance(ride.x1, ride.y1, x, y)
            time_to_complete = ride.time_to_complete()
            if step + time_to_reach + time_to_complete > ride.finish:
                continue
            if step + time_to_reach + time_to_complete > num_timesteps:
                continue
            # take this ride!
            score += ride.score()
            reach_step = step + time_to_reach
            if reach_step <= ride.start:
                reach_step = ride.start
                bonus_count += 1
                score += bonus  # yay
            step = reach_step + time_to_complete
            x, y = ride.x2, ride.y2
            satisfied_rides.add(ride_i)
            rides_taken.append(ride_i)
            # print(f"{step}: took {ride_i}. went from {ride.x1}, {ride.y1} to {x}, {y}"
            #       f" within {ride.start}, {ride.finish}, score is {score}")
            # no need to break and re-loop since we're taking the first available ride every time
        output.append((len(rides_taken), rides_taken))

    print(f"{len(satisfied_rides)}\{num_rides} rides completed, bonus count: {bonus_count}")
    return output, score


def solve_each_trip_2(rides: List[Ride], num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps):
    """continuously add first possible ride, until the end of time"""
    rides = list(enumerate(rides))
    # rides.sort(key=lambda tup: tup[1].start)
    satisfied_rides = set()
    score = 0
    bonus_count = 0
    output: List[Tuple[int, List[int]]] = []

    for car_index in range(num_vehicles):
        x, y = 0, 0
        step = 0
        rides_taken = []
        looking_for_bonus = True
        has_a_ride = False
        while has_a_ride or looking_for_bonus:
            for ride_i, ride in rides:
                if ride_i in satisfied_rides: #TEMP TEMP TEMP
                    continue
                if ride.finish <= step:
                    continue
                time_to_reach = distance(ride.x1, ride.y1, x, y)
                time_to_complete = ride.time_to_complete()
                if step + time_to_reach + time_to_complete > ride.finish:
                    continue
                if step + time_to_reach + time_to_complete > num_timesteps:
                    continue
                # can take this ride!
                reach_step = step + time_to_reach
                if looking_for_bonus and reach_step <= ride.start:
                    reach_step = ride.start
                    score += bonus  # yay
                    bonus_count += 1
                elif looking_for_bonus:
                    has_a_ride = True
                    continue
                score += ride.score()
                step = reach_step + time_to_complete
                x, y = ride.x2, ride.y2
                satisfied_rides.add(ride_i)
                rides_taken.append(ride_i)
                looking_for_bonus = True
                has_a_ride = False
                # print(f"{step}: took {ride_i}. went from {ride.x1}, {ride.y1} to {x}, {y}"
                #       f" within {ride.start}, {ride.finish}, score is {score}")
                break
            else:
                looking_for_bonus = False
        output.append((len(rides_taken), rides_taken))
    print(f"{len(satisfied_rides)}\{num_rides} rides completed, bonus count: {bonus_count}")
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

    with open(output_file_name, mode="w") as file:
        for amount_of_rides, the_rides in output:
            file.write(f"{amount_of_rides} ")
            file.write(f"{' '.join(str(x) for x in the_rides)}\n")

    # classic_solve(rides, num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps)


def dist(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)
def calc_score(ride, car, bonus, num_timesteps):
    #note - this alg can cause wait for million seconds for best ride
    if(ride.completed):
        return (0,0)


def calc_score(ride, car):
    # note - this alg can cause wait for million seconds for best ride
    ride_length = dist(ride.x1, ride.x2, ride.y1, ride.y2)
    dist_to_start = dist(car.x, ride.x1, car.y, ride.y1)
    wait_time = 0
    if (car.time + dist_to_start < ride.start):
        wait_time = ride.start - (car.time + dist_to_start)

    if (car.time + wait_time + dist_to_start + ride_length > ride.finish):
        return (0, 0)
    if(car.time + wait_time + dist_to_start + ride_length > num_timesteps):
        return (0,0)

    score = ride_length
    if (car.time+dist_to_start<= ride.start):
        score = (score+ bonus)
    if (car.time + dist_to_start + ride_length > ride.finish):
        return (0, 0)

    return ( score, (ride_length + dist_to_start + wait_time))


# Each car adds the next best ride and win!
def classic_solve(rides, num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps):
    cars = [Car(0, 0, 0) for i in range(num_vehicles)]
  #  cars_heap = []
    cars = [Car(0,0,0) for i in range(num_vehicles)]
 #   for car in cars:
  #      heapq.heappush(cars_heap, (0,car))
    for turn in range(num_timesteps):
        for car in cars:
            curr_max = 0
            curr_max_index = -1
            curr_total_time = 0
            if (car.time != turn):
                continue
            for i in range(len(rides)):
                ride = rides[i]
                score = calc_score(ride, car)
                if (score[0] > curr_max):
                score = calc_score(ride, car, bonus, num_timesteps)
                if(score[0] > curr_max):
                    curr_max_index = i
                    curr_max = score[0]
                    curr_total_time = score[1]
            if (curr_max_index == -1):
                continue
            ride = rides[curr_max_index]
            car.time += curr_total_time
            car.add_ride(curr_max_index)
            car.x = ride.x2
            car.y = ride.y2
            rides[curr_max_index].completed = True

    with open(output_file_name, mode="w") as file:
        for car in cars:
            file.write(f"{len(car.rides)}")
            for ride in car.rides:
                file.write(f" {ride}")
            file.write('\n')


"""
for i in range(len(file_names)):
    input_file_name = file_names[i] + ".in"
    output_file_name = file_names[i]+".out"
    setup()
"""

file_index = 3
input_file_name = file_names[file_index] + ".in"
output_file_name = file_names[file_index] + ".out"
setup()
