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
