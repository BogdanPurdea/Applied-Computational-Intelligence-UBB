<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 3 VIDEO SENSORS -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 3 - Video Sensors Part 2**


---

## 📖 3.1 Camera Parameters and 3D Perception Review

To understand how cameras capture the world, we must define the parameters that translate 3D physical space into 2D images.

### 📑 3.1.1 Intrinsic Parameters

Intrinsic parameters describe the internal characteristics of the camera:
* **Camera Center ($O$):** The physical point inside the camera where light rays intersect;
* **Principal Point ($u_0, v_0$):** The point where the central viewing axis hits the image sensor;
* **Image Coordinates ($u, v$):** The 2D pixel grid coordinates on the final image;
* **Focal Length ($f$):** The physical distance from the camera center to the principal point;
* **Pixel Size ($dpx, dpy$):** The physical dimensions of a single pixel on the sensor.

The focal length is often converted into pixel units for mathematical convenience. This gives us two focal lengths, one for the x-axis and one for the y-axis. The formulas are $f_x = \frac{f}{dpx}$ and $f_y = \frac{f}{dpy}$.

These properties form the Intrinsic Camera Matrix ($K$), which projects a 3D point $P(x, y, z)$ into 2D pixel coordinates.

$$K = \begin{bmatrix} f_x & 0 & u_0 \\ 0 & f_y & v_0 \\ 0 & 0 & 1 \end{bmatrix}$$

The projection equation is calculated as follows:

$$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = K \cdot \begin{bmatrix} x/z \\ y/z \\ 1 \end{bmatrix}$$

### 📑 3.1.2 Extrinsic Parameters

Extrinsic parameters represent the position and orientation of the camera within a larger world coordinate system. By convention, in automotive applications, the center of the vehicle's rear axis acts as the origin of this world system.

Extrinsics consist of a rotation matrix ($R$) and a translation vector ($T$).
* **Translation Vector ($T$):** Represents the shift of the camera along the x, y, and z axes;
* **Rotation Matrix ($R$):** Represents how much the camera is tilted or turned. It accounts for three specific 3D rotations: pitch (up/down), yaw (left/right), and roll (tilt side-to-side).

Combining the intrinsic and extrinsic parameters allows us to map any world point to a pixel:

$$\begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim K \cdot \left( R \cdot \begin{bmatrix} x \\ y \\ z \end{bmatrix} + T \right) = K \cdot [R | T] \cdot \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

### 📑 3.1.3 3D Reconstruction and Disparity

3D reconstruction is the process of calculating the 3D shape and position of real objects strictly from 2D images. This is achieved using two cameras (a stereo system) or a single moving camera capturing images over time (a mono system).

To perform 3D reconstruction easily, images undergo **rectification**. Rectification is a digital image processing technique that warps images so that corresponding points on an object appear on the exact same horizontal scan-line in both views.

Once rectified, the system calculates **disparity** ($d$), which is the horizontal shift in pixel location of an object between the two images.
* Disparity is small for distant objects;
* Disparity is large for close objects.

Depth ($z$) is calculated using the focal length in pixels ($f_x$), the baseline distance between the cameras ($b$), and the disparity ($d$):

$$z = \frac{f_x \cdot b}{d}$$


---

## 📖 3.2 Mathematical Foundations: Vectors and Matrices

To find the mathematical relationship between two different views of the same object, we rely on vector mathematics.

* **Vector:** A quantity possessing both a direction and a magnitude (length);
* **Coordinates:** A vector's specific values when projected onto orthogonal (perpendicular) axes. For a 3D vector $\overline{a}$, the coordinates are written as $\overline{a} = \begin{bmatrix} a_1 & a_2 & a_3 \end{bmatrix}$;
* **Dot Product:** An operation that multiplies two vectors to produce a single number. If the vectors are perpendicular, their dot product is exactly zero.

  $$\overline{a} \cdot \overline{b} = a_1 b_1 + a_2 b_2 + a_3 b_3$$
  
* **Cross Product:** An operation that multiplies two vectors to produce a *new* vector that is entirely perpendicular to both original vectors.

The cross product can be written as a matrix multiplication. The first vector is transformed into a skew-symmetric matrix (denoted as $\overline{a}_\times$), which then multiplies the second vector:

$$\overline{a} \times \overline{b} = \begin{bmatrix} 0 & -a_3 & a_2 \\ a_3 & 0 & -a_1 \\ -a_2 & a_1 & 0 \end{bmatrix} \cdot \begin{bmatrix} b_1 \\ b_2 \\ b_3 \end{bmatrix} = \overline{a}_\times \cdot \overline{b}$$

### 📑 3.2.1 Translation and Rotation

When managing two different coordinate systems (like two cameras), we use translation and rotation to relate them.
* **Translation:** A translation vector ($\overline{T}$) represents the exact coordinates of the second system's origin point relative to the first system. We update positions using $\overline{X_1} = \overline{X_2} + \overline{T}$;
* **Rotation:** A rotation matrix ($R$) aligns the axes of the two systems. A pure rotation operation is expressed as $R \cdot \overline{X_1}$.

A general 3D rotation combines individual rotations around the x, y and z axes into a single multiplied matrix.


---

## 📖 3.3 The Essential Matrix

