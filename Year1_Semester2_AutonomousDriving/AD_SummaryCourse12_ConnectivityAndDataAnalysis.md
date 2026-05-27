<!-- --------------------------------------------------------------- -->
<!-- ---------- COURSE 12 Connectivity and Data Analysis ----------- -->
<!-- --------------------------------------------------------------- -->

# 🔖 **Course 12 - Connectivity and Data Analysis**

---

## 📖 12.1 Overview
Modern mobility relies on "connected cars" that communicate with various entities to improve safety, efficiency, and the user experience.

### 📑 12.1.1 Communication Ecosystem
A car should communicate with the following:
* **V2V (Vehicle-to-Vehicle):** Direct communication between cars;
* **V2I (Vehicle-to-Infrastructure):** Communication between the car and road infrastructure (e.g., traffic lights, road sensors);
* **V2N (Vehicle-to-Network):** Communication with cellular networks or the cloud;
* **V2P (Vehicle-to-Pedestrian):** Communication with devices carried by pedestrians;
* **V2E (Vehicle-to-Everything):** Comprehensive connectivity encompassing all previously mentioned domains.

### 📑 12.1.2 Benefits of Connected Cars
* Improved driving safety and autonomous drive support;
* Enhanced in-car experience and advanced navigation;
* Environmental benefits (emissions reduction) and efficiency (saving time and money).

---

## 📖 12.2 Technology and Communication
Connectivity relies on various protocols, each with specific trade-offs regarding cost, power, and reliability.

| Protocol | Pros | Cons |
| :--- | :--- | :--- |
| **Satellite** | Available globally with line-of-sight | Extremely expensive |
| **Mobile (3G/4G/5G)** | Stable, universal compatibility | High cost, high power usage, no direct V2V |
| **LPWA** | Stable, wide area, low energy | Requires new infrastructure |
| **WiFi** | Affordable, universal | High power, unstable/inconsistent |
| **Bluetooth** | Widely established | Inconsistent, security issues |
| **NFC** | Simple setup, encrypted | Very short range |

### 📑 12.2.1 Server-Side Architecture
To handle large-scale data from connected vehicles, systems must prioritize:
* **High Availability:** Utilizing standby systems and multi-master configurations (Tools: `keepalived`, `ha-proxy`, `Kubernetes`);
* **Scalability:** Vertical (larger hardware) or horizontal (more nodes) scaling;
* **Asynchronous Processing:** Using message queues (e.g., `Kafka`, `RabbitMQ`) to handle data peaks;
* **Distributed Systems:** Utilizing multiple nodes and geo-locations, managed via `DNS` and `DDNS`.

---

## 📖 12.3 Data Analysis and Pipelines
Data from the car is constantly sent to the cloud, processed, and utilized for fleet monitoring, reporting, and real-time mapping.

### 📑 12.3.1 Data Management Challenges
* **Big Data Management:** Process data as close to the source as possible using techniques like **MapReduce** (Tools: `Hadoop`, `Spark`);
* **Data Integrity:** Ensuring data remains unchanged during transfer, often verified via hashing algorithms like `MD5` or `SHA-1`;
* **Security:** Implementing secure zones (`DMZ`) and handling OTA (Over-the-Air) updates.

### 📑 12.3.2 Data Processing Pipelines
Data pipelines transform raw data into usable information through a series of operators:
1.  **Input Operator:** Reads raw data;
2.  **Processing Operator:** Transforms or analyzes data;
3.  **Output Operator:** Writes data to the destination.

### 📑 12.3.3 Data Delivery Semantics
When sending data through pipelines, different delivery guarantees can be achieved:
* **At most once:** Data might be lost but is never duplicated;
* **At least once:** Data is never lost but might be duplicated;
* **Exactly once:** The ideal but complex state, requiring state management (e.g., a `STATE Database` to track progress and prevent duplicate processing).

### 📑 12.3.4 Data Hierarchy
Data follows a progression from raw input to final presentation:
1.  **RAW Data:** Unprocessed information directly from sensors;
2.  **Meta Data:** Information describing the raw data;
3.  **Semantic Data:** Data with context or meaning applied;
4.  **Indexing:** Organizing data for fast retrieval;
5.  **Presentation:** The final format for user interaction (e.g., reports, dashboards).

---

## 📖 12.4 Use Cases
* **Connected Horizon:** Predictive assistance and energy management that adjust vehicle behavior based on road conditions ahead;
* **Community-Based Parking:** Cars share parking data with the cloud to reduce search time, fuel costs and stress;
* **Connected Workshop:** Vehicles automatically transmit diagnostic codes, tire pressure, battery health and wheel alignment data to service centers, increasing customer retention and satisfaction;
* **Autonomous Driving Levels:** Support for SAE levels 2–4, including highway pilots, traffic jam pilots and automated valet parking.
