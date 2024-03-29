import random

def generate_random_yashi_game(rows, cols, npoints):
    solvable = False
    n = 1

    while solvable == False:
        if npoints > rows*cols:
          raise ValueError("More points than possible nodes")
        # Create a list of points (excluding the origin)
        points = [(i, j) for i in range(rows) for j in range(cols)]

        # Shuffle the points randomly
        random.shuffle(points)

       # Take only the first 'npoints' points
        selected_points = points[:npoints]

        # Create the CSV string
        csv_string = "point,x,y\n"
        for idx, (x, y) in enumerate(selected_points):
            csv_string += f"{idx},{x},{y}\n"

        # Check if the random yashi game is solvable
        solvable = version_one(StringIO(csv_string), rows, n)
        n += 1

    return csv_string
