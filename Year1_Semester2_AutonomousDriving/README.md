<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 1 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 1 - Artificial Intelligence-Based Perception in Self-Driving Vehicles**

------------------------------------------------------------------------

## 📖 1.1 Introduction to Data-Driven Perception
Modern self-driving cars use Artificial Intelligence (AI) to understand their surroundings. This is called **perception**. 

* **The Shift to 360° Systems**: Older systems used single sensors for simple tasks. Modern vehicles use multiple sensors (cameras and radars) placed all around the car to get a full 360-degree view; 
* **The AI Pipeline**: The car's computer takes sensor data and runs it through three main steps: Perception (understanding the scene), Prediction (guessing what will happen next), and Planning (deciding how to drive);
* **Mobile Computers**: Vehicles are turning into advanced, AI-powered mobile computing centers. 

### 📑 1.1.1 The Rise of Foundation Models
The industry is moving from classical Machine Learning to **Foundation Models**.
* **Definition**: A foundation model is a very large AI model. It is trained on huge amounts of data that has not been labeled by humans. Once trained, it can be reused for many different tasks;
* **Emergence**: The model learns behaviors naturally from the data, rather than being strictly programmed to do them;
* **Homogenization**: The exact same methods can be used to solve completely different problems;

------------------------------------------------------------------------

## 📖 1.2 Main Challenges in AI for Self-Driving
Building safe and effective AI for cars involves four main challenges: Representation, Safety, Efficiency and Cost;

### 📑 1.2.1 The Representation Challenge
**Representation** is how the AI internally maps and understands the physical world;
* **The Problem**: The AI must perform well even when the environment changes (e.g., different weather or new cities). Just training the AI on a specific driving task is not enough to help it truly understand the world;
* **Solutions**: Engineers use different methods to train the AI. They use **Self-Supervision** (where the AI learns by finding patterns in data without human labels) and **Large Language Models** to give the AI extra guidance;
* **Inductive Bias**: This is a set of built-in assumptions that help the AI learn. Inductive bias is strictly required for the AI to learn anything useful.

### 📑 1.2.2 The Safety Challenge
Cars must follow strict mandatory safety rules, such as ISO 26262 and ISO/PAS 21448.
* **Inherently Safe AI:** Building an AI that perfectly avoids all hazards is impossible with today's technology;
* **Safe Fail:** When a system breaks, it must fail safely. The car must stay on the road and safely slow down or stop. This requires real-time error detection;
* **Safety Margins:** The AI often performs worse in the real world than it did in the lab. Engineers fix this by improving **model robustness**. This includes estimating when the AI is uncertain and detecting errors during driving.

### 📑 1.2.3 The Efficiency Challenge
The computers inside cars are limited. They have low power, low internet bandwidth, and limited processing abilities. However, they still need to react in real-time. 
* **Solutions**: Engineers shrink the AI models to make them run faster.
    * **Knowledge Distillation (KD)**: A small model (the student) is trained to copy the behavior of a massive model (the teacher);
    * **Quantization**: This shrinks the math inside the AI to use less memory;
    * **Neural Architecture Search (NAS)**: An automated process that finds the fastest and best shape for the AI model.

### 📑 1.2.4 The Cost Challenge
Creating AI is very expensive.
* **Problems**: Collecting data takes too long, legal rules (like GDPR) make data sharing hard, and development costs are unpredictable;
* **Solutions*:
    * **Active Learning:** The AI asks humans to label only the most confusing or "interesting" images, saving time and money;
    * **Federated Learning:** Cars learn locally and only share their learned patterns with the cloud, not raw private data;
    * **Multi-Task Learning:** One AI model learns to do many tasks at once, saving computer power.

------------------------------------------------------------------------

## 📖 1.3 Key Takeaways
* **Hardware & Software**: Self-driving relies on advanced computers, computer vision, and machine learning;
* **No Free Lunch Theorem**: Even with massive amounts of data, an AI cannot learn without built-in assumptions (inductive bias);
* **The Future**: The industry is slowly moving past just analyzing sensor data. The ultimate goal is **end-to-end driving**, where a single AI takes in camera video and directly outputs steering wheel and pedal commands;
* **Industry & Academia**: Solving these massive open problems requires schools and companies to work closely together.

<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 2 VIDEO SENSORS -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 2 - Video Sensors**

## 📖 2.1 Introduction to Video Sensors

Automated driving relies on a combination of different sensor technologies. These components include video cameras, radar systems, ultrasonic sensors, and electric power steering. A central processing unit collects data from these sensors. Software engineering ties all these systems together.

The engineering teams develop software for both mono (single) and stereo (dual) video systems. They build computer vision algorithms, which allow computers to understand digital images. They also develop machine learning algorithms for automated driving and driver assistance.

Specific examples of these algorithms include:
* **Visual Odometry:** This technique estimates a vehicle's position and path by analyzing a continuous sequence of camera images;
* **3D Free-space:** This identifies safe, empty areas on the road where the vehicle can drive without hitting obstacles;
* **Deep Learning:** This is a type of artificial intelligence that uses neural networks to recognize complex patterns, like detecting pedestrians or reading street signs.

------------------------------------------------------------------------

## 📖 2.2 Images and Their Representation

The simplest way to understand cameras is the pinhole camera model. Light passes through a tiny hole and projects an inverted (upside-down) image. This basic design lets in only a small amount of light. However, modern geometric models used in software do not require this image inversion.

A photograph is an image created when a camera captures light. This light falls on a light-sensitive surface and is then encoded into a digital format.

A digital image is the numeric representation of that picture. It is stored as a vector or a matrix of numbers. Each number corresponds to a single pixel. A pixel is the smallest individual dot of color in an image.

The most common model used to represent color is the RGB model. RGB stands for Red, Green, and Blue. Every single pixel is represented by three separate numbers, indicating the amount of red, green, and blue light. Because it must store three values for every pixel, a color image uses more memory than a grayscale (black and white) image.

------------------------------------------------------------------------

## 📖 2.3 Camera Calibration

Computer vision attempts to extract 3D real-world information from 2D flat image data. To do this, the system must use a mathematical model to transform 3D points into 2D pixels. Calibration is the process of finding the exact parameters for this model to ensure the real world projects correctly onto the image plane.
Calibration happens in two ways:

* **Static Calibration:** This occurs before the camera is used on the road. The camera is pointed at a static target with a known visual pattern. The software detects where the pattern is in the image and compares it to where it expects the pattern to be. This comparison computes both the internal and external parameters;
* **Online Calibration:** This happens continuously while the car is driving. The camera's physical position can shift dynamically due to external influences, such as a heavy baggage load altering the car's tilt. The system detects this de-calibration and adjusts the math automatically. The geometric model is not fixed; it changes over time.

### 📑 2.3.1 Intrinsic Parameters

Intrinsic parameters describe the internal geometry and optical traits of the camera itself. There are five intrinsic parameters:
* **Camera Center ($O$):** The physical origin point of the camera;
* **Principal Point ($u_0, v_0$):** The center coordinate of the image;
* **Focal Length ($f$):** The distance from the camera center $O$ to the principal point;
* **Pixel Size ($dpx, dpy$):** The physical width and height of a single pixel on the sensor;
* **Focal Length in Pixels ($f_x, f_y$):** The focal length scaled by the pixel dimensions. Specifically, $f_x = f \cdot dpx$ and $f_y = f \cdot dpy$;

These parameters are combined into an intrinsic matrix called $K$:

$$K = \begin{bmatrix} f_x & 0 & u_0 \\ 0 & f_y & v_0 \\ 0 & 0 & 1 \end{bmatrix}$$

Using similar triangles, a 3D point $P(x, y, z)$ projects to 2D image coordinates $u$ and $v$:

* Horizontal coordinate: $\frac{u - u_0}{f_x} = \frac{x}{z}$ 
* Vertical coordinate: $\frac{v - v_0}{f_y} = \frac{y}{z}$ 

### 📑 2.3.2 Extrinsic Parameters

Extrinsic parameters describe the camera's position and orientation relative to the real world. By convention, the origin of this world coordinate system is the center of the car's rear axis.
These parameters are represented by:
* **Rotation Matrix ($R$):** This accounts for three rotations applied in 3D space: pitch (tilting up or down), roll (tilting side to side), and yaw (turning left or right);
* **Translation Vector ($T$):** This accounts for the physical distance the camera is shifted from the origin.

Together, they form a combined matrix $[R|T]$.
The complete matrix-based projection formula, using both intrinsic and extrinsic parameters, is:

$$ \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim K \cdot \left( R \cdot \begin{bmatrix} x \\ y \\ z \end{bmatrix} + T \right) = K \cdot [R|T] \cdot \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} $$

------------------------------------------------------------------------

## 📖 2.4 Distortions

Distortion is an unwanted alteration of the original image. In the presence of distortions, the standard perspective projection model is no longer valid.

There are two primary types of distortion:

