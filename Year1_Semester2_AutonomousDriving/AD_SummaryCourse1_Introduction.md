<!-- --------------------------------------------------------------- -->
<!-- -------------------- COURSE 1 INTRODUCTION -------------------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 1 - Artificial Intelligence-Based Perception in Self-Driving Vehicles**

---

## 📖 1.1 Introduction to Data-Driven Perception
Modern self-driving cars use Artificial Intelligence (AI) to understand their surroundings. This is called **perception**. 

* **The Shift to 360° Systems:** Older systems used single sensors for simple tasks. Modern vehicles use multiple sensors (cameras and radars) placed all around the car to get a full 360-degree view; 
* **The AI Pipeline:** The car's computer takes sensor data and runs it through three main steps: Perception (understanding the scene), Prediction (guessing what will happen next), and Planning (deciding how to drive);
* **Mobile Computers:** Vehicles are turning into advanced, AI-powered mobile computing centers. 

### The Rise of Foundation Models
The industry is moving from classical Machine Learning to **Foundation Models**.
* **Definition:** A foundation model is a very large AI model. It is trained on huge amounts of data that has not been labeled by humans. Once trained, it can be reused for many different tasks;
* **Emergence:** The model learns behaviors naturally from the data, rather than being strictly programmed to do them;
* **Homogenization:** The exact same methods can be used to solve completely different problems;

---

## 📖 1.2 Main Challenges in AI for Self-Driving
Building safe and effective AI for cars involves four main challenges: Representation, Safety, Efficiency and Cost;

### 📑 1.2.1 The Representation Challenge
**Representation** is how the AI internally maps and understands the physical world;
* **The Problem:** The AI must perform well even when the environment changes (e.g., different weather or new cities). Just training the AI on a specific driving task is not enough to help it truly understand the world;
* **Solutions:** Engineers use different methods to train the AI. They use **Self-Supervision** (where the AI learns by finding patterns in data without human labels) and **Large Language Models** to give the AI extra guidance;
* **Inductive Bias:** This is a set of built-in assumptions that help the AI learn. Inductive bias is strictly required for the AI to learn anything useful.

### 📑 1.2.1 The Safety Challenge
Cars must follow strict mandatory safety rules, such as ISO 26262 and ISO/PAS 21448.
* **Inherently Safe AI:** Building an AI that perfectly avoids all hazards is impossible with today's technology;
* **Safe Fail:** When a system breaks, it must fail safely. The car must stay on the road and safely slow down or stop. This requires real-time error detection;
* **Safety Margins:** The AI often performs worse in the real world than it did in the lab. Engineers fix this by improving **model robustness**. This includes estimating when the AI is uncertain and detecting errors during driving.

### 📑 1.2.1 The Efficiency Challenge
The computers inside cars are limited. They have low power, low internet bandwidth, and limited processing abilities. However, they still need to react in real-time. 
* **Solutions:** Engineers shrink the AI models to make them run faster.
    * **Knowledge Distillation (KD):** A small model (the student) is trained to copy the behavior of a massive model (the teacher);
    * **Quantization:** This shrinks the math inside the AI to use less memory;
    * **Neural Architecture Search (NAS):** An automated process that finds the fastest and best shape for the AI model.

### 📑 1.2.1 The Cost Challenge
Creating AI is very expensive.
* **Problems:** Collecting data takes too long, legal rules (like GDPR) make data sharing hard, and development costs are unpredictable;
* **Solutions:** * **Active Learning:** The AI asks humans to label only the most confusing or "interesting" images, saving time and money;
    * **Federated Learning:** Cars learn locally and only share their learned patterns with the cloud, not raw private data;
    * **Multi-Task Learning:** One AI model learns to do many tasks at once, saving computer power.

---

## 📖 1.3 Key Takeaways
* **Hardware & Software:** Self-driving relies on advanced computers, computer vision, and machine learning;
* **No Free Lunch Theorem:** Even with massive amounts of data, an AI cannot learn without built-in assumptions (inductive bias);
* **The Future:** The industry is slowly moving past just analyzing sensor data. The ultimate goal is **end-to-end driving**, where a single AI takes in camera video and directly outputs steering wheel and pedal commands;
* **Industry & Academia:** Solving these massive open problems requires schools and companies to work closely together.
