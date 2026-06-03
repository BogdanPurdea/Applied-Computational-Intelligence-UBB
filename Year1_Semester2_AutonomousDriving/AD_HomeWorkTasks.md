<!-- --------------------------------------------------------------- -->
<!-- ------------------- COURSE 5 DEEP LEARNING -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 5 - Deep Learning**

## Definitions of Technical Terms

Before doing the math, let us define the symbols and terms used in the equations.
* **Model Parameters ($\theta$)**: The internal settings of the model that change during training. Think of them like tuning knobs on a radio;
* **Data Distribution ($p_{\text{data}}$)**: The true, real-world probability of the data;
* **Model Distribution ($p_{\text{model}}$)**: The probability guessed by our model based on its current parameters;
* **Expected Value ($\mathbb{E}$)**: The average result you would get if you repeated an experiment many times;
* **Argmin ($\text{argmin}$)**: A math operation that finds the exact input value that produces the lowest possible result;
* **Argmax ($\text{argmax}$)**: A math operation that finds the exact input value that produces the highest possible result;
* **Log-Likelihood**: A score that measures how well the model's predictions match the real data;
* **Kullback-Leibler Divergence ($D_{\text{KL}}$)**: A way to measure the difference between two probability distributions. A score of zero means they are completely identical.

---

## Step-by-Step Proof

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
