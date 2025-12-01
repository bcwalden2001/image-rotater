## Summary

This program rotates a raster image by a user-specified angle and number of repetitions. It maps each original pixel to a new position on a dynamically resized canvas to prevent clipping, displays the rotated image, and calculates error metrics to analyze pixel displacement and color fidelity.

## Methodology

### Setup: 
The program imports OpenCV, NumPy, and math utilities, then loads the image normalized to floating-point precision.

### Matrix Operations: 
A custom matrix multiplication function is used instead of NumPy’s built-in operations. A helper function converts floating-point RGB values back to 8-bit integers for display.

### Rotation Calculation:
A 2×2 rotation matrix is constructed based on the user-defined angle. The four corners of the image are rotated to compute the new canvas size, ensuring no clipping occurs. A total rotation matrix is calculated by multiplying the angle by the number of rotations, reducing compounding rounding errors.

### Pixel Mapping:
Each pixel is translated to a centered coordinate system and multiplied by the total rotation matrix. The transformed coordinates are rounded and mapped to the new output frame.

### Error Tracking: 
Two metrics are recorded during rotation:

- Absolute color error: Difference between the original pixel RGB values and the rotated pixel’s RGB values.
- Pixel rounding error: Euclidean distance between the exact floating-point coordinate and the final integer pixel coordinate.

### Display: 
The rotated floating-point image is converted to 8-bit format and displayed in a window. Error metrics are printed to the console.

### Results

<img width="385" height="595" alt="image" src="https://github.com/user-attachments/assets/60b3e6de-e4ce-4c5b-aed2-be3d76f8c2e0" />

<img width="781" height="303" alt="image" src="https://github.com/user-attachments/assets/a87acf64-af8d-4e10-b238-d4089e29bc74" />

## Conclusion

The program preserves RGB values well, as shown by low absolute color error. Pixel rounding error, however, accumulates across multiple rotations, causing slight displacement of pixel positions. This demonstrates the trade-off between maintaining color fidelity and the limitations of rounding in repeated geometric transformations.




