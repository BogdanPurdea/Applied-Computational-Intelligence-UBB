<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 5 DEEP LEARNING -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 5 - Deep Learning**

## 📖 5.1 Definitions of Technical Terms

Before doing the math, let us define the symbols and terms used in the equations.
* **Model Parameters ($\theta$)**: The internal settings of the model that change during training. Think of them like tuning knobs on a radio;
* **Data Distribution ($p_{\text{data}}$)**: The true, real-world probability of the data;
* **Model Distribution ($p_{\text{model}}$)**: The probability guessed by our model based on its current parameters;
* **Expected Value ($\mathbb{E}$)**: The average result you would get if you repeated an experiment many times;
* **Argmin ($\text{argmin}$)**: A math operation that finds the exact input value that produces the lowest possible result;
* **Argmax ($\text{argmax}$)**: A math operation that finds the exact input value that produces the highest possible result;
* **Log-Likelihood**: A score that measures how well the model's predictions match the real data;
* **Kullback-Leibler Divergence ($D_{\text{KL}}$)**: A way to measure the difference between two probability distributions. A score of zero means they are completely identical.

------------------------------------------------------------------------

## 📖 5.2 Step-by-Step Proof

**Goal:** We want to show that finding the parameters $\theta$ that minimize the expected KL divergence leads to the exact same formula as maximizing the log-likelihood.

**Step 1:** We start with the bottom equation. We want to find the parameters $\theta$ that minimize the expected KL divergence.

$$ \theta^* = \text{argmin}*\theta \mathbb{E}*{x \sim p_{\text{data}}(x)} [D_{\text{KL}}(p_{\text{data}}(y | x) || p_{\text{model}}(y | x; \theta))] $$

**Step 2:** We write out the standard mathematical definition for the KL divergence. It is the expected value of the difference between the logarithms of the two distributions.

$$ D_{\text{KL}}(p_{\text{data}} || p_{\text{model}}) = \mathbb{E}*{y \sim p*{\text{data}}(y|x)} [\log p_{\text{data}}(y | x) - \log p_{\text{model}}(y | x; \theta)] $$

**Step 3:** We substitute the expanded definition from Step 2 back into our original equation from Step 1.

$$ \theta^* = \text{argmin}*\theta \mathbb{E}*{x \sim p_{\text{data}}(x)} [\mathbb{E}*{y \sim p*{\text{data}}(y|x)} [\log p_{\text{data}}(y | x) - \log p_{\text{model}}(y | x; \theta)]] $$

**Step 4:** We combine the two expected value operations into a single expected value over both inputs $x$ and outputs $y$.

$$ \theta^* = \text{argmin}*\theta \mathbb{E}*{x, y \sim p_{\text{data}}(x, y)} [\log p_{\text{data}}(y | x) - \log p_{\text{model}}(y | x; \theta)] $$

**Step 5:** We separate the subtraction inside the expected value into two different expected values.

$$ \theta^* = \text{argmin}*\theta \left( \mathbb{E}*{x, y \sim p_{\text{data}}(x, y)} [\log p_{\text{data}}(y | x)] - \mathbb{E}*{x, y \sim p*{\text{data}}(x, y)} [\log p_{\text{model}}(y | x; \theta)] \right) $$

**Step 6:** We identify and remove constants. The first part of the equation, $\mathbb{E}_{x, y \sim p_{\text{data}}(x, y)} [\log p_{\text{data}}(y | x)]$, only depends on the true data. It does not contain our model's parameters $\theta$. Changing $\theta$ will never change this value. Therefore, we can safely ignore it when searching for the minimum.

$$ \theta^* = \text{argmin}*\theta \left( - \mathbb{E}*{x, y \sim p_{\text{data}}(x, y)} [\log p_{\text{model}}(y | x; \theta)] \right) $$

**Step 7:** We flip the operation. Finding the minimum of a negative number is mathematically identical to finding the maximum of a positive number. We change $\text{argmin}$ to $\text{argmax}$ and drop the negative sign.

$$ \theta^* = \text{argmax}*\theta \mathbb{E}*{x, y \sim p_{\text{data}}(x, y)} [\log p_{\text{model}}(y | x; \theta)] $$

------------------------------------------------------------------------

<!-- --------------------------------------------------------------- -->
<!-- ------------------------ COURSE 6 CNN ------------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 6 - Convolutional Neural Networks**

## 📖 6.1 Definitions of Technical Terms

Prove that finding the model settings that minimize the Negative Log-Likelihood (NLL) for a Gaussian distribution is exactly the same as minimizing the squared difference between the predictions and the true data (Ordinary Least Squares).

