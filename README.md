## Summary

This program performs image rotation on a raster image using a manually implemented rotation matrix, transforming the resulting image into an expanded canvas (or container), mapping each original pixel to its rotated position. After rotation data is given by the user, the program will display the newly-constructed image in a window and log error metrics.

## Methodology

The program begins by importing OpenCV, NumPy, and several trigonometric utilities, and loads an image normalized to floating-point precision. A custom matrix multiplication function is defined, alternatively NumPy’s **dot** or **matmul** built-ins would work. A helper function was also implemented to convert floating-point RGB values back to 8-bit integers.

In order to rotate the image, the user provides the number of repeated rotations and the rotation angle. The program constructs a 2×2 rotation matrix and applies it not only to pixels but also to the four corner points of the image, enabling computation of the new bounding box after rotation. This ensures the rotated output image has the correct dimensions, especially to avoid clipping of the corners. A total rotation matrix is then calculated by multiplying the angle by the number of rotations (rather than rotating the image step-by-step), reducing compounding rounding error.

Every pixel in the original image is translated into a centered coordinate system, multiplied by the total rotation matrix, and mapped into the new output frame. The code tracks two error metrics during this process:
• **absolute color error**—difference between the original pixel’s RGB and the value stored at the rotated pixel’s new location, and
• **pixel rounding error**—the Euclidean distance between the exact floating-point coordinate and the final, rounded integer pixel coordinate.

Finally, the rotated floating-point image is converted to an 8-bit format so it can be displayed.
