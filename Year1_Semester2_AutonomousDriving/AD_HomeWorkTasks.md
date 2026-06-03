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

