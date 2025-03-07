from read_coordinates import read_coordinates, get_serial_port
import math
from scipy.stats import pearsonr
from matplotlib import pyplot as plt
def compute_distance(point1: list[int, int], point2: list[int, int]) -> float:

    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


if __name__ == "__main__":
    serial_port = get_serial_port()
    print("Shape 1:")
    coordinates1 = read_coordinates(serial_port=serial_port, timeout = 5)
    print("Shape 1: ", coordinates1)

    print("Shape 2:")
    coordinates2 = read_coordinates(serial_port=serial_port, timeout = 5)
    print("Shape 2: ", coordinates2)

    
    origin_distances_1 = []
    origin_distances_2 = []

    coefficients: dict = {}

    for point in coordinates1:
        origin_distances_1.append(compute_distance([0,0], point))

    for point in coordinates2:
        origin_distances_2.append(compute_distance([0,0], point))

    # Plot the distances
    plt.subplot(2, 1, 1)
    plt.plot([i for i in range(len(origin_distances_1))], [origin_distances_1[i] for i in range(len(origin_distances_1))], "o")
    plt.subplot(2, 1, 2)
    plt.plot([i for i in range(len(origin_distances_2))], [origin_distances_2[i] for i in range(len(origin_distances_2))], "o")
    plt.show()

    # Compute the pearsons correlation coefficient
    smaller, larger = (origin_distances_1, origin_distances_2) if (len(origin_distances_1) < len(
        origin_distances_2)) else (origin_distances_2, origin_distances_1)
    
    corr, _ = pearsonr(smaller, larger[:len(smaller)])
    
    # Print the similarity(correlation) between two shapes
    print("Correlation coefficient: ", corr)