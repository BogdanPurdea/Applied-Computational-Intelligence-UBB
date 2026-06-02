<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 1 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 1 - Artificial Intelligence-Based Perception in Self-Driving Vehicles**

---

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

---

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

---

## 📖 1.3 Key Takeaways
* **Hardware & Software**: Self-driving relies on advanced computers, computer vision, and machine learning;
* **No Free Lunch Theorem**: Even with massive amounts of data, an AI cannot learn without built-in assumptions (inductive bias);
* **The Future**: The industry is slowly moving past just analyzing sensor data. The ultimate goal is **end-to-end driving**, where a single AI takes in camera video and directly outputs steering wheel and pedal commands;
* **Industry & Academia**: Solving these massive open problems requires schools and companies to work closely together.

<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 2 VIDEO SENSORS -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 2 - Video Sensors**

---

## 📖 2.1 Introduction to Video Sensors

Automated driving relies on a combination of different sensor technologies. These components include video cameras, radar systems, ultrasonic sensors, and electric power steering. A central processing unit collects data from these sensors. Software engineering ties all these systems together.

The engineering teams develop software for both mono (single) and stereo (dual) video systems. They build computer vision algorithms, which allow computers to understand digital images. They also develop machine learning algorithms for automated driving and driver assistance.

Specific examples of these algorithms include:
* **Visual Odometry:** This technique estimates a vehicle's position and path by analyzing a continuous sequence of camera images;
* **3D Free-space:** This identifies safe, empty areas on the road where the vehicle can drive without hitting obstacles;
* **Deep Learning:** This is a type of artificial intelligence that uses neural networks to recognize complex patterns, like detecting pedestrians or reading street signs.


---

## 📖 2.2 Images and Their Representation

The simplest way to understand cameras is the pinhole camera model. Light passes through a tiny hole and projects an inverted (upside-down) image. This basic design lets in only a small amount of light. However, modern geometric models used in software do not require this image inversion.

A photograph is an image created when a camera captures light. This light falls on a light-sensitive surface and is then encoded into a digital format.

A digital image is the numeric representation of that picture. It is stored as a vector or a matrix of numbers. Each number corresponds to a single pixel. A pixel is the smallest individual dot of color in an image.

The most common model used to represent color is the RGB model. RGB stands for Red, Green, and Blue. Every single pixel is represented by three separate numbers, indicating the amount of red, green, and blue light. Because it must store three values for every pixel, a color image uses more memory than a grayscale (black and white) image.


---

## 📖 2.2 Camera Calibration

Computer vision attempts to extract 3D real-world information from 2D flat image data. To do this, the system must use a mathematical model to transform 3D points into 2D pixels. Calibration is the process of finding the exact parameters for this model to ensure the real world projects correctly onto the image plane.
Calibration happens in two ways:

* **Static Calibration:** This occurs before the camera is used on the road. The camera is pointed at a static target with a known visual pattern. The software detects where the pattern is in the image and compares it to where it expects the pattern to be. This comparison computes both the internal and external parameters;
* **Online Calibration:** This happens continuously while the car is driving. The camera's physical position can shift dynamically due to external influences, such as a heavy baggage load altering the car's tilt. The system detects this de-calibration and adjusts the math automatically. The geometric model is not fixed; it changes over time.

### 📑 2.2.1 Intrinsic Parameters

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

### 📑 2.2.2 Extrinsic Parameters

Extrinsic parameters describe the camera's position and orientation relative to the real world. By convention, the origin of this world coordinate system is the center of the car's rear axis.
These parameters are represented by:
* **Rotation Matrix ($R$):** This accounts for three rotations applied in 3D space: pitch (tilting up or down), roll (tilting side to side), and yaw (turning left or right);
* **Translation Vector ($T$):** This accounts for the physical distance the camera is shifted from the origin.

Together, they form a combined matrix $[R|T]$.
The complete matrix-based projection formula, using both intrinsic and extrinsic parameters, is:

$$ \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} \sim K \cdot \left( R \cdot \begin{bmatrix} x \\ y \\ z \end{bmatrix} + T \right) = K \cdot [R|T] \cdot \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} $$


---

## 📖 2.3 Distortions

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

---

## 📖 2.4 Projective Geometry

Projective geometry is a branch of mathematics that studies the properties of objects that remain invariant (unchanged) under projective transformations. It is a very useful tool in computer vision.
* **Euclidean geometry** describes objects "as they are". Their true sizes and parallel lines are maintained regardless of how they move;
* **Projective geometry** describes objects "as they appear" to a camera. For example, parallel lane lines on a road will appear to converge in the distance.

Projective geometry rules can only be applied after lens distortions have been mathematically eliminated. Once corrected, the image formation can be correctly modeled based on perspective projection. Using planar homography matrices ($H$), a point $P$ on a flat plane can be transferred from the view of a first camera ($P_1$) to the view of a second camera ($P_2$) using the formula: $P_2 = H_{image} \cdot P_1$, where $H_{image} = H_2 \cdot H_1^{-1}$.


---

## 📖 2.5 3D Reconstruction

3D reconstruction is the process of calculating the 3D shape and position of real objects entirely from flat 2D images.

This can be accomplished using two types of setups:

* **Stereo camera system:** Two cameras placed at different positions look at the same object at the exact same time;
* **Mono camera system:** A single moving camera captures the same scene at different points in time.

Before depth can be calculated, the images must undergo rectification. Rectification is a mathematical process that aligns the images so that matching points appear on the exact same horizontal scan-line.

### 📑 2.5.1 Disparity and Depth Calculation

Disparity is the physical displacement (distance) between a point's location in the left image and its location in the right image. By measuring disparity, the system can determine how far away an object is.
* If an object is close, the disparity is large;
* If an object is far away, the disparity is small.

To calculate the exact depth ($z$), the software uses the focal length in pixels ($f_x$), the baseline distance between the two cameras ($b$), and the disparity ($d$):
$$z = \frac{f_x \cdot b}{d}$$

### 📑 2.5.2 The Inverse Problem

Once the depth ($z$) is known, the system solves the inverse problem to find the actual real-world $x$ and $y$ coordinates. It reverses the standard projection formulas:
* Horizontal position: $x = \frac{(u - u_0) \cdot z}{f_x}$ 
* Vertical position: $y = \frac{(v - v_0) \cdot z}{f_y}$

