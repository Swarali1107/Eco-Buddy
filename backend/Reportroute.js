import express from "express";
import Report from "../backend/reportModel.js";
import upload from "../backend/middleware/upload.js";

const router = express.Router();

// POST a new report with photos
router.post("/", upload.array("photos", 3), async (req, res) => {
  try {
    const { reporterName, reporterContact, location, latitude, longitude, description } = req.body;
    const photos = req.files ? req.files.map(f => f.path) : [];

    const newReport = new Report({
      reporterName: reporterName || "Anonymous",
      reporterContact,
      location,
      latitude,
      longitude,
      description,
      photos
    });

    const savedReport = await newReport.save();
    res.status(201).json(savedReport);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server error" });
  }
});

// GET all reports
router.get("/", async (req, res) => {
  try {
    const reports = await Report.find().sort({ dateReported: -1 }); // latest first
    res.status(200).json(reports);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// GET single report by ID
router.get("/:id", async (req, res) => {
  try {
    const report = await Report.findById(req.params.id);
    if (!report) return res.status(404).json({ message: "Report not found" });
    res.status(200).json(report);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

export default router;
