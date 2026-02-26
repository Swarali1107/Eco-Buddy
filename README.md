🌍 ECO-BUDDY
AI-Powered Real-Time Waste Hotspot Detection for Sustainable Cities
📌 Overview

ECO-BUDDY is an AI-driven urban waste monitoring system designed to help cities detect, visualize, and manage garbage accumulation efficiently. The platform processes real-time waste data and generates dynamic heatmaps to identify high-density waste hotspots, enabling proactive waste management and smarter resource allocation.

By transforming environmental data into actionable insights, ECO-BUDDY supports smart city initiatives and promotes sustainable urban development.


🚀 Key Features

    🔥 Real-Time Waste Hotspot Detection

    🗺️ Interactive Heatmap Visualization

    📊 Data-Driven Urban Insights

    ⚡ Backend–Python Integration

    🌱 Smart City & Sustainability Focus

    🧠 AI-Powered Data Processing using Pathway

    🗄️ MongoDB Atlas Integration



🏗️ System Architecture
    Frontend (Map + Heatmap Visualization)
            ↓
    Node.js Backend (Express API)
            ↓
    Python Processing Engine (Pathway)
            ↓
    MongoDB Atlas (Waste Data Storage)

Workflow:

    Waste data is stored in MongoDB.

    Backend API (/api/heatmap) triggers Python script.

    Python (Pathway) processes and aggregates hotspot data.

    Backend sends processed JSON response.

    Frontend renders interactive heatmap.



🛠️ Tech Stack
💻 Frontend

        HTML

        CSS

        JavaScript

        Leaflet.js (Map Visualization)

        Leaflet Heatmap Plugin

⚙️ Backend

        Node.js

        Express.js

        Child Process (exec) for Python integration

🧠 AI & Data Processing

        Python

        Pathway (Real-time data processing framework)

🗄️ Database

        MongoDB Atlas



📂 Project Structure
Eco-Buddy/
│
├── backend/
│   ├── server.js
│   ├── package.json
│
├── pathway_engine/
│   ├── hotspot_detector.py
│   ├── venv/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│
└── README.md


⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Swarali1107/Eco-Buddy.git
cd Eco-Buddy
2️⃣ Setup Backend
cd backend
npm install

Start server:

node server.js
3️⃣ Setup Python Environment
cd pathway_engine
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Install dependencies:

pip install pathway pymongo
4️⃣ Configure MongoDB

Create MongoDB Atlas cluster

Add connection string in server.js

Ensure waste data collection exists

👤 User Interface

Open in browser:

    frontend/index.html

    This is the public user-facing interface that displays:

    Interactive Map

    Waste Heatmap

    Real-time hotspot visualization

🛠️ Admin Interface

    Open in browser:

    frontend-pages/Adminportal.html

    This is the admin dashboard used for:

    Managing waste entries

    Monitoring data

🔌 API Endpoint
GET /api/heatmap

Returns processed hotspot data in JSON format.

Example Response:

[
  { "lat": 18.5204, "lng": 73.8567, "intensity": 0.8 },
  { "lat": 18.5300, "lng": 73.8500, "intensity": 0.6 }
]
🧠 How Hotspot Detection Works

Waste location data is collected.

Pathway processes streaming data.

Clustering logic identifies high-density regions.

Output is formatted as heatmap-compatible JSON.

Frontend visualizes using color intensity scaling.



🌱 Problem Statement

Urban waste management systems are reactive and inefficient. Overflowing garbage leads to:

Public health hazards

Environmental pollution

Poor resource allocation

Inefficient collection routes

ECO-BUDDY shifts waste management from reactive to proactive using AI.



🎯 Impact

    📉 Reduces garbage overflow

    🚛 Optimizes waste collection routes

    🌍 Improves environmental sustainability

    🏙️ Supports Smart City initiatives

    📊 Enables data-driven municipal decisions

    🔮 Future Enhancements

    📱 Citizen reporting mobile app

    🤖 ML-based waste prediction model

    🛰️ IoT bin sensors integration

    📈 Predictive analytics dashboard

    🚛 Route optimization using AI

    📊 Admin control panel


🏆 Use Cases

    Municipal Corporations

    Smart City Projects

    Environmental NGOs

    Urban Planning Departments

    Waste Management Companies
