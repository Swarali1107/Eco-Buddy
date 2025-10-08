import mongoose from "mongoose";

const reportSchema = new mongoose.Schema({
  reporterName: { type: String, default: "Anonymous" },
  reporterContact: { type: String, required: true },
  location: { type: String, required: true },
  latitude: Number,
  longitude: Number,
  description: String,
  photos: [String],  // store file paths
  dateReported: { type: Date, default: Date.now },
  status: { type: String, default: "Pending" } // Pending / Verified / Cleaned
});

const Report = mongoose.model("Report", reportSchema);
export default Report;