**1. Radial Distortion**
This is caused by the physical curve of the camera lens. Straight lines in the real world appear curved in the image. It manifests in two ways: barrel distortion (where the image bulges outward) and pincushion distortion (where the image pinches inward).
It is mathematically modeled using the radius $r$ (where $r^2 = x^2 + y^2$) and distortion coefficients $k_1$ and $k_2$. The equation is:

$$
\begin{aligned}
x_{undistorted} - x_{distorted}
&=
x \left(k_1 r^2 + k_2 r^4 + \cdots\right)
\\
y_{undistorted} - y_{distorted}
&=
y \left(k_1 r^2 + k_2 r^4 + \cdots\right)
\end{aligned}
$$

**2. Tangential Distortion**
This occurs due to the physical misalignment of the camera lens and the camera sensor. If the lens is not perfectly parallel to the image sensor, parts of the image will look unnaturally close.
It uses tangential distortion coefficients $p_1$ and $p_2$. The equation is:

$$
\begin{aligned}
x_{undistorted} - x_{distorted}
&=
2 p_1 x y + p_2 \left(r^2 + 2x^2\right)
\\
y_{undistorted} - y_{distorted}
&=
p_1 \left(r^2 + 2y^2\right) + 2 p_2 x y
\end{aligned}
$$

------------------------------------------------------------------------

## 📖 2.5 Projective Geometry

Projective geometry is a branch of mathematics that studies the properties of objects that remain invariant (unchanged) under projective transformations. It is a very useful tool in computer vision.
* **Euclidean geometry** describes objects "as they are". Their true sizes and parallel lines are maintained regardless of how they move;
* **Projective geometry** describes objects "as they appear" to a camera. For example, parallel lane lines on a road will appear to converge in the distance.

Projective geometry rules can only be applied after lens distortions have been mathematically eliminated. Once corrected, the image formation can be correctly modeled based on perspective projection. Using planar homography matrices ($H$), a point $P$ on a flat plane can be transferred from the view of a first camera ($P_1$) to the view of a second camera ($P_2$) using the formula: $P_2 = H_{image} \cdot P_1$, where $H_{image} = H_2 \cdot H_1^{-1}$.

------------------------------------------------------------------------

## 📖 2.6 3D Reconstruction

3D reconstruction is the process of calculating the 3D shape and position of real objects entirely from flat 2D images.

This can be accomplished using two types of setups:

* **Stereo camera system:** Two cameras placed at different positions look at the same object at the exact same time;
* **Mono camera system:** A single moving camera captures the same scene at different points in time.

Before depth can be calculated, the images must undergo rectification. Rectification is a mathematical process that aligns the images so that matching points appear on the exact same horizontal scan-line.

### 📑 2.6.1 Disparity and Depth Calculation

Disparity is the physical displacement (distance) between a point's location in the left image and its location in the right image. By measuring disparity, the system can determine how far away an object is.
* If an object is close, the disparity is large;
* If an object is far away, the disparity is small.

To calculate the exact depth ($z$), the software uses the focal length in pixels ($f_x$), the baseline distance between the two cameras ($b$), and the disparity ($d$):
$$z = \frac{f_x \cdot b}{d}$$

### 📑 2.6.2 The Inverse Problem

Once the depth ($z$) is known, the system solves the inverse problem to find the actual real-world $x$ and $y$ coordinates. It reverses the standard projection formulas:
* Horizontal position: $x = \frac{(u - u_0) \cdot z}{f_x}$ 
* Vertical position: $y = \frac{(v - v_0) \cdot z}{f_y}$


<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 3 VIDEO SENSORS -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 3 - Video Sensors Part 2**

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

## 📖 3.4 The Fundamental Matrix

The Essential Matrix requires knowledge of physical 3D space. The **Fundamental Matrix** ($F$) adapts this concept to work entirely in 2D image pixel coordinates.
To transition to pixel coordinates, we recall that the projection from 3D space to pixel space uses the intrinsic matrix $K$. By substituting the physical coordinates ($\overline{P_1}, \overline{P_2}$) with their pixel equivalents ($u_1, u_2$) multiplied by the inverse of the camera matrices ($K^{-1}$), we get the Fundamental Matrix constraint:

$$\begin{bmatrix} u_1 \\ v_1 \\ 1 \end{bmatrix}^T \cdot K_1^{-T} \cdot (\overline{T}_\times \cdot R) \cdot K_2^{-1} \cdot \begin{bmatrix} u_2 \\ v_2 \\ 1 \end{bmatrix} = 0$$

The **Fundamental Matrix** ($F$) encapsulates the central matrices into a single entity:

$$F = K_1^{-T} \cdot (\overline{T}_\times \cdot R) \cdot K_2^{-1}$$

### Intuition: Epipolar Lines

The Fundamental Matrix dictates that a point in the first image maps to a specific *line* in the second image.

If we multiply the pixel coordinates of image 1 by the Fundamental Matrix ($u_1^T \cdot F$), the result is a vector $\begin{bmatrix} a & b & c \end{bmatrix}$. This vector represents the coefficients of a standard 2D line equation ($ax + by + c = 0$). The matching pixel in the second image ($u_2, v_2$) must perfectly fall on this line for the equation to equal zero. This is known as an epipolar line.

------------------------------------------------------------------------

## 📖 3.5 Estimating the Essential Matrix

In real-world applications, identifying matching pixels between two images involves noise and slight inaccuracies. Therefore, the equation $\overline{P_1}^T \cdot E \cdot \overline{P_2} = 0$ is rarely perfectly zero.

To estimate the actual Essential Matrix, we collect multiple corresponding points between images and calculate a residual error ($r_i$) for each point pairing. The goal is to find the matrix parameters ($\alpha, \beta, \gamma, t_1, t_2$) that result in the smallest possible sum of squared errors:

$$\text{argmin} \sum_{i} (r_i(\alpha, \beta, \gamma, t_1, t_2))^2$$

This minimization is commonly solved using the **Gauss-Newton algorithm**.

* *Algorithm Explanation:* The Gauss-Newton algorithm is an iterative mathematical method used to solve non-linear least squares problems. It operates by guessing an initial solution, calculating the slope (gradient) of the error surface, and taking a step downwards toward the lowest error point, repeating this process until the solution converges at a minimum value.

------------------------------------------------------------------------

## 📖 3.6 Projective Geometry and Conclusions

### 📑 3.6.1 Homography Matrices

When observing a purely flat, planar surface, the relationship between two camera views simplifies into a **Homography Matrix** ($H$).
A physical plane point $P$ can be transferred to the first camera view as $P_1 = H_1 \cdot P$ and to the second view as $P_2 = H_2 \cdot P$. We can directly transfer pixels from camera 1 to camera 2 using an image homography matrix ($H_{image}$):

$$H_{image} = H_2 \cdot H_1^{-1}$$

$$P_2 = H_{image} \cdot P_1$$

------------------------------------------------------------------------

## 📖 3.7 Summary

The Essential Matrix is a fundamental mathematical concept required for key video sensor tasks in automated driving systems.
* It is mandatory for **Rectification**, enabling the alignment of image planes to simplify depth calculation;
* It is mandatory for **Ego-motion estimation**, allowing a vehicle to track its own movement relative to its surroundings;
* These principles apply universally whether the system uses a mono camera in motion or a static stereo camera pair.

<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 4 VIDEO SENSORS -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 4 - Video Sensors Part 3**

## 📖 4.1 3D Computer Vision: Disparity Estimation & Optical Flow

## Recap and Problem Statement

To understand 3D computer vision, we must first understand the types of cameras used to capture the world. A monocular camera is a single camera. A stereo camera is a device with two separate camera lenses. Both types of cameras are typically used in driver assistance applications.

Stereo cameras capture two images of a scene simultaneously. Because the lenses are slightly apart, objects in the left image appear slightly shifted in the right image. The displacement of pixels between the two images is called the disparity. Each pixel in each image has an associated disparity value.

We can calculate the exact distance to an object using this shift. Disparity is small for objects that are far away, and large for objects in close range. The formula relating the depth to the disparity is:

$z=\frac{f\cdot b}{d}$ 

In this equation, $z$ is the depth or distance, $f$ is the focal length of the camera lens, $b$ is the baseline or distance between the two lenses, and $d$ is the disparity.

A disparity map is a visualization of the horizontal shift between the left image and right image. In these maps, a higher intensity of color or brightness is associated with greater disparity.

Monocular cameras do not provide the information necessary to calculate disparity because they only have one lens. Instead, they calculate a result analogous to disparity called optical flow. Optical flow is calculated from pairs of images taken consecutively, instead of simultaneously. Unlike disparity, optical flow has direction, as well as magnitude.

In summary, using a stereo camera, the 3D scene may be reconstructed via a disparity map. Using a monocular camera, the 3D scene may be reconstructed via the optical flow.

--------------------------------------------------------------------

## 📖 4.2 Overview of Disparity Estimation Algorithms

To create a disparity map, the computer must figure out which pixel in the right image matches a specific pixel in the left image. The fundamental matrix is a mathematical tool that relates corresponding points in stereo images. Using the fundamental matrix, and a point in one of the images, one may obtain an associated line in the other image called the epipolar line.

