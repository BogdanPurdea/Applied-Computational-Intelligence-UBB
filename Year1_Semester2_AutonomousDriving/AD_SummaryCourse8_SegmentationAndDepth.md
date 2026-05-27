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
