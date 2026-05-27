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