This leads to a rule called the epipolar constraint. Each point in the right image that is associated to some point in the left image will lie on its epipolar line.

To make finding these points easier, we use a process called stereo image rectification. Stereo image rectification is the process of projecting pairs of images onto the same image plane. When this is done, epipolar lines become parallel. In rectified images, all epipolar lines are parallel to the horizontal axis. This means that corresponding points have the same vertical coordinates. Rectification simplifies the task of matching points in stereo image pairs and obtaining disparity maps.

There are four main steps in computing disparity maps:
* In step 1, the matching cost is computed;
* In step 2, the cost is aggregated;
* In step 3, the final disparity is selected;
* In step 4, the disparity is refined;
* Ideally, the output should be a smooth disparity map.

--------------------------------------------------------------------

## 📖 4.3 Matching Cost Computation & Cost Aggregation

### 📑 4.3.1 Step 1: Matching Cost Computation

This step requires a cost criterion to measure the extent of matching between two pixels. This is the stage where it is determined whether the values of two pixels correspond to the same point in a scene. The value is computed at each pixel.

A common technique for this is block matching. For each pixel that we want to match, we choose a small region of pixels in one image and search for the closest matching region in the other. The search is constrained to the epipolar line of the point. In order to determine which is the closest matching region we employ a comparison metric, also known as a cost function.

One of the simplest cost functions is the sum of absolute differences (SAD). This cost function computes the absolute differences between the pixel intensities in two associated blocks and sums up the results. The formula is:

$SAD(x,y,d)=\sum_{(x,y)\in w}|I_{l}(x,y)-I_{r}(x-d,y)|$ 

Another cost function is the census transform (CT). The census transform algorithm creates a bit string by comparing the value of a center pixel to all 8 adjacent pixels. It assigns a 0 if the neighbor is darker, and a 1 if the neighbor is brighter or equal. The formulas are:

$$
\mathrm{Bit}(i,j)=
\begin{cases}
0, & \text{if } I(i,j) < I(x,y) \\
1, & \text{if } I(i,j) \ge I(x,y)
\end{cases}
$$

$Census(x,y)=Bitstring_{(i,j)\in w}(Bit(i,j))$ 

To compare two blocks, the hamming distance is calculated between the reference image and the candidate target image. The total cost function is:

$CT(x,y,d)=\Sigma_{(x,y)\in w}Hamming(Census_{ref}(x,y)-Census_{tar}(x-d,y))$ 

### 📑 4.3.2 Step 2: Cost Aggregation

Knowing the matching cost for a single pixel is not sufficient for precise matching. Therefore, cost aggregation is done locally using a window over multiple pixels. The purpose of cost aggregation is to minimize matching uncertainties.

There are different types of windows used for aggregation:
* A fixed square window is a simple box shape, but it tends to blur object boundaries;
* An adaptive window calculates the cost for the center window and any two other adjacent windows. In practice it is adaptively varied based on context;
* A window with adaptive support weights operates differently. Each pixel is assigned a support weight based on its intensity dissimilarity and distance from the center.

## Disparity Selection & Refinement

### 📑 4.3.3 Step 3: Disparity Selection

In local stereo matching algorithms, after the disparities are calculated, the disparity for each pixel is selected using a local winner-take-all (WTA) strategy. The formula is:

$d_{p}=argmin_{d\in D}C(p,d)$ 

Here, $p$ and $d$ represent the pixel and disparity respectively, $C(p,d)$ is the aggregate cost, and $D$ denotes the set of allowed disparities. The result, $d_{p}$, is the minimum aggregated cost at each pixel.

### 📑 4.3.4 Step 4: Disparity Refinement

Disparity maps obtained initially may contain errors and unmatched pixels, depending on the method used. The accuracy is sensitive to noise and unclear regions.

The purpose of this step is to improve the quality of disparity maps. Disparity maps are refined using a variety of methods, including regularization and interpolation. This is done by reducing noise by filtering inconsistent pixels, and filling in gaps through interpolation.
* Regularization reduces the overall noise by filtering inconsistent pixels;
* The interpolation process is responsible for filling in gaps by approximating the disparity in areas where it is unclear or absent;
* During interpolation, the disparity is calculated based on values in its neighborhood;
* Common techniques for disparity refinement include Gaussian convolution and median filtering.

--------------------------------------------------------------------

## 📖 4.4 Optical Flow

Optical flow is the distribution of apparent velocities of features in successive images in a scene. It visually tracks where pixels move from one frame of a video to the next.

In visual representations of optical flow, the color in the image represents the direction of the flow vector at that pixel. The brightness represents the magnitude or how fast the feature is moving.

--------------------------------------------------------------------

## 📖 4.5 Lucas-Kanade Algorithm

The Lucas-Kanade method takes two images as input and outputs a local flow vector. The goal is to associate a velocity vector, $v=(u,v)$, to each pixel corresponding to some object in a scene, using two consecutive images. The algorithm works on grayscale images.

The Lucas-Kanade algorithm makes two basic assumptions:
1. The pair of images used are separated by a small time increment, $dt$, such that pixel intensities don't rapidly change between consecutive frames;
2. A neighborhood of pixels moves together smoothly, with the same velocity.

### 📑 4.4.1 Mathematical Derivation

By the first assumption, if a point $x=(x,y)$ moves at time $t$, to the point $x+dx$ at time $t+dt$, the intensities of the two points are the same. This is written as:

$I(x+dx,t+dt)=I(x,t)$ 

If $v$ is the optical flow vector, we may write $dx = vdt$, such that $I(x+vdt,t+dt)=I(x,t)$. Because the time increment $dt$ is small, we take the truncated Taylor series of $I$. This simplifies the equation to:

$\nabla I(x,t)\cdot v=-I_{t}(x,t)$ 

This final equation can be written out fully as:

$I_{x}(x,t)u+I_{y}(x,t)v=-I_{t}(x,t)$ 

Remember the second assumption: a neighborhood of pixels moves with the same velocity. Let $x_{1}...x_{n}$ denote $n$ points from the local neighbourhood of $x$. This creates a system of equations that can be represented as $Av=b$.

If there are more than two points, the system $Av=b$ is overdetermined. We may solve it using the method of least squares. The final velocity vector $v$ is calculated with the following formula:

$v=-(A^{T}A)^{-1}A^{T}b$

<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 1 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 5 - Probabilities and Uncertainty**

---

## 📖 5.1 Probabilities and Uncertainty

To understand machine learning, you first must understand probability. Machines use probability to handle uncertainty in the real world. 

### 📑 5.1.1 Sources of Uncertainty
* **Stochastic Universe:** The world has true randomness;
* **Incomplete Observations:** We cannot measure everything;
* **Incomplete Modeling:** Our computer programs are too simple to capture all details.

### 📑 5.1.2 Probability Distributions
A probability distribution shows how likely different outcomes are.
* **Probability Mass Function (PMF):** Used for discrete variables. A discrete variable takes specific separate values (like rolling a 1, 2, or 3 on a dice);
* **Probability Density Function (PDF):** Used for continuous variables. A continuous variable can take any value within a range (like exact temperatures);
* **Joint Probability ($p(x,y)$):** The chance of two events, $x$ and $y$, happening together;
* **Prior Probability ($p(x)$):** The chance of event $x$ happening on its own;
* **Conditional Probability ($p(y|x)$):** The chance of event $y$ happening, given that event $x$ is already known;
    * **Formula:** $p(y|x)=\frac{p(x,y)}{p(x)}$;
    * *Explanation:* The conditional probability is the joint probability of both events happening, divided by the probability of the known event.

### 📑 5.1.3 Common Probability Functions
* **Bernoulli:** Models a single event with two possible outcomes (like a coin flip);
* **Gaussian (Normal) Distribution:** Models data that clusters around a central average, creating a bell-shaped curve;
    * **1D Gaussian Formula:** $p(X=x)=\frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(x-\mu)^{2}}{2\sigma^{2}}}$;
    * *Explanation:* This equation calculates the probability of $x$. The symbol $\mu$ is the mean (average), and $\sigma$ is the standard deviation (how spread out the data is);
* **Dirac Distribution:** Concentrates all probability at one exact specific point;
    * **Formula:** $p(X=x)=\delta(x-\mu)$;
    * *Explanation:* The probability is 1 exactly at the mean $\mu$, and 0 everywhere else.

### 📑 5.1.4 Important Math Concepts
* **Expectation ($\mathbb{E}$):** The average value you expect to get from a function over many random trials;
    * **Formula for PDFs:** $\mathbb{E}_{x\sim p(x)}[f(x)]=\int_{x}f(x)p(x)dx$;
    * *Explanation:* It multiplies each possible outcome $f(x)$ by its probability $p(x)$ and adds them all up (using an integral for continuous data);
