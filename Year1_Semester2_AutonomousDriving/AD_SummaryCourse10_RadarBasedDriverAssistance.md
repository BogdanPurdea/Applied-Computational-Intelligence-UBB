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
