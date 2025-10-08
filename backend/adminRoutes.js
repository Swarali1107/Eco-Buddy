// routes/reportRoutes.js
import express from 'express';
import Report from "../backend/reportModel.js";
const router = express.Router();

// GET all reports
router.get('/', async (req, res) => {
  try {
    const reports = await Report.find().sort({ date: -1 }); // latest first
    res.json(reports);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;