* **KL Divergence ($D_{KL}$):** A metric that measures how much a predicted probability distribution ($Q$) deviates from a true reference distribution ($P$);
    * **Formula:** $D_{KL}[P||Q]=\mathbb{E}_{\chi\sim P(\chi)}[log\frac{P(\chi)}{Q(\chi)}]$;
    * *Explanation:* It calculates the expected difference between the logarithms of the two probabilities. Note: It is not a true "distance" because it is asymmetrical (comparing P to Q is not the same as comparing Q to P).

---

## 📖 5.2 Machine Learning Fundamentals

### 📑 5.2.1 Core Definition
A computer program is said to **learn** from **Experience (E)** with respect to some **Task (T)** and **Performance Measure (P)**, if its performance at tasks in T improves with experience E.

* **Task (T):** What the model needs to do. Examples include classification (assigning categories), regression (predicting continuous numbers) or translation;
* **Experience (E):** How the model gets data;
    * *Passive:* The model is just fed data. Includes Supervised learning (data has correct answer labels) and Unsupervised learning (data has no labels);
    * *Active:* The model interacts with the world. Includes Reinforcement Learning (acting in an environment to maximize a reward);
* **Performance Measure (P):** How we score the model.

### 📑 5.2.2 The Inference Problem
The goal of machine learning is to create a mapping from an input (like raw image pixels) to a useful output (like "this is a cat"). 

* **Parametric Hypothesis Space:** A set of possible programs. Each program variation is controlled by a parameter vector ($\theta$). Changing $\theta$ changes how the program behaves;
* **Empirical Data Distribution ($\hat{p}_{data}$):** We do not have access to every piece of data in the universe. We only have a small training dataset. We build an empirical (observed) distribution from this limited training set;
* **IID Assumptions:** For learning to work, we assume training data is Independent (one sample does not affect another) and Identically Distributed (all samples come from the same real-world environment).

### 📑 5.2.3 Training the Model
* **Maximum Likelihood:** The ideal goal is to find the best parameters ($\theta^{*}$) that make the correct outputs highly probable;
    * **Formula:** $\theta^{*}=argmax_{\theta}\mathbb{E}_{x,y\sim p_{data}}[log~p_{model}(y|x;\theta)]$;
    * *Explanation:* We want to find the arguments ($\theta$) that maximize the expected log probability of the correct label $y$ given the input $x$;
* **Loss Function ($\mathcal{L}$):** A mathematical penalty. Instead of maximizing success, programs are usually built to minimize loss (like Negative Log Likelihood).;
    * **Formula:** $\theta^{*}=argmin_{\theta}\mathcal{L}(\theta)$;
    * *Explanation:* Find the parameters $\theta$ that result in the minimum possible loss $\mathcal{L}$. The training loss is also called the **Empirical Risk**.

### 📑 5.2.4 Model Capacity and Errors
* **Model Capacity:** The ability of a model to fit a wide variety of mathematical functions;
* **Underfitting:** The model capacity is too low. It cannot even learn the training data. This results in high training loss;
* **Overfitting:** The model capacity is too high. It memorizes the training data perfectly but fails on new, unseen test data. This results in low training loss but high test loss;
* **Regularization:** Techniques used to control model capacity and prevent overfitting. This introduces an **inductive bias**, which forces the model to prefer simpler explanations over complex memorization.

---

## 📖 5.3 The Path to Deep Learning

There is a massive **Abstraction Gap** between raw input data (like a grid of colored pixels) and the final concept (like identifying a dog). The input has many tangled variables like illumination, camera angle, and occlusion (objects blocking each other). 

### 📑 5.3.1 Three Generations of AI
1.  **First Generation (Hand-Designed Features):** Humans wrote rigid code to extract specific shapes (like edges or gradients);
    * *Pros:* Better than pure rule-based logic;
    * *Cons:* Very hard to design, brittle to lighting changes, and does not scale well;
2.  **Second Generation (Shallow Models):** Models with a single learned hidden layer. They started learning their own simple features from the data;
    * *Cons:* The abstraction gap to the final concept was still too large to cross in one step;
3.  **Third Generation (Deep Learning):** Models with many layers. They learn a hierarchy of features;
    * *Mechanism:* The first layer learns edges. The second layer combines edges to learn corners. The third layer combines corners to learn object parts. This process is called **End-to-End Learning**;
    * *Pros:* Achieves near-human performance. Fully scalable;
    * *Cons:* Requires massive amounts of data. Expensive to train and run.

### 📑 5.3.2 Distributed Representations
Deep learning solves complex variations by using **Distributed Representations**. Instead of creating a separate category for every possible combination of traits (e.g., red car, blue car, red bird, blue bird), it splits concepts into separate learned factors (e.g., shape features + color features). This is highly efficient.

---

## 📖 5.4 Foundation Models

### 📑 5.4.1 Definition
A **Foundation Model** is a massive machine learning model trained on a huge scale of unlabelled data from diverse sources (text, audio, images, sensors). After this initial training, the exact same model is reused and adapted for many different, specific downstream tasks.

### 📑 5.4.2 Key Properties
* **Emergence:** The model develops complex behaviors and skills that were not explicitly programmed or constrained by the creators;
    * *Advantage:* Requires much less human supervision to learn complex things;
    * *Disadvantage:* Can develop unanticipated and hidden biases;
* **Homogenization:** Using the exact same model architecture and training pipeline to solve entirely different problems across different industries;
    * *Advantage:* Greatly simplifies the engineering pipeline;
    * *Disadvantage:* Creates a single point of failure. If the foundation model has a flaw, all applications built on it inherit that flaw.

<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 6 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 6 - CNN  to Autonomous Driving**

---

## 📖 1.1 Introduction to Autonomous Driving

Quick Math Refresher & Optimization

Derivative: A value that describes how sensitive a mathematical function is to a microscopic change in its input. It represents the tangent of the slope of the function.

Partial Derivative: Similar to a regular derivative, but used for functions with multiple inputs. It measures the sensitivity of the function along just one specific input dimension.

Gradient: A mathematical vector that groups together all the partial derivatives of a function. It points in the direction where the function increases the fastest (steepest ascent).

Objective Function: A formula, such as negative log-likelihood, that a machine learning model tries to minimize.

Gradient Descent Algorithm: A method that starts with a random guess and takes steps in the direction of the negative slope to find the local minimum of an objective function.

Backpropagation Algorithm: A process used to compute the gradient. It first calculates the prediction (forward propagation) and then computes the partial derivatives backward using the recursive chain rule.

Minibatch: A small, random subset of training data. Stochastic Gradient Descent (SGD) uses minibatches to estimate the gradient because calculating the exact error over the entire dataset is too computationally expensive. Larger minibatches increase gradient accuracy and parallelism, but they consume more memory and decrease the regularization effect.

Regularization: Techniques used to prevent a model from simply memorizing data. Examples include early stopping, data augmentation (mirroring, rotating, or scaling images), weight decay, and dropout.

Precursors: Multi-Layer Perceptrons (MLPs)

Multi-Layer Perceptron (MLP): An early network design composed of Fully Connected (FC) layers.



Shutterstock

Esplora

Fully Connected (FC) Layer: A layer where every input element connects to every output element. It processes data in two stages:

Linear Projection Stage: Multiplies the input feature vector by learned parameters (weights) to create a new linear combination.

Detector Stage: Applies a non-linear mathematical function to decide if a matched pattern is strong enough. A common detector is the Rectified Linear Unit (ReLU), defined as $y=max(0,x)$. Other functions include the logistic and softplus functions.

Limitations of MLPs: They do not exploit the spatial structure of images and require a massive number of parameters. For example, a 256 by 256 image requires 1 million parameters in a single FC layer, which easily leads to overfitting.

Convolutional Layers

Convolutional Neural Networks (CNNs): Networks designed to scan for small, local patterns and successively group them into larger, more abstract patterns.

Convolution Stage: Replaces fully connected topology by exploiting the grid-like structure of images. It uses a Kernel (or filter), which is a small matrix of weights, and slides it over the input data. At each position, it calculates the sum of element-wise multiplications.

This approach massively reduces the number of parameters compared to FC layers and makes the network equivariant to spatial translation (shifting).

Meta-Parameters of Convolution:

Stride: Controls the step size when sliding the kernel along the horizontal or vertical axes. A larger stride reduces the output size and computational complexity.

Padding: The addition of zeros around the borders of the input matrix. This prevents the outer edges of the data from being lost and keeps the input-to-output size ratio consistent.

The Pooling Stage

Pooling Layer: A layer that slides a window over the data and extracts a single summary statistic from the neighboring features.

The primary goals of pooling are to add invariance to small translations (shifts) in the input and to downsample the signal.

Max Pooling: The most common pooling statistic, which acts as a "winner takes all" mechanism by only keeping the highest value in the window. Average pooling is an alternative that smooths out detection noise.

Output Layers

Output Layer: A final transformation layer required because raw network outputs cannot always represent valid probability functions. It restricts the output to a parametric family of Probability Mass Functions (PMF) or Probability Density Functions (PDF).

