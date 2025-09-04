# 🏋️‍♂️ FitGuard – IoT Management for Gyms

**FitGuard** is an innovative IoT solution designed to monitor and adjust environmental conditions in gyms, ensuring a safe, healthy, and enjoyable workout experience for both members and staff.

---

## 🔍 **Project Overview**

FitGuard enables gyms to dynamically adjust temperature, humidity, noise levels, and crowd density based on real-time data collected from IoT sensors.
The system provides gym managers with advanced tools to monitor and improve the training environment, enhancing customer satisfaction and safety..

---

## 🚀 Features

✔ **Monitor Environmental Conditions** – Real-time tracking of air quality, temperature, noise, and crowd density.  
✔ **Dynamic Adjustments** – Automatically adjust environmental factors based on real-time data.  
✔ **Personalized Workout Environment** – Maintain optimal conditions for each gym area (Gym Floor & Studios).  
✔ **Health & Safety** – Maintain optimal air quality and noise levels to ensure customer and employee well-being.  
✔ **Gym Management Tools** – View alerts, reports, and historical data for improved decision-making.  
✔ **Noise Reduction & Acoustic Control** – Adjust noise levels and music for a better workout atmosphere. 
✔ **Real-Time Alerts** – Notifications for high electricity consumption or overcrowding. 

The project follows **IoT principles** for real-time environmental monitoring and smart adjustments, using **Node.js** for backend development and **React.js** for the frontend.

---

## 🛠 Technologies Used

- **Node.js**
- **Express.js**
- **React.js** (Frontend)
- **IoT Sensors** (Temperature, Humidity, CO₂, Noise, Crowd Density)
- **MongoDB**

---

## 📊 Sensors (Emulators)
- **DHT-1** – Temperature & humidity.

- **ElecMeter** – Electricity consumption.

- **SensitivityMeter** – Noise/occupancy index (proxy for gym crowding).

- **Motion** – Motion/crowd detection sensor.

---

## 🔗 **Project Links**  

📌 [Project Presentation](https://www.youtube.com/watch?v=kY96Prmqh8o)  
📌 [Project Design on Canva](https://www.canva.com/design/DAGdxlUPqSQ/T0AoYankSs7rAPMulDDP5A/edit?utm_content=DAGdxlUPqSQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)  

---

## 👥 **Authors**  

- **Gal Mizrachi** - [GitHub Profile](https://github.com/GalMizrachi)  
- **Maya Lesnik** - [GitHub Profile](https://github.com/mayalesnik)  

---

## ⚙️ **How to Run**
- **Install requirements:**
 pip install -r requirements.txt

- **Start Manager (handles MQTT + DB + alerts):**
 python manager.py

- **Launch Emulators:**
 start_emulators.bat

- **Start the GUI:**
  python gui.py

- **(Optional) Run the Assistant BOT:**
 python assistant_BOT.py

 ---