Before we start the math, let us define the pieces of the equation.

* **Model Parameters ($\theta$)**: The internal settings of the model. We want to find the best settings;
* **Model Prediction ($\mu(x, \theta)$)**: The output guessed by our model for a given input ($x$) and current settings ($\theta$);
* **True Target ($y$)**: The actual, correct answer we want our model to predict;
* **Variance ($\sigma^2$)**: A number representing how spread out the data is. The problem states this is "fixed and known," meaning it is just a constant number, like $5$ or $10$;
* **Expected Value ($\mathbb{E}$)**: The average result calculated over all our data points ($x, y$);
* **Argmin ($\arg\min$)**: A math operation. It means "find the specific value of $\theta$ that produces the lowest possible score";
* **Logarithm ($\log$)**: A math function that un-does exponential growth. It has special rules that make multiplication turn into addition, and exponents turn into multiplication.

------------------------------------------------------------------------

## 📖 6.2 Step-by-Step Proof

**Goal:** We will start with the complex top equation (Negative Log-Likelihood) and use basic algebra to turn it into the simple bottom equation (Ordinary Least Squares).

**Step 1: Start with the original NLL objective.**
We want to find the settings $\theta^*$ that minimize this expected value. The scary-looking fraction and the $e$ represent the formula for a normal bell curve.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y \sim p_{\text{data}}(x,y)} \left[ - \log \left( \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(y - \mu(x, \theta))^2}{2\sigma^2}} \right) \right]$$

**Step 2: Apply the multiplication rule for logarithms.**
A rule of logarithms is that the log of two things multiplied together is the sum of their individual logs: $\log(A \cdot B) = \log(A) + \log(B)$. We apply this to split the equation into two parts.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y} \left[ - \left( \log \left( \frac{1}{\sqrt{2\pi}\sigma} \right) + \log \left( e^{-\frac{(y - \mu(x, \theta))^2}{2\sigma^2}} \right) \right) \right]$$

**Step 3: Apply the exponent rule for logarithms.**
Another rule is that the natural logarithm ($\log$) completely cancels out the natural exponent ($e$). So, $\log(e^Z) = Z$. This removes the $e$ from our equation.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y} \left[ - \left( \log \left( \frac{1}{\sqrt{2\pi}\sigma} \right) - \frac{(y - \mu(x, \theta))^2}{2\sigma^2} \right) \right]$$

**Step 4: Distribute the negative sign.**
We multiply the negative sign on the outside into both terms on the inside. Two negatives make a positive.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y} \left[ - \log \left( \frac{1}{\sqrt{2\pi}\sigma} \right) + \frac{(y - \mu(x, \theta))^2}{2\sigma^2} \right]$$

**Step 5: Separate the expected value ($\mathbb{E}$).**
The average of a sum is the sum of the averages. We can break the equation into two separate expected value calculations.

$$\theta^* = \arg \min_{\theta} \left( \mathbb{E}_{x,y} \left[ - \log \left( \frac{1}{\sqrt{2\pi}\sigma} \right) \right] + \mathbb{E}_{x,y} \left[ \frac{(y - \mu(x, \theta))^2}{2\sigma^2} \right] \right)$$

**Step 6: Drop the constant term.**
Look closely at the first part: $- \log \left( \frac{1}{\sqrt{2\pi}\sigma} \right)$. There is no $\theta$ in this part. It is just a constant number. Because it never changes, it has zero impact on finding the minimum value for $\theta$. We can safely throw it away.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y} \left[ \frac{(y - \mu(x, \theta))^2}{2\sigma^2} \right]$$

**Step 7: Drop the constant multiplier.**
The term we have left is divided by $2\sigma^2$. The problem states variance ($\sigma^2$) is fixed. Multiplying or dividing an entire equation by a positive constant number changes the final score, but it does not change *where* the minimum score happens. For example, the lowest point of a valley is in the same location whether you measure depth in feet or inches. We can throw away the $2\sigma^2$ denominator.

$$\theta^* = \arg \min_{\theta} \mathbb{E}_{x,y} \left[ (y - \mu(x, \theta))^2 \right]$$

**Conclusion:** After simplifying, we are left with the expected value of the squared difference between the true target $y$ and the prediction $\mu(x, \theta)$. This perfectly matches the bottom equation.

------------------------------------------------------------------------

## 📖 6.3 Definitions of Technical Terms

Let us define the symbols used in the diagram before starting the math.