Sigmoid Output Layer: Used for binary classification (two outcomes). It outputs a single scalar probability constrained between 0 and 1.

Softmax Output Layer: Used for generic classification (multiple outcomes). It forces a vector of raw scores into a list of probabilities where all values fall between 0 and 1, and their total sum exactly equals 1.

Regression: For continuous number prediction, the network can output parameters like the mean without needing a specialized PMF output layer. This minimizes the Euclidean distance between predictions and ground truth, known as Ordinary Least Squares.

Batch Normalization

Batch Normalization Layer: A layer introduced to solve the problem of uneven activation scales, which causes different sensitivities for different parameters during training.

It computes the mean and variance for each feature over the current minibatch. It then normalizes the data by subtracting the mean and dividing by the variance, keeping the data uniformly scaled.

<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 7 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 7 - Image Classification and Object Detection**

---

## 📖 7.1 Neural Network Basics
A neural network is a computer system inspired by the human brain. It uses math to find patterns in data.

* **Fully Connected Layer**: A layer where every artificial neuron connects to all neurons in the next layer;
* **Convolution Layer**: A layer that acts like a sliding filter to find visual features like edges or textures;
* **Max-Pooling Layer**: A layer that shrinks the image size to save memory and keep the most important details;
* **Non-linearities (Activation Functions)**: Math rules that help the network learn complex patterns;
    * **Logistic (Sigmoid)**: Squeezes numbers between 0 and 1. Formula: $y=\frac{1}{1+e^{-x}}$;
    * **ReLU (Rectified Linear Unit)**: Changes all negative numbers to zero. Formula: $y=max(0,x)$;
* **Optimization**: The process of minimizing mistakes;
    * **Backpropagation**: A method to trace errors backward through the network to update it.

---

## 📖 7.2 Image Classification
Image classification is the task of assigning a specific label to an entire picture.

* **Input**: A single image.
* **Output**: A list of probabilities for each possible category;
* **How it works**: Models like AlexNet and VGG use two main parts;
    1.  **Feature Extractor**: Finds abstract local patterns in the image;
    2.  **Decision Layers**: Looks at the whole picture to make the final guess;
* **Cross Entropy**: A math formula used during training to measure how wrong the network's guess is. Formula: $\Delta(y,\hat{y})=-\sum_{c}y_{c}log(\hat{y}_{c})$.

---

## 📖 7.3 Semi-Supervised Image Classification
Labeling thousands of images by hand is very expensive. Semi-supervised learning uses a few labeled images and many unlabeled images to train the model.

This method requires an **inductive bias**. An inductive bias is a built-in assumption about the data. Common methods include:
* **Feature Local Consistency**: Adding random noise to an image should not change the network's guess.
* **Parameter Local Consistency**: The network's internal math weights should change smoothly during training.
* **Global Consistency**: Images that look similar should get the same label.
* **Pseudo Labeling**: If the network is very confident about an unlabeled image, we trust that guess and use it as a true label.

---

## 📖 7.4 Object Detection
Object detection finds specific items in an image and draws a tight box around them.

* **Bounding Box**: The smallest straight rectangle that completely covers an object.

### 📑 7.4.1 Two-Stage Detectors (e.g., R-CNN)
These models find objects in two distinct steps.
* **Stage 1 (Proposal Generation)**: The model guesses many possible locations (boxes) where an object might be;
* **Stage 2 (Classification)**: The model crops those boxes, resizes them, and checks what is inside;
* **Bounding Box Regression**: The model uses math to slightly move and resize the box to fit the object perfectly;
* **Non-Maximum Suppression (NMS)**: A cleanup step. It deletes extra boxes that overlap the same object. NMS uses a metric called **Intersection over Union (IoU)** to measure overlap. Formula: $iou(B_{1},B_{2})=\frac{|B_{1}\cap B_{2}|}{|B_{1}\cup B_{2}|}$;
* **Pros/Cons**: They are simple to understand but slow and expensive to run because they check so many boxes.

### 📑 7.4.2 One-Stage Detectors (e.g., YOLO, SSD)
These models detect all objects by looking at the image only once.
* **Fully Convolutional Network (FCN)**: A network that only uses sliding filters (convolutions) and pooling. It does not use flat (fully connected) layers;
* **Sliding Window**: The FCN acts like a small window sliding across the entire image to find objects instantly;
* **Receptive Field**: The specific patch of pixels in the original image that a single artificial neuron is looking at;
* **Anchors**: Pre-defined prototype boxes with different shapes (like tall or wide rectangles). Because objects come in many shapes, the network uses these anchors as starting points. It then adjusts the best-fitting anchor instead of building a box from scratch.

<!-- ------------------------------------------------------------------ -->
<!-- --- COURSE 8 Image Segmentation and Monocular Depth Estimation --- -->
<!-- ------------------------------------------------------------------ -->

# 🔖 **Course 8 - Image Segmentation and Monocular Depth Estimation**

---

## 📖 8.1 Deep Learning Foundations (Recap)

Before discussing advanced concepts, it is important to understand the building blocks of neural networks:
* **Fully Connected Layer**: A layer where every artificial neuron is connected to every neuron in the subsequent layer;
* **Convolution Layer**: A layer that uses small grids (filters or kernels) that slide across an image to detect local features, such as edges or textures;
* **Max-Pooling Layer**: A technique to shrink the size of an image (down-sampling). It works by sliding a window over the data and only keeping the maximum value within that window;
* **Non-Linearities**: Mathematical functions applied to a neuron's output. Without them, a network could only learn straight lines;
    * **Logistic (Sigmoid)**: Squeezes output values into a range between 0 and 1;
        $$y = \frac{1}{1+e^{-x}}$$
    * **ReLU (Rectified Linear Unit)**: Replaces any negative number with zero, but leaves positive numbers completely unchanged. This is fast and highly effective;
        $$y = \max(0,x)$$
* **Fully Convolutional Networks (FCNs)**: Networks that replace fully connected layers with convolutional layers. FCNs act like a "sliding window," allowing them to process input images of any size.

---

## 📖 8.2 Image Segmentation

Image segmentation is the process of grouping pixels in an image into meaningful categories. It distinguishes between **"things"** (countable, distinct objects like cars or people) and **"stuff"** (shapeless textures or materials like sky, grass, or roads).

### 📑 8.1.1 Problem Definitions
* **Semantic Segmentation**: Classifies every pixel into a general category (e.g., "car" or "road"). It does *not* separate individual objects. If two cars overlap, they are merged into one giant "car" region;
* **Instance-Level Segmentation**: Focuses only on "things." It detects individual objects and separates them by giving each a unique mask (e.g., Car 1, Car 2);
* **Panoptic Segmentation**: The ultimate combination. It classifies the "stuff" pixels (like sky) and also identifies and uniquely labels each individual "thing" (like Car 1, Car 2).

### 📑 8.1.2 Approaches to Semantic Segmentation
Semantic segmentation models usually fall into two categories:

**A. Two-Stage Approach (Region Classification)**
1.  **Proposal Stage**: The network guesses potential locations of objects;
2.  **Classification Stage**: The network determines what class each region belongs to;
3.  **Tiling Stage**: The regions are stitched together to form the final pixel map.

**B. One-Stage Approach (Sliding Window Classifier)**
A standard Convolutional Neural Network (CNN) is converted into an FCN to classify pixels in a single pass. However, because networks use pooling (which shrinks the image), the output is a blurry, coarse segmentation. 

Several ideas exist to fix this resolution problem:
1.  **Remove Strides**: Stop the network from shrinking the image;
    * *Disadvantage*: This is computationally expensive and heavily reduces the network's context (its "receptive field");
2.  **Shift-and-Stitch**: Shift the input image by one pixel multiple times, pass them all through the network, and weave the results together;
    * *Solution*: This can be optimized using **Dilated Convolutions**;
    * *Dilated Convolution*: A layer that expands the filter by inserting zeros between its values. It increases the network's field of view without increasing the number of learned parameters;
        $$y_{j,x,y}=\sum_{i=1}^{D_{in}}\sum_{\Delta y=1}^{H_{K}}\sum_{\Delta x=1}^{W_{K}}w_{j,i,\Delta x,\Delta y}\cdot x_{i,x+(\Delta x-1)\cdot r,\ y+(\Delta y-1)\cdot r}$$
        *(Where $r$ is the dilation rate. Regular convolution is just $r=1$)*;
    * *Disadvantage*: Still computationally demanding;
3.  **Interpolate Output**: Simply guess the missing pixels by blending neighboring values (bilinear upsampling);
4.  **Encoder-Decoder**: Shrink the image to learn the deep abstract meaning (Encoder), and then artificially expand it back to its original size (Decoder);
    * *Transposed Convolution*: A layer that actively *learns* how to expand (up-sample) an image. It broadcasts a single input pixel to multiple output pixels by multiplying it with a filter;
