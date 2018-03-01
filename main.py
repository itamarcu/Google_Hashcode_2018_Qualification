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


def solve():
    rides = []

    with open(input_file_name) as file:
        num_columns, num_rows, num_vehicles, num_rides, bonus, num_timesteps = map(int, file.readline().split(" "))
        for _ in range(num_rides):
            x1, y1, x2, y2, start, finish = map(int, file.readline().split(" "))
            rides.append(Ride(x1, y1, x2, y2, start, finish))

    print(f"solving: {input_file_name}")


solve()
