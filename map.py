import csv


def load_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [list(map(int, row)) for row in reader]

collision_map = load_csv('map_Tile Layer 1.csv')