The **Essential Matrix** ($E$) mathematically connects the 3D physical coordinates of a point as seen by two different cameras.

Imagine two cameras observing a single physical point $P$.
* $C_1$ is the first camera, with the point appearing along a vector $\overline{P_1}$;
* $C_2$ is the second camera, with the point appearing along a vector $\overline{P_2}$;
* $\overline{T}$ is the translation vector bridging the two cameras;
* $R$ is the rotation matrix aligning the second camera to the first.

Because $\overline{P_1}$, $\overline{P_2}$, and $\overline{T}$ all intersect at the cameras and the object, they lie on the exact same geometric plane. This creates a **coplanar constraint**.

Mathematically, if three vectors are coplanar, taking the cross product of two of them creates a perpendicular vector. Taking the dot product of this new perpendicular vector with the third original vector must equal zero.

When we convert $\overline{P_2}$ into the first camera's coordinate system (creating $R \cdot \overline{P_2}$), the coplanar constraint formula is written as:

$$\overline{P_1}^T \cdot (\overline{T}_\times \cdot R) \cdot \overline{P_2} = 0$$

*(Note: The prime symbol '$'$' denotes a matrix transpose)* 

The **Essential Matrix** ($E$) is defined as the middle portion of this constraint:

$$E = \overline{T}_\times \cdot R$$

The Essential Matrix possesses 5 Degrees of Freedom (DoF). It accounts for the 3 angles of rotation (pitch, roll, yaw) and 2 degrees of translation. Translation only has 2 DoF here because the equation equals zero, meaning scaling the matrix does not change the mathematical truth of the equation.


---

## 📖 3.4 The Fundamental Matrix

The Essential Matrix requires knowledge of physical 3D space. The **Fundamental Matrix** ($F$) adapts this concept to work entirely in 2D image pixel coordinates.
To transition to pixel coordinates, we recall that the projection from 3D space to pixel space uses the intrinsic matrix $K$. By substituting the physical coordinates ($\overline{P_1}, \overline{P_2}$) with their pixel equivalents ($u_1, u_2$) multiplied by the inverse of the camera matrices ($K^{-1}$), we get the Fundamental Matrix constraint:

$$\begin{bmatrix} u_1 \\ v_1 \\ 1 \end{bmatrix}^T \cdot K_1^{-T} \cdot (\overline{T}_\times \cdot R) \cdot K_2^{-1} \cdot \begin{bmatrix} u_2 \\ v_2 \\ 1 \end{bmatrix} = 0$$

The **Fundamental Matrix** ($F$) encapsulates the central matrices into a single entity:

$$F = K_1^{-T} \cdot (\overline{T}_\times \cdot R) \cdot K_2^{-1}$$

### Intuition: Epipolar Lines

The Fundamental Matrix dictates that a point in the first image maps to a specific *line* in the second image.

If we multiply the pixel coordinates of image 1 by the Fundamental Matrix ($u_1^T \cdot F$), the result is a vector $\begin{bmatrix} a & b & c \end{bmatrix}$. This vector represents the coefficients of a standard 2D line equation ($ax + by + c = 0$). The matching pixel in the second image ($u_2, v_2$) must perfectly fall on this line for the equation to equal zero. This is known as an epipolar line.


---

## 📖 3.5 Estimating the Essential Matrix

In real-world applications, identifying matching pixels between two images involves noise and slight inaccuracies. Therefore, the equation $\overline{P_1}^T \cdot E \cdot \overline{P_2} = 0$ is rarely perfectly zero.

To estimate the actual Essential Matrix, we collect multiple corresponding points between images and calculate a residual error ($r_i$) for each point pairing. The goal is to find the matrix parameters ($\alpha, \beta, \gamma, t_1, t_2$) that result in the smallest possible sum of squared errors:

$$\text{argmin} \sum_{i} (r_i(\alpha, \beta, \gamma, t_1, t_2))^2$$

This minimization is commonly solved using the **Gauss-Newton algorithm**.

* *Algorithm Explanation:* The Gauss-Newton algorithm is an iterative mathematical method used to solve non-linear least squares problems. It operates by guessing an initial solution, calculating the slope (gradient) of the error surface, and taking a step downwards toward the lowest error point, repeating this process until the solution converges at a minimum value.


---

## 📖 3.6 Projective Geometry and Conclusions

### 📑 3.6.1 Homography Matrices

When observing a purely flat, planar surface, the relationship between two camera views simplifies into a **Homography Matrix** ($H$).
A physical plane point $P$ can be transferred to the first camera view as $P_1 = H_1 \cdot P$ and to the second view as $P_2 = H_2 \cdot P$. We can directly transfer pixels from camera 1 to camera 2 using an image homography matrix ($H_{image}$):

$$H_{image} = H_2 \cdot H_1^{-1}$$

$$P_2 = H_{image} \cdot P_1$$


---

## 📖 3.7 Summary

The Essential Matrix is a fundamental mathematical concept required for key video sensor tasks in automated driving systems.
* It is mandatory for **Rectification**, enabling the alignment of image planes to simplify depth calculation;
* It is mandatory for **Ego-motion estimation**, allowing a vehicle to track its own movement relative to its surroundings;
* These principles apply universally whether the system uses a mono camera in motion or a static stereo camera pair.