5.  **Encoder-Decoder with Skip Connections**: When the encoder shrinks an image, it forgets exactly *where* the objects were. Skip connections fix this by directly wiring high-resolution, low-level details from the early layers straight to the final expanding layers. This fuses "what" the object is with "where" the object is.;
    * **SegNet**: Remembers the exact grid indices during max-pooling and reuses them;
    * **U-Net**: Copies entire feature maps from the encoder and concatenates them with the decoder.

---

## 📖 8.3 Monocular Depth Estimation

**Problem Statement**: Estimating a dense, 3D depth map using only a single, 2D RGB image. 

This is fundamentally an "ill-posed" problem, meaning a single 2D image does not contain enough geometric information to mathematically calculate exact 3D depth. The model must rely on context and assumptions.

### 📑 8.3.1 Network Priors (Biases)
Humans use lighting and symmetry to guess distance. Neural networks, however, learn counter-intuitive priors. They strongly rely on the shadow underneath an object or the point where the object touches the ground to estimate distance. They struggle to inherently understand an object's true size.

### 📑 8.3.2 Architectures and Loss
* **Coarse-to-fine Architecture**: A dual-network setup. A "coarse" network evaluates the whole image to understand the global perspective, and a "fine" network refines the local details;
* **Scale-Invariant Loss**: Because the network only sees a flat image, it might guess the relative layout of a room perfectly but get the absolute meters entirely wrong. The scale-invariant loss prevents the network from being penalized if all depth predictions are off by the exact same multiplier;
    $$D(y,y^{*})=\frac{1}{2n}\sum_{i=1}^{n}(\log y_{i}-\log y_{i}^{*}+\alpha(y,y^{*}))^{2}$$
    *(Where $y$ is the predicted depth, $y^*$ is the true depth, and $\alpha$ computes the constant scale difference to cancel it out).*

### 📑 8.3.3 Self-Supervised Learning for Depth
Finding perfect ground truth depth data is difficult. LiDAR (laser sensors) is sparse, and stereo cameras are inaccurate. Instead, engineers use **Self-Supervised Learning**.
1. The network looks at the left camera image and guesses the depth;
2. It uses that depth guess to mathematically warp the left image to simulate what the right camera should be seeing;
3. It compares its fake warped image against the real right camera image;
4. The error is measured using **SSIM (Structured Similarity Index Measure)**, which judges how perceptually similar two images are based on average intensity and contrast.
    $$SSIM(x_{1},x_{2})=\frac{(2\mu_{x}\mu_{y}+c_{1})(2\sigma_{xy}+c_{2})}{(\mu_{x}^{2}+\mu_{y}^{2}+c_{1})(\sigma_{x}^{2}+\sigma_{y}^{2}+c_{1})}$$
    *(Where $\mu$ is mean intensity, $\sigma$ is standard deviation, and $c_1, c_2$ are constants).*

---

## 📖 8.4 Birds-Eye View (BEV) Representations

**Motivation**: Instead of processing the world from the perspective of a dashboard camera, we can transform all camera data into a top-down, "drone-like" perspective known as the Birds-Eye View (BEV). This makes 3D object detection and car trajectory planning significantly easier.

### 📑 8.4.1 Main Approaches
* **Lift-Splat-Shoot (LSS)**:
    1.  **Lift**: The network extracts features from every camera and predicts their depth. It then projects these features out into 3D space like a cone (frustum);
    2.  **Splat**: The 3D features from all surrounding cameras are pooled and flattened down onto a single 2D grid centered on the vehicle;
    3.  **Shoot**: The autonomous system plots driving paths across this unified top-down map and evaluates their safety;
* **Transformer-Based Approach**: Instead of mathematically projecting features into 3D space, this uses Attention mechanisms. For every grid square in the BEV map, the network "queries" (searches) all cameras to see if they contain visual evidence of an object belonging in that specific square.

---

## 📖 8.5 Brief Overview: Self-Supervised Learning (SSL)

Autonomous Driving (AD) systems require massive amounts of data. Manually labeling this data is extremely slow and expensive. Self-Supervised Learning (SSL) solves this by teaching the network to understand environments using raw, unlabeled data like camera feeds or LiDAR (laser scans).

* **Reconstruction Methods**: The network hides (masks) part of an image and learns by trying to accurately guess the missing pieces;
* **Distillation Methods**: A smaller, faster "student" network learns by copying the outputs of a larger, highly accurate "teacher" network;
* **World Models**: The system looks at a sequence of past events to predict future states. For example, it estimates future vehicle movement (ego-motion) based on previous frames;
* **AD-L-JEPA**: A modern architecture designed specifically for self-driving. It hides regions of a 3D point cloud. Instead of predicting the exact missing laser points, it predicts the general abstract meaning of the missing region.

---

## 📖 8.6 Deep Dive: UniPAD Architecture

**UniPAD** is an advanced learning framework for autonomous driving. It learns by projecting flat 2D images into 3D space and practicing how to draw (render) the scenes. The lecture breaks this system down into three steps:

**Step 1: The Basic Auto-Encoder**
1.  **Masking**: The system covers up large sections of an input camera image;
2.  **Lifting to 3D**: It takes the remaining visible pieces and mathematically projects them into a 3D grid (a volumetric representation);
3.  **Rendering**: It shoots imaginary light rays through this 3D grid to recreate the missing parts of the 2D image;
4.  **Learning**: It compares its recreation to the real image. The difference (Reconstruction Loss) is used to update the network so it improves over time.

**Step 2: Adding Sensor Supervision**
Learning depth from standard images alone is difficult. In this step, exact ground-truth distance measurements from LiDAR and RADAR are added. This teaches the system exactly how far away objects actually are, grounding the 3D projections in reality.

**Step 3: Knowledge Transfer (Teaching the Camera)**
LiDAR and RADAR capture excellent 3D shapes, but cameras are cheaper and capture rich color. In this final step, the system uses the high-quality 3D laser data as a "teacher." A mathematical penalty called a "Knowledge Transfer Loss" forces the camera-only system to mimic the exact 3D understanding of the laser system. This effectively teaches the regular camera to "see" in 3D.

---

## 📖 8.7 Conclusions and Key Design Principles

Deep Learning has completely revolutionized Computer Vision. Building successful models relies on several key empirical principles:

* **Map to Known Tasks**: Always frame the problem as a standard machine learning task. Use classification for discrete labels or regression for predicting continuous numbers;
* **Check the Receptive Field**: Ensure the network can "see" enough of the image at once to understand the context;
* **Optimize Parameters**: Reduce the size and depth of data before applying heavy mathematical operations (like $3\times3$ convolutions). This keeps the model efficient;
* **Simplify the Problem**: Break complex tasks into smaller sub-problems. 

**The Future of Computer Vision**:
* **Neural Architecture Search (NAS)**: Instead of humans designing network layers by hand, algorithms will automatically test and find the best structural designs;
* **Explainable AI**: It is becoming critical to understand *why* a network makes a specific decision and exactly which pixels caused that decision;
* **Beyond Convolutions**: Standard Convolutional Neural Networks (CNNs) might not be the final answer. New frameworks, especially **Transformers** (which use "attention" mechanisms to focus heavily on specific important regions), are currently taking over as the state-of-the-art.

<!-- --------------------------------------------------------------- -->
<!-- --------- COURSE 9 Transformers and Visual Attention ---------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 9 - Transformers and Visual Attention**

---

## 📖 9.1 Neural Machine Translation (NMT) & The Attention Mechanism
* **The Problem with RNNs:** Traditional Encoder-Decoder architectures rely on Recurrent Neural Networks (RNNs), such as LSTMs, to compress a variable-length input sentence into a fixed-length final state. This creates an **information bottleneck** where the model fails to retain necessary context in long sequences.
* **The Solution (Attention):** Instead of a single fixed state, the encoder creates a variable-length representation using Bidirectional RNNs. At each step of translation, the decoder "queries" the encoder to generate a specific context vector relevant to the next predicted word.
* **Pre-Transformer Attention Types:**
    * **Additive Attention (Bahdanau):** Uses a feed-forward network (FFN) to combine query and key states. It is effective but computationally inefficient.
    * **Dot Product Attention (Luong):** Computes similarity via a simple dot product between the query and the key, requiring them to be of equal length.

---

## 📖 9.2 "Attention Is All You Need" (The Transformer)
* **Core Concept:** The Transformer architecture removes RNNs entirely, replacing them with **Multi-Head Self-Attention**;
* **Advantages over RNNs:**
    * **Scalability:** Eliminates the sequential processing path ($O(T)$), allowing for highly parallel computation across all tokens;
    * **No Position Bias:** RNNs tend to over-value the most recently seen information; Transformers model global dependencies equally across the sequence;
* **Scaled Dot-Product Attention:**
    * **Formula:** $$Attention(Q,K,V)=softmax(\frac{QK^{T}}{\sqrt{d_{k}}})V$$ 
    * **Explanation:** The model compares a Query matrix ($Q$) against Key matrices ($K^{T}$) using dot products to find sequence alignments. It scales the result by $\frac{1}{\sqrt{d_{k}}}$ (where $d_{k}$ is the dimension size) to prevent the softmax function from saturating. The resulting normalized weights are multiplied by the Value matrix ($V$) to form the output context;
