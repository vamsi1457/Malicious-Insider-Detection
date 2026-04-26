# Malicious Insider Detection System (MIDS)
### Enterprise Cybersecurity Behavioural Analytics Framework

The modern enterprise security model is shifting from perimeter defense to internal user behavior monitoring. Traditional firewalls are blind to threats originating from within. MIDS provides a scalable, real-time solution to identify malicious behavioral shifts using a Hybrid Machine Learning approach.

---

## 1. System Architecture Visualization

The system operates as a continuous pipeline, moving data from raw ingestion to active threat alerting.

[ DATA INGESTION ] ----> [ HYBRID ML ENGINE ] ----> [ PERSISTENCE ] ----> [ MONITORING ]
      |                         |                        |                      |
Live Network Logs        1. Isolation Forest       SQLite Database        Streamlit UI
(FastAPI Endpoint)       2. LSTM Neural Net        (Encrypted Storage)    (Admin Panel)

---

## 2. Technical Component Breakdown

| Module | Technology | Primary Function |
| :--- | :--- | :--- |
| Backend API | FastAPI / Uvicorn | High-performance asynchronous log ingestion and real-time processing. |
| Static Brain | Isolation Forest (Scikit-Learn) | Identifies point-in-time anomalies such as unauthorized mass downloads. |
| Temporal Brain | LSTM Neural Network (TensorFlow) | Tracks sequences of user actions to detect patterns that shift over time. |
| Storage Layer | SQLite (SQLAlchemy) | Persistent storage for system telemetry, threat logs, and admin credentials. |
| Frontend UI | Streamlit | Secure administrative dashboard for real-time monitoring and analytics. |

---

## 3. Advanced Features

### Hybrid Predictive Engine
The system does not rely on a single algorithm. It utilizes a dual-layer verification process. First, the Isolation Forest checks if the specific action is an outlier based on historical frequency. Second, the LSTM (Long Short-Term Memory) network analyzes the sequence of actions leading up to that point to catch "low-and-slow" threats.

### Privacy by Design
Identity masking is integrated into the preprocessing pipeline. Personal identifiers are removed during the training and inference stages to ensure data protection compliance (GDPR/ISO 27001) while maintaining high detection precision.

### Role-Based Access Control (RBAC)
The Admin Dashboard is protected by a secure authentication layer. On the first run, the system prompts the administrator to initialize a master password, which is then stored securely in the local database for all future sessions.

---

## 4. Module Descriptions

### Data Simulator
This module mimics a live enterprise environment. It generates realistic logs including timestamps, user IDs, IP addresses, and specific system actions. It includes a streaming script that posts data to the API every two seconds to test system latency.

### Machine Learning Training
The training suite prepares the artifacts required for live inference.
- train_iforest.py: Analyzes the mock data to establish a baseline of normal behavior.
- train_lstm.py: Learns the typical order of operations for users to predict and flag sequence breaks.

### Backend Infrastructure
The engine is built for 24/7 uptime. It receives raw JSON payloads, converts them into numeric tensors for the models, and commits the results to the database within milliseconds.

---

## 5. Installation and Deployment

### 5.1 Environment Setup
Install the required Python libraries using the package manager.
```bash
pip install -r requirements.txt"# Malicious-Insider-Detection" 