* **Weights ($W$)**: Numbers in a neural network that multiply the input data to change its scale;
* **Bias ($b$)**: A number added to the network's calculation to shift the result up or down;
* **Fully Connected Layer**: A standard neural network operation that applies a linear transformation. It multiplies inputs by Weights and adds a Bias;
* **Batch Normalization**: A technique used to stabilize and speed up training by standardizing the data;
* **Mean ($\mu$)**: The average value of the data passing through the layer;
* **Standard Deviation ($\sigma$)**: A measurement of how spread out the data is;
* **Gamma ($\gamma$)**: A learned parameter in Batch Normalization that scales the data;
* **Beta ($\beta$)**: A learned parameter in Batch Normalization that shifts the data.

------------------------------------------------------------------------

## 📖 6.4 Step-by-Step Derivation

**Goal:** We have two sequential operations. We want to mathematically combine them into one single operation taking the form $y = W'x + b'$. We need to find the exact formulas for the new weights ($W'$) and the new bias ($b'$).

**Step 1: Write the equation for the Fully Connected Layer.**
The input is $x$. The layer multiplies $x$ by the weights $W$ and adds the bias $b$. The intermediate output is $h$.

$$h = Wx + b$$

**Step 2: Write the equation for the Batch Normalization Layer.**
The input is $h$. The layer subtracts the mean $\mu$, divides by the standard deviation $\sigma$, multiplies by $\gamma$, and adds $\beta$. The final output is $y$.

$$y = \gamma \left( \frac{h - \mu}{\sigma} \right) + \beta$$

**Step 3: Substitute the first equation into the second.**
We replace the variable $h$ in the second equation with the full definition of $h$ from the first equation.

$$y = \gamma \left( \frac{(Wx + b) - \mu}{\sigma} \right) + \beta$$

**Step 4: Distribute the division and multiplication.**
We break the large fraction apart to separate the term containing $x$ from the constant terms. We multiply the $\frac{\gamma}{\sigma}$ factor into both parts.

$$y = \frac{\gamma}{\sigma} Wx + \frac{\gamma}{\sigma} (b - \mu) + \beta$$

**Step 5: Identify the new weights and bias.**
The target format for our new, single layer is $y = W'x + b'$. We match the parts of our expanded equation from Step 4 to this target format.

The new weight matrix $W'$ is everything multiplying $x$:

$$W' = \frac{\gamma}{\sigma} W$$

The new bias vector $b'$ is all the remaining constant terms added at the end:

$$b' = \frac{\gamma}{\sigma} (b - \mu) + \beta$$

**Conclusion:** By calculating $W'$ and $b'$ using these formulas after training is complete, you can safely remove the Batch Normalization layer entirely. The new single layer will produce the exact same output $y$ for any input $x$.

Here is the mathematical and programmatic solution for the Intersection over Union (IoU) homework task.

To build a strong foundation, let us first define the specific technical terms involved in this calculation.


------------------------------------------------------------------------

<!-- --------------------------------------------------------------- -->
<!-- ------------------------ COURSE 7 ICOD ------------------------ -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 7 - Image Classification and Object Detection**

## 📖 7.1 Definitions of Technical Terms

* **Bounding Box**: A rectangular border drawn around an object within an image to identify its location;
* **Coordinates**: Numbers that specify an exact location. For this task, we use the top-left corner $(x^{\text{min}}, y^{\text{min}})$ and the bottom-right corner $(x^{\text{max}}, y^{\text{max}})$ to define a box;
* **Intersection**: The shared area where two bounding boxes overlap;
* **Union**: The total, combined area covered by both bounding boxes, counting the overlapping region only once;
* **Intersection over Union (IoU)**: A standard metric used to evaluate how closely two bounding boxes match. It is a ratio that ranges from $0$ (no overlap) to $1$ (perfect match).

------------------------------------------------------------------------

## 📖 7.2 Step-by-Step Mathematical Computation

**Goal:** We need to find the IoU for two bounding boxes, $B_1$ and $B_2$, using their top-left and bottom-right coordinates.

Let the coordinates be defined as:

* $B_1 = (x_{1}^{\text{min}}, y_{1}^{\text{min}}, x_{1}^{\text{max}}, y_{1}^{\text{max}})$
* $B_2 = (x_{2}^{\text{min}}, y_{2}^{\text{min}}, x_{2}^{\text{max}}, y_{2}^{\text{max}})$

**Step 1: Find the coordinates of the intersection rectangle.**
The top-left corner of the intersection is the largest minimum coordinate. The bottom-right corner is the smallest maximum coordinate.

$$x_{I}^{\text{min}} = \max(x_{1}^{\text{min}}, x_{2}^{\text{min}})$$