* **Multi-Head Attention:** Instead of one single attention pass, the model projects $Q$, $K$, and $V$ into multiple different representation spaces ("heads"). This allows the model to simultaneously attend to different types of contextual relationships in parallel;
* **Positional Embeddings:** Because the model lacks recurrence, it has no inherent sense of word order. Constant, position-dependent vectors (often derived from sine and cosine functions) are added to the input word embeddings so the model can recognize relative sequence order;
* **Architecture Components:** The network relies heavily on Skip Connections, Layer Normalization (to aid rapid convergence), and FFNs (to lift token features and increase representational power). The decoder employs **masking** to prevent tokens from "looking ahead" at future words during the training phase.

---

## 📖 9.3 Object Detection with Transformers (DETR)
* **Direct Set Prediction:** DETR (Detection Transformer) shifts object detection from a heuristic-heavy task to a direct set prediction problem. It outputs a fixed number of predictions natively, consisting of bounding boxes and class labels (including $\emptyset$ for a special "no object" class);
* **Elimination of NMS:** Traditional CNN architectures (like Faster R-CNN) rely on Non-Maximum Suppression (NMS) to manually filter out overlapping anchor boxes. DETR bypasses this by generating distinct, non-overlapping predictions through its global attention mechanism;
* **Bipartite Matching Loss (Hungarian Loss):**
    * **Formula:** $$\mathcal{L}_{Hungarian}=\sum_{i=1}^{n}-log\hat{p}_{\sigma_{i}}(c_{i})+[[c_{i}\ne\emptyset]]\cdot\mathcal{L}_{bbox}(b_{i},\hat{b}_{\sigma_{i}})$$ 
    * **Process:** Instead of matching predictions to predefined anchors, DETR uses the Hungarian algorithm to find the optimal one-to-one matching ($\sigma$) between ground truth objects and model predictions. It penalizes classification errors for all outputs, but only computes bounding box errors for predictions matched to actual ground truth objects;
* **Bounding Box Loss & GIoU:**
    * **Formula:** $$\mathcal{L}_{iou}(b,\hat{b})=1-(\frac{|b\cap\hat{b}|}{|b\cup\hat{b}|}-\frac{|B(b,\hat{b})\backslash b\cup\hat{b}|}{|B(b,\hat{b})|})$$ 
    * **Explanation:** The bounding box loss is a linear combination of standard L1 loss and Generalized Intersection over Union (GIoU). Standard IoU yields a zero gradient if two boxes do not overlap at all, which halts learning. GIoU solves this by factoring in $B(b,\hat{b})$, representing the smallest bounding box that completely encloses both the prediction and the ground truth box;
* **DETR Architecture Overview:**
    1.  **Backbone:** A standard CNN extracts a robust set of 2D image features;
    2.  **Transformer Encoder:** Flattens the CNN feature map into a 1D sequence for processing via self-attention;
    3.  **Transformer Decoder:** Takes a fixed number of learned "object queries" (positional embeddings) and attends to the encoder's output in parallel. These queries learn to intrinsically focus on different geometric and semantic regions of an image;
    4.  **Prediction Heads:** Independent FFNs compute the final class assignment and bounding box coordinates for every query;
* **Results & Efficacy:** DETR performs competitively with established models like Faster R-CNN. It excels at detecting large objects due to the global attention mechanism but struggles slightly with small objects. As the transformer decoder becomes deeper (exceeding 3 layers), post-processing with NMS becomes actively unnecessary and can even degrade performance by suppressing valid overlaps.

<!-- --------------------------------------------------------------- -->
<!-- ------- COURSE 10 Radar-Based Driver Assistance Systems ------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 10 - Radar-Based Driver Assistance Systems**

---

## 📖 10.1 Introduction to Driver Assistance Systems (DAS)
Driver Assistance Systems (DAS) aim to improve safety and driving comfort by supporting the driver, especially in critical situations. The ultimate goal is accident-free driving.

* **Process:**
    * **Sensors:** Survey the surroundings and interior of the vehicle.
    * **Control Units:** Monitor and analyze sensor data in real time.
    * **Sensor Fusion:** Combines data from multiple sensors to validate information for reliable support.

---

## 📖 10.2 Radar Basics
Radar is a fundamental technology used to measure the environment for DAS.

### 📑 10.2.1 Measurement Variables
Radar systems typically utilize a **polar coordinate system** $(r, \theta)$, where $r$ is the range and $\theta$ is the azimuth (angle). This is equivalent to a Cartesian coordinate system $(x, y)$.

* **Key Measurements:** Range, Azimuth, and Radial Velocity.
* **Limitation:** Radar only measures the **radial velocity** (the component of velocity directly toward or away from the sensor). It cannot directly reconstruct or measure the full two-dimensional velocity vector in a Cartesian system.

### 📑 10.2.2 Distance Measurement Principle
Radar measures the time ($t_d$) elapsed between sending a pulse and receiving the echo.
* **Formula:** $D = t_d \times \frac{c}{2}$
    * Where $D$ is the distance, $t_d$ is the time delay, and $c$ is the speed of light.

### 📑 10.2.3 Radial Velocity Measurement Principle
Radar detects the frequency shift between the transmitted and received signals to determine the speed of a target.
* **Formula:** $f_d = \frac{2v_r f_{tx}}{c}$
    * $f_d$: Frequency difference (Doppler shift);
    * $v_r$: Radial speed of the target;
    * $f_{tx}$: Transmitted frequency;
    * $c$: Speed of light.

### 📑 10.2.4 Frequency-Modulated Continuous-Wave (FMCW) Principle
FMCW radar allows for more advanced measurement.
* **Formula:** $f_d = \frac{2D}{c} \cdot \frac{\Delta f}{\Delta t} + \frac{2v_r}{\lambda_{tx}}$ 
    * This formula combines distance ($D$) and radial velocity ($v_r$) measurements;
    * Using three frequency ramps enables the system to handle **multi-target scenarios**;
    * Using four ramps allows for the efficient **suppression of ghost targets**;

---

## 📖 10.3 Sensor Data Fusion
Fusion combines data from various sources to create a complete and accurate picture of the environment.

* **Architecture Components:**
    1.  **Data Fusion:** Integrating raw inputs;
    2.  **Environment Model:** Creating a unified map;
    3.  **Situation Interpretation:** Analyzing what is happening;
* **Inputs:**
    * **Camera:** Detects lane markings and classifies objects;
    * **Radar:** Detects moving and stationary objects;
    * **Digital Map/Navigation:** Provides context on the roadway.

---

## 📖 10.4 Key Use Cases and Functionalities

### 📑 10.4.1 Adaptive Cruise Control (ACC)
Maintains a secure distance to the vehicle ahead while keeping a set speed.
* **Inputs:** Radar data, video data, and ego vehicle data (own car data);
* **Reaction:** Automatic longitudinal control (acceleration or deceleration);
* **Target Logic:** The system tracks stationary objects (e.g., guardrails) and uses video lane detection to maintain the correct target vehicle in a curve;

### 📑 10.4.2 Predictive Emergency Braking & Pedestrian Protection
Systems designed to act faster than a human to avoid or mitigate collisions.
* **Inputs:** Ego motion, object classification (pedestrian, cyclist), motion models, and time-to-collision (TTC) calculations;
* **Driver Monitoring:** Estimates the driver's level of attention (e.g., intention to brake or evade);
* **Reaction:** Collision avoidance or mitigation through automatic braking or steering;

---

## 📖 10.5 System Approach Summary
1.  **Sensory Information:** Raw data from radar, video, ultrasonic sensors, and ego vehicle sensors;
2.  **Signal Processing:** Initial calculation of objects and environment data;
3.  **Environmental Hypothesis:** Creating an understanding of the environment, such as object-lane association and parallel lanes;
4.  **Situation Analysis:** Assessing the criticality of the situation and driver activity;
5.  **Decision:** Executing warnings, partial braking, or full emergency braking.

<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 1 Sensor Fusion -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 11 - Sensor Fusion**

---

## 📖 11.1 Introduction to Data Fusion
Data fusion is utilized because individual sensors inherently possess measurement errors and operational limitations. 

* **Sensor Uncertainty:** All sensors have intrinsic errors; for example, a GPS receiver may provide position data with an accuracy of approximately 3 meters;
* **Sensor Drawbacks:** Sensors may fail under specific conditions. GPS signals, for instance, are weak or unavailable in tunnels. Inertial Measurement Units (IMUs) accumulate errors over time due to the integration process required to calculate position;
* **Methodological Limitations:** Theoretical models often fail to account for real-world process variations, such as mechanical issues.

### 📑 11.1.1 The Data Fusion Process
Data fusion improves estimation by combining measurements from different sources using a **weighted average**.
* **Weight Assignment:** Weights are assigned based on the reliability of the sensor data, with greater weight given to more accurate, less uncertain data;
* **Logic Example:** If GPS signal quality is high, the system trusts the GPS for position. If the GPS signal is weak (e.g., inside a tunnel), the system relies on predictive data from other sensors like the IMU.

