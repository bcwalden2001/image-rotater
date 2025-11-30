import cv2
import numpy as np
from math import sin, cos, pi, sqrt

# Matrix multiplication between two 2D numPy arrays
def multiply_matrix(A1, A2):
    if A1.shape[1] != A2.shape[0]:
        raise ValueError("Matrix dimensions do not match for multiplication.")
    final_matrix = np.zeros((A1.shape[0], A2.shape[1]))
    for i in range(A1.shape[0]):
        for j in range(A2.shape[1]):
            for k in range(A1.shape[1]):
                final_matrix[i, j] += A1[i, k] * A2[k, j]
    return final_matrix

# Converting float image to uint8
def to_uint8_image(image_float):
    scaled = image_float * 255  # Scaling from 0-1 to 0-255
    result = np.zeros_like(scaled, dtype=np.uint8)
    for i in range(scaled.shape[0]):
        for j in range(scaled.shape[1]):
            for c in range(3):  # Iterating over RGB channels
                val = scaled[i][j][c]
                # Handling out of bounds values
                if val < 0:
                    val = 0
                elif val > 255:
                    val = 255
                result[i][j][c] = int(val)
    return result

# Prompting user for input
rotations = int(input("Enter the number of rotations: "))
angle = int(input("Enter the angle of rotation: "))

# Rotating image multiple times
def rotate_image(image, angle, rotations):

    rows, cols = image.shape[:2]    # Image dimensions
    pixels_in_image = rows * cols   # Total pixels in image

    dist_rgbs_absolute = []         # Empty list to store color differences
    dist_rgbs_rounding = []         # Empty list to store pixel rounding errors

    radians = angle * pi / 180      # Converting degrees to radians

    R = np.array([[cos(radians), -sin(radians)], [sin(radians), cos(radians)]])     # Rotation matrix 

    # Determining coordinates of the image corners
    corner_points = np.array([
        [-cols / 2, -rows / 2],
        [cols / 2, -rows / 2],
        [cols / 2, rows / 2],
        [-cols / 2, rows / 2]
    ])

    # Rotating cornerpoint to find the new image bounds
    new_corners = multiply_matrix(R, corner_points.T).T     # Changing corner points for dynamic resizing
    min_x, min_y = new_corners.min(axis=0)
    max_x, max_y = new_corners.max(axis=0)
    new_width = int(round(max_x - min_x))
    new_height = int(round(max_y - min_y))

    # Empty image to store result after rotation
    rotated_image = np.zeros((new_height, new_width, 3), dtype=np.float32)

    # Shift value for translation
    offset_x = new_width // 2
    offset_y = new_height // 2

    # Creating a single total rotation for repeated rotations
    total_rotation = rotations * angle  # Calculating the total angle of rotation
    total_radians = total_rotation * pi / 180  # Converting degrees to radians
    R_total = np.array([[cos(total_radians), -sin(total_radians)], 
                        [sin(total_radians), cos(total_radians)]])
    
    # Iterating over every pixel in the original image
    for i in range(rows):
        for j in range(cols):

            # Translating pixel coordinates to be centered around (0, 0)
            relative_pos = np.array([[j - cols / 2], [i - rows / 2]])

            # Applying the rotation matrix
            rotated_pos = multiply_matrix(R_total, relative_pos)

            # Translating coordinates back to original image space
            displayed_x = int(rotated_pos[0, 0] + offset_x)
            displayed_y = int(rotated_pos[1, 0] + offset_y)
            actual_x = rotated_pos[0, 0] + offset_x
            actual_y = rotated_pos[1, 0] + offset_y

            # Checking if new pixel position is inside the image bounds
            if 0 <= displayed_x < new_width and 0 <= displayed_y < new_height:
                # Calculate pixel rounding error between float and integer position
                rounding_difference = sqrt((actual_x - displayed_x) ** 2 + (actual_y - displayed_y) ** 2)
                dist_rgbs_rounding.append(rounding_difference)

                # Only computing color error if the destination pixel is inside the original bounds
                if 0 <= i < rotated_image.shape[0] and 0 <= j < rotated_image.shape[1]:
                    RGB_difference = sqrt(
                        (image[i][j][2] - rotated_image[displayed_y][displayed_x][2]) ** 2 +
                        (image[i][j][1] - rotated_image[displayed_y][displayed_x][1]) ** 2 +
                        (image[i][j][0] - rotated_image[displayed_y][displayed_x][0]) ** 2)
                    dist_rgbs_absolute.append(RGB_difference)

                # Assign original pixel color to the rotated position
                rotated_image[displayed_y, displayed_x] = image[i, j]

    # Average absolute color error per pixel
    absolute_error = sum(dist_rgbs_absolute) / pixels_in_image

    # Average rounding error per pixel
    rounding_error = sum(dist_rgbs_rounding) / (pixels_in_image * rotations)

    return rotated_image, absolute_error, rounding_error

# Loading the image again
image = cv2.imread("knight_cat.png")

# Normalizing between to float range for precise calculations
image_float = image / 255.0

# Performing the rotation
rotated, absolute_error, rounding_error = rotate_image(image_float, angle, rotations)

# Printing the errors to the console
print(f"Absolute error: {absolute_error:.3f}")
print(f"Pixel rounding error: {rounding_error:.3f}")
print(f"# Rotations * Pixel Displacement: {rotations * rounding_error}")

# Converting to a displayable format
rotated_display = to_uint8_image(rotated)

label = f"{rotations} rotations, {angle} degrees"
cv2.imshow(label, rotated_display)

# Waiting for key to be pressed to close all the windows
key = cv2.waitKey(0)

# Closes all windows
cv2.destroyAllWindows()
