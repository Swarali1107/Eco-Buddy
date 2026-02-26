import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors";
import reportRoutes from "./Reportroute.js";
import adminRoutes from "./adminRoutes.js";
import { exec } from 'child_process';


dotenv.config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("CONNECTED TO ATLAS SUCCESSFULLY"))
  .catch(err => console.log("ATLAS ERROR:", err.message));
// Routes
app.use("/api/reports", reportRoutes);
app.use("/api/admin", adminRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.get('/api/heatmap', (req, res) => {
    exec('"./venv/Scripts/python.exe" ../pathway_engine/hotspot_detector.py', (error, stdout, stderr) => {

        if (error) {
            console.error("Heatmap Python Error:", error);
            return res.status(500).send("Heatmap error");
        }

        if (stderr) {
            console.error("Python stderr:", stderr);
        }

        try {
            const data = JSON.parse(stdout);
            res.json(data);
        } catch (err) {
            console.error("JSON Parse Error:", err);
            res.status(500).send("Invalid heatmap data");
        }

    });
});
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));