---

## 📖 11.2 Preliminary Statistical Notions
Understanding data fusion requires foundational knowledge of probability and statistics.

* **Random Variable ($X$):** A function that maps a random event to a numerical value;
* **Expected Value ($E[X]$):** The weighted average of all possible values, representing the expected outcome;
    $$E[X] = \frac{\sum_{i=1}^{N} x_i}{N}$$ 
* **Variance ($Var(X)$):** Measures the spread of data points around the mean, representing how far values deviate from the average;
    $$Var(X) = E[(\bar{x} - X)^2] = \frac{\sum_{i=1}^{N} (\bar{x} - x_i)^2}{N}$$ 
* **Standard Deviation ($\sigma$):** The square root of variance; it provides a measure of dispersion in the same units as the original data;
    $$\sigma(X) = \sqrt{Var(X)}$$ 
* **Covariance ($Cov(X, Y)$):** Expresses the linear dependency between two different dimensions or variables;
    $$Cov(X, Y) = E[(\bar{x} - X)(\bar{y} - Y)] = \frac{\sum_{i=1}^{N} \sum_{j=1}^{M} (\bar{x} - x_i)(\bar{y} - y_i)}{N + M}$$ 
* **Gaussian (Normal) Distribution:** A continuous probability distribution characterized by the probability density function;
    $$f(x | \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$ 
* **White Noise:** Random signal distortion with a mean of zero, often modeled as a Gaussian distribution centered at 0 with a specific variance.

---

## 📖 11.3 State Observers
A state observer estimates the internal state ($x_t$) of a system that may not be directly measurable, relying instead on system inputs ($u_t$) and outputs ($y_t$).

* **System Model:**
    * State update: $x_{t+1} = A_t x_t + B_t u_t$
    * Output measurement: $y_t = H_t x_t$
* **Optimal State Estimation:** By incorporating feedback via a **Gain ($L_t$)**, the observer corrects the model's estimate based on the difference between the actual output and the predicted output:
    $$\hat{x}_{t+1} = A_t \hat{x}_t + B_t u_t + L_t(y_t - \hat{y}_t)$$ 

---

## 📖 11.4 Kalman Filter
The Kalman Filter is an optimal state estimator for stochastic systems, explicitly handling process noise ($w_t$) and measurement noise ($v_t$).

### 📑 11.4.1 Assumptions
* Both $w_t$ and $v_t$ are uncorrelated white noises;
* $v_t \sim N(0, R_t)$, where $R_t$ is measurement noise covariance;
* $w_t \sim N(0, Q_t)$, where $Q_t$ is process noise covariance.

### 📑 11.4.2 The Algorithm
The filter operates in two repeating steps:

1.  **Prediction:** Projects the current state and error covariance forward.
    * $\hat{x}_t^- = A \hat{x}_{t-1} + B u_{t-1}$
    * $P_t^- = A P_{t-1} A^T + Q_t$
2.  **Update:** Adjusts the projection using new measurement data.
    * $K_t = \frac{P_t^- H^T}{H P_t^- H^T + R_t}$ (Kalman Gain)
    * $\hat{x}_t = \hat{x}_t^- + K_t(y_t - H \hat{x}_t^-)$
    * $P_t = (I - K_t H) P_t^-$

### 📑 11.4.3 Drawback
The standard Kalman Filter assumes the system model is linear. Nonlinearities cause the Gaussian distribution of the state estimate to become distorted.

---

## 📖 11.5 Extended Kalman Filter (EKF)
The EKF is designed for nonlinear systems by linearizing the model at each time step using Taylor approximation.

* **Linearization:** Uses the Jacobian matrix to approximate nonlinear functions $f$ and $g$;
    * $F_K = \frac{\partial f}{\partial x}$ evaluated at the current state estimate;
    * $G_K = \frac{\partial g}{\partial x}$ evaluated at the current state estimate;
* **Modified Algorithm:** Follows the same prediction/update logic as the standard Kalman Filter but recomputes Jacobians at every step.

### 📑 11.5.1 Advantages and Disadvantages
* **Advantages:** Enables estimation in complex, nonlinear real-world environments;
* **Disadvantages:** * High computational cost due to Jacobian calculation;
    * Analytic computation of Jacobians can be difficult;
    * If nonlinearities are severe, the first-order Taylor approximation becomes inaccurate, making the EKF suboptimal.

<!-- --------------------------------------------------------------- -->
<!-- ---------- COURSE 12 Connectivity and Data Analysis ----------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 12 - Connectivity and Data Analysis**

---

## 📖 12.1 Overview
Modern mobility relies on "connected cars" that communicate with various entities to improve safety, efficiency, and the user experience.

### 📑 12.1.1 Communication Ecosystem
A car should communicate with the following:
* **V2V (Vehicle-to-Vehicle):** Direct communication between cars;
* **V2I (Vehicle-to-Infrastructure):** Communication between the car and road infrastructure (e.g., traffic lights, road sensors);
* **V2N (Vehicle-to-Network):** Communication with cellular networks or the cloud;
* **V2P (Vehicle-to-Pedestrian):** Communication with devices carried by pedestrians;
* **V2E (Vehicle-to-Everything):** Comprehensive connectivity encompassing all previously mentioned domains.

### 📑 12.1.2 Benefits of Connected Cars
* Improved driving safety and autonomous drive support;
* Enhanced in-car experience and advanced navigation;
* Environmental benefits (emissions reduction) and efficiency (saving time and money).

---

## 📖 12.2 Technology and Communication
Connectivity relies on various protocols, each with specific trade-offs regarding cost, power, and reliability.

| Protocol | Pros | Cons |
| :--- | :--- | :--- |
| **Satellite** | Available globally with line-of-sight | Extremely expensive |
| **Mobile (3G/4G/5G)** | Stable, universal compatibility | High cost, high power usage, no direct V2V |
| **LPWA** | Stable, wide area, low energy | Requires new infrastructure |
| **WiFi** | Affordable, universal | High power, unstable/inconsistent |
| **Bluetooth** | Widely established | Inconsistent, security issues |
| **NFC** | Simple setup, encrypted | Very short range |

### 📑 12.2.1 Server-Side Architecture
To handle large-scale data from connected vehicles, systems must prioritize:
* **High Availability:** Utilizing standby systems and multi-master configurations (Tools: `keepalived`, `ha-proxy`, `Kubernetes`);
* **Scalability:** Vertical (larger hardware) or horizontal (more nodes) scaling;
* **Asynchronous Processing:** Using message queues (e.g., `Kafka`, `RabbitMQ`) to handle data peaks;
* **Distributed Systems:** Utilizing multiple nodes and geo-locations, managed via `DNS` and `DDNS`.

---

## 📖 12.3 Data Analysis and Pipelines
Data from the car is constantly sent to the cloud, processed, and utilized for fleet monitoring, reporting, and real-time mapping.

### 📑 12.3.1 Data Management Challenges
* **Big Data Management:** Process data as close to the source as possible using techniques like **MapReduce** (Tools: `Hadoop`, `Spark`);
* **Data Integrity:** Ensuring data remains unchanged during transfer, often verified via hashing algorithms like `MD5` or `SHA-1`;
* **Security:** Implementing secure zones (`DMZ`) and handling OTA (Over-the-Air) updates.

### 📑 12.3.2 Data Processing Pipelines
Data pipelines transform raw data into usable information through a series of operators:
1.  **Input Operator:** Reads raw data;
2.  **Processing Operator:** Transforms or analyzes data;
3.  **Output Operator:** Writes data to the destination.

### 📑 12.3.3 Data Delivery Semantics
When sending data through pipelines, different delivery guarantees can be achieved:
* **At most once:** Data might be lost but is never duplicated;
* **At least once:** Data is never lost but might be duplicated;
* **Exactly once:** The ideal but complex state, requiring state management (e.g., a `STATE Database` to track progress and prevent duplicate processing).

### 📑 12.3.4 Data Hierarchy
Data follows a progression from raw input to final presentation:
1.  **RAW Data:** Unprocessed information directly from sensors;
2.  **Meta Data:** Information describing the raw data;
3.  **Semantic Data:** Data with context or meaning applied;
4.  **Indexing:** Organizing data for fast retrieval;
5.  **Presentation:** The final format for user interaction (e.g., reports, dashboards).

---

## 📖 12.4 Use Cases
* **Connected Horizon:** Predictive assistance and energy management that adjust vehicle behavior based on road conditions ahead;
* **Community-Based Parking:** Cars share parking data with the cloud to reduce search time, fuel costs and stress;
* **Connected Workshop:** Vehicles automatically transmit diagnostic codes, tire pressure, battery health and wheel alignment data to service centers, increasing customer retention and satisfaction;
* **Autonomous Driving Levels:** Support for SAE levels 2–4, including highway pilots, traffic jam pilots and automated valet parking.

