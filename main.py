file_names = ["a_example", "b_should_be_easy", "c_no_hurry", "d_metropolis", "e_high_bonus"]

class Ride:
    def __init__(self, x1, y1, x2, y2, start, finish):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.start = start
        self.finish = finish

class Car:
    def __init__(self,time, x, y):
        self.time = time
        self.x = x
        self.y = y
        self.rides = []
    def add_ride(self, ride):
        self.rides.append(ride)

def setup():
    rides = []

    with open(input_file_name) as file:
        num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps = map(int, file.readline().split(" "))
        for _ in range(num_rides):
            x1, y1, x2, y2, start, finish = map(int, file.readline().split(" "))
            rides.append(Ride(x1, y1, x2, y2, start, finish))

    print(f"solving: {input_file_name}")

    classic_solve(rides, num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps)

def dist(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def calc_score(ride, car):
    #note - this alg can cause wait for million seconds for best ride
    ride_length = dist(ride.x1, ride.x2, ride.y1, ride.y2)
    dist_to_start = dist(car.x, ride.x1, car.y, ride.y1)
    wait_time = 0
    if(car.time +dist_to_start < ride.start):
        wait_time = ride.start - (car.time + dist_to_start)
    if(car.time + dist_to_start + ride_length > ride.finish):
        return (0,0)

    return ( ride_length, (ride_length + dist_to_start + wait_time))

#Each car adds the next best ride and win!
def classic_solve(rides, num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps):
    cars = [Car(0,0,0) for i in range(num_vehicles)]
    for turn in range(num_timesteps):
        for car in cars:
            curr_max = 0
            curr_max_index = -1
            curr_total_time = 0
            if(car.time != turn):
                continue
            for i in range(len(rides)):
                ride = rides[i]
                score = calc_score(ride, car)
                if(score[0] > curr_max):
                    curr_max_index = i
                    curr_max = score[0]
                    curr_total_time = score[1]
            if(curr_max_index == -1):
                continue
            ride = rides[i]
            del rides[i]
            car.time += curr_total_time
            car.add_ride(i)
            car.x = ride.x2
            car.y = ride.y2

    with open (output_file_name, mode="w") as file:
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
input_file_name = file_names[1] + ".in"
output_file_name = file_names[1]+".out"
setup()