$$y_{I}^{\text{min}} = \max(y_{1}^{\text{min}}, y_{2}^{\text{min}})$$

$$x_{I}^{\text{max}} = \min(x_{1}^{\text{max}}, x_{2}^{\text{max}})$$

$$y_{I}^{\text{max}} = \min(y_{1}^{\text{max}}, y_{2}^{\text{max}})$$

**Step 2: Calculate the dimensions of the intersection.**
We subtract the minimums from the maximums. We must use a $\max(0, \text{value})$ function because if the boxes do not overlap at all, the subtraction could result in a negative distance, which is physically impossible for a length.

$$\text{Width}_I = \max(0, x_{I}^{\text{max}} - x_{I}^{\text{min}})$$

$$\text{Height}_I = \max(0, y_{I}^{\text{max}} - y_{I}^{\text{min}})$$

**Step 3: Calculate the area of the intersection.**

$$\text{Area}_I = \text{Width}_I \cdot \text{Height}_I$$

**Step 4: Calculate the areas of the individual bounding boxes.**

$$\text{Area}_{B1} = (x_{1}^{\text{max}} - x_{1}^{\text{min}}) \cdot (y_{1}^{\text{max}} - y_{1}^{\text{min}})$$

$$\text{Area}_{B2} = (x_{2}^{\text{max}} - x_{2}^{\text{min}}) \cdot (y_{2}^{\text{max}} - y_{2}^{\text{min}})$$

**Step 5: Calculate the Union area.**
If we simply add the two areas together, we count the overlapping intersection area twice. Therefore, we must subtract one instance of the intersection area.

$$\text{Area}_U = \text{Area}_{B1} + \text{Area}_{B2} - \text{Area}_I$$

**Step 6: Compute the final IoU score.**
Divide the intersection by the union.

$$\text{IoU} = \frac{\text{Area}_I}{\text{Area}_U}$$

------------------------------------------------------------------------

## 📖 7.3 Definitions of Technical Terms

Calculate the final output of the bounding box decoder if the Fully Connected (FC) layer predicts a value of exactly zero for all its outputs.

Before performing the calculation, let us define the variables used in the diagram.

* **Fully Connected (FC) Layer**: The final part of the neural network that outputs raw numerical predictions;
* **Network Predictions ($d_x, d_y, d_w, d_h$)**: The raw numbers guessed by the network. They represent instructions on how to shift the center and scale the size of the box;
* **Crop Dimensions ($w^{\text{crop}}, h^{\text{crop}}$)**: The width and height of the initial region (the "crop") the network is analyzing;
* **Decoder**: The set of mathematical formulas that translate the raw network predictions into final, usable coordinates;
* **Final Output ($x, y, w, h$)**: The center coordinates ($x, y$) and the exact width and height ($w, h$) of the final bounding box.

------------------------------------------------------------------------

## 📖 7.4 Step-by-Step Mathematical Computation

**Goal:** Calculate the final values for $x, y, w$, and $h$ given that the network predictions ($d_x, d_y, d_w, d_h$) are all equal to $0$.

**Step 1: Write down the decoder formulas provided in the image.**

$$x = w^{\text{crop}} \cdot (d_x + 0.5)$$

$$y = h^{\text{crop}} \cdot (d_y + 0.5)$$

$$w = w^{\text{crop}} \cdot e^{d_w}$$

$$h = h^{\text{crop}} \cdot e^{d_h}$$

**Step 2: Substitute $0$ for all the network prediction variables.**

$$x = w^{\text{crop}} \cdot (0 + 0.5)$$

$$y = h^{\text{crop}} \cdot (0 + 0.5)$$

$$w = w^{\text{crop}} \cdot e^0$$

$$h = h^{\text{crop}} \cdot e^0$$

**Step 3: Simplify the equations.**
Remember that any non-zero number raised to the power of $0$ is exactly $1$ (so, $e^0 = 1$).

$$x = 0.5 \cdot w^{\text{crop}}$$

$$y = 0.5 \cdot h^{\text{crop}}$$

$$w = w^{\text{crop}} \cdot 1 = w^{\text{crop}}$$

$$h = h^{\text{crop}} \cdot 1 = h^{\text{crop}}$$

**Conclusion:** If the FC layer predicts zeroes, the final bounding box has its center exactly in the middle of the original crop ($50\%$ of the width and $50\%$ of the height), and its dimensions are exactly equal to the original crop's dimensions. In plain terms, predicting zeroes means the network chooses not to adjust the initial box at all.


------------------------------------------------------------------------

