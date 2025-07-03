import math

class Pallet:
    def __init__(self, weight, id):
        self.weight = weight
        self.length = 1  
        self.width = 1
        self.id = id

class BoxTruck:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.grid = [[0 for _ in range(width)] for _ in range(length)]
        self.pallets = []

    def load_pallets(self, pallet_list):
        # Sort cargo by descending weight
        pallet_list = sorted(pallet_list, key=lambda x: -x.weight)

        # Place every pallet in the pallet list
        for pallet in pallet_list:
            best_position = None  
            min_imbalance = float('inf')

            for x in range(self.length):
                for y in range(self.width):
                    if self.grid[x][y] == 0:
                        # Use a temporary grid to try every position in the truck 
                        temp_grid = [row[:] for row in self.grid]
                        temp_grid[x][y] += pallet.weight
                        # Calculate imbalance in the truck
                        imbalance = self.calculate_imbalance(temp_grid)
                        # Update minimum imbalance every time a new one is found and set it as the best postion
                        if imbalance < min_imbalance:
                            min_imbalance = imbalance
                            best_position = (x, y)
            # Once best postion is found, palce it in the truck
            if best_position:
                x, y = best_position
                self.grid[x][y] += pallet.weight
                self.pallets.append((pallet, (x, y)))
            else:
                print(f"No space for pallet '{pallet.id}' ")

    def calculate_imbalance(self, grid):
        # Find total weight of the whole pallet list
        total_weight = sum(sum(row) for row in grid)
        if total_weight == 0:
            return 0

        x_total_weight = 0
        y_total_weight = 0
        # Find total weight of the x and y planes
        for x in range(self.length):
            for y in range(self.width):
                weight = grid[x][y]
                x_total_weight += x * weight
                y_total_weight += y * weight

        # Find center mass of the x and y planes 
        x_center_mass = x_total_weight / total_weight
        y_center_mass = y_total_weight / total_weight

        # Find center of the truck
        x_center = (self.length - 1) / 2
        y_center = (self.width - 1) / 2

        # Calculate imbalance usinf euclidean distance formula
        imbalance = math.sqrt((x_center_mass - x_center) ** 2 + (y_center_mass - y_center) ** 2)
        return imbalance

    def print_layout(self):
        layout = [['_' for _ in range(self.width)] for _ in range(self.length)]
        for item, (x, y) in self.pallets:
            layout[x][y] = item.id
        print("\nTruck Layout:")
        for row in layout:
            print(' '.join(row))

    def print_info(self):
        total_weight = sum(sum(row) for row in self.grid)
        imbalance = self.calculate_imbalance(self.grid)

        print(f" Total cargo weight: {total_weight:.2f}")
        print(f" Imbalance distance from center: {imbalance:.4f}")

    # Function to simulate a load in order starting at the back of the box truck. 
    def place_in_order(self, cargo_list):
        pos_index = 0
        for x in range(self.length):
            for y in range(self.width):
                if pos_index >= len(cargo_list):
                    return
                if self.grid[x][y] == 0:
                    item = cargo_list[pos_index]
                    self.grid[x][y] += item.weight
                    self.pallets.append((item, (x, y)))
                    pos_index += 1
        if pos_index < len(cargo_list):
            print(" Error at loading")

""" Test Implementation """
cargo = [
    Pallet(weight=300, id='A'),
    Pallet(weight=200, id='B'),
    Pallet(weight=150, id='C'),
    Pallet(weight=400, id='D'),
    Pallet(weight=250, id='E'),
    Pallet(weight=100, id='F'),
    Pallet(weight=50, id='G'),
]

# Test 1
truck = BoxTruck(length=10, width=5)
truck.load_pallets(cargo)
truck.print_layout()
truck.print_info()


# Test 2
truck = BoxTruck(length=10, width=5)
truck2 = BoxTruck(length=10, width=5)
truck.load_pallets(cargo)
truck.print_layout()
truck.print_info()
truck2.place_in_order(cargo)
truck2.print_layout()
truck2.print_info()

# Test 3
truck = BoxTruck(length=2, width=2)
truck.load_pallets(cargo)
truck.print_layout()
truck.print_info()
