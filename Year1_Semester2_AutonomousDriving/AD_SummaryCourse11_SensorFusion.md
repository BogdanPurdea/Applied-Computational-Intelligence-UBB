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
