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