<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 8 SEGMENTATION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 8 - Segmentation and Depth**

## 📖 8.1 Definitions of Technical Terms

Demonstrating that the Shift-and-Stitch method is mathematically equivalent to using Dilated Convolutions.

* **Max Pooling**: A mathematical filter that slides a window over data and only keeps the largest number in that window;
* **Stride ($s$)**: The number of positions a filter jumps forward each time it moves;
* **Convolution**: A mathematical operation where a small grid of weights (the kernel) slides over data, multiplying and adding numbers together to find patterns;
* **Shift-and-Stitch**: A technique used to prevent losing detail when using a stride greater than $1$. It shifts the input data slightly, runs the network multiple times, and weaves (interleaves) the final results together;
* **Dilated Convolution**: A convolution filter that spreads out its points by skipping spaces. It covers a wider area without requiring more parameters;
* **Dilation Rate ($r$)**: The number of steps between each point in a dilated convolution filter.

------------------------------------------------------------------------

## 📖 8.2 Part 1: The 1D Case

**Goal:** Prove that running Shift-and-Stitch (with a max pool stride of $s$) produces the exact same final output as setting the max pool stride to $1$ and using a dilated convolution with a rate of $r = s$.

Let $x$ be the 1D input data sequence. Let $w$ be the weights of the convolution kernel. Let $k$ be the size of the max pool window.

### The Shift-and-Stitch Equation

In Shift-and-Stitch, we shift the input data by a distance $\Delta$ (where $\Delta$ ranges from $0$ to $s-1$).
The max pool layer uses a stride of $s$. The output of the max pool at step $j$ for a shift $\Delta$ is:

$$\text{Pool}[j] = \max(x[j \cdot s + \Delta : j \cdot s + \Delta + k])$$

The standard convolution applies the weights $w$ to this pooled result.
When we "stitch" (interleave) the results back together, the final output is mapped to a high-resolution position $t$, where $t = j \cdot s + \Delta$. We can write the stitched output $z[t]$ as:

$$z[t] = \sum_{a} w[a] \cdot \max(x[t + a \cdot s : t + a \cdot s + k])$$

### The Dilated Convolution Equation

In the second approach, the max pool layer is changed to have a stride of exactly $1$. Therefore, the output of the pool layer at any position $t$ is:

$$m[t] = \max(x[t : t + k])$$

Next, we apply a dilated convolution to $m$. The dilation rate is set to the original stride ($r = s$). The formula for a dilated convolution is:

$$y[t] = \sum_{a} w[a] \cdot m[t + a \cdot s]$$

We substitute our definition of $m$ into this equation:

$$y[t] = \sum_{a} w[a] \cdot \max(x[t + a \cdot s : t + a \cdot s + k])$$

**Conclusion for 1D:** The final equation for $y[t]$ (Dilated Convolution) exactly matches the final equation for $z[t]$ (Shift-and-Stitch). They calculate the exact same numbers.

------------------------------------------------------------------------

## 📖 8.3 Part 2: The 2D Case

**Goal:** Expand the 1D proof to 2D images.

The logic remains identical. The only difference is that our position index $t$ becomes a 2D coordinate $(u, v)$ representing width and height. Our convolution weight index $a$ becomes a 2D grid $(a, b)$.

### The Shift-and-Stitch Equation (2D)

The input is shifted by $(\Delta_u, \Delta_v)$. We weave the outputs into a high-resolution 2D grid at position $(u, v)$. The stride $s$ applies to both directions.

$$z[u, v] = \sum_{a} \sum_{b} w[a, b] \cdot \max(x[u + a \cdot s : u + a \cdot s + k, v + b \cdot s : v + b \cdot s + k])$$

### The Dilated Convolution Equation (2D)

First, we run the 2D max pool with a stride of $1$ in both directions.

$$m[u, v] = \max(x[u : u + k, v : v + k])$$

Next, we run the 2D dilated convolution with a rate of $r = s$.

$$y[u, v] = \sum_{a} \sum_{b} w[a, b] \cdot m[u + a \cdot s, v + b \cdot s]$$

Substitute the definition of $m[u, v]$ into the equation:

$$y[u, v] = \sum_{a} \sum_{b} w[a, b] \cdot \max(x[u + a \cdot s : u + a \cdot s + k, v + b \cdot s : v + b \cdot s + k])$$

**Conclusion for 2D:** The formula for $y[u, v]$ perfectly matches $z[u, v]$. The outputs are mathematically identical. The dilated convolution computes the Shift-and-Stitch result in a single pass.

------------------------------------------------------------------------

## 📖 8.4 
