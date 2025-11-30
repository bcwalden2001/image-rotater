## Summary

This program performs image rotation on a raster image using a manually implemented rotation matrix, transforming the resulting image into an expanded canvas (or container), mapping each original pixel to its rotated position. After rotation data is given by the user, the program will display the newly-constructed image in a window and log error metrics.

## Methodology

The program begins by importing OpenCV, NumPy, and several trigonometric utilities, and loads an image normalized to floating-point precision. A custom matrix multiplication function is defined, alternatively NumPy’s **dot** or **matmul** built-ins would work. A helper function was also implemented to convert floating-point RGB values back to 8-bit integers.

In order to rotate the image, the user provides the number of repeated rotations and the rotation angle. The program constructs a 2×2 rotation matrix and applies it not only to pixels but also to the four corner points of the image, enabling computation of the new bounding box after rotation. This ensures the rotated output image has the correct dimensions, especially to avoid clipping of the corners. A total rotation matrix is then calculated by multiplying the angle by the number of rotations (rather than rotating the image step-by-step), reducing compounding rounding error.

Every pixel in the original image is translated into a centered coordinate system, multiplied by the total rotation matrix, and mapped into the new output frame. The code tracks two error metrics during this process:
• **absolute color error**—difference between the original pixel’s RGB and the value stored at the rotated pixel’s new location, and
• **pixel rounding error**—the Euclidean distance between the exact floating-point coordinate and the final, rounded integer pixel coordinate.

Finally, the rotated floating-point image is converted to an 8-bit format so it can be displayed.

The images below shows how accurate pixels are re-constructed largely effected by the degree of rotation data.

<img width="385" height="595" alt="image" src="https://github.com/user-attachments/assets/60b3e6de-e4ce-4c5b-aed2-be3d76f8c2e0" />

<img width="781" height="303" alt="image" src="https://github.com/user-attachments/assets/a87acf64-af8d-4e10-b238-d4089e29bc74" />

## Conclusion

Based on the error calculation chart above, there is less variation in absolute color error than pixel rounding error which means that RGB values are preserved fairly well and no signifcant change in color data can be seen for repeating rotations. Pixel locations, however, are being displaced differently across repeated rotations due to the limitations of rounding floating-point coordinates to integers. These results show that the rotation algorithms are effective at preserving what is displayed but less so at determining where the pixels ends up.
