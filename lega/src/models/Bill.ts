import mongoose, { Schema, Document } from "mongoose";

export interface IBill extends Document {
  billId: string;
  state: string;
  title: string;
  geminiSummary: string;
  audioUrl?: string; // Optional if audio generation fails or is pending
  tags: string[];
  sector: "healthcare" | "education" | "service" | "corporate";
  createdAt: Date;
  updatedAt: Date;
}

const BillSchema: Schema = new Schema(
  {
    billId: { type: String, required: true, unique: true },
    state: { type: String, required: true },
    title: { type: String, required: true },
    geminiSummary: { type: String, required: true },
    audioUrl: { type: String },
    tags: { type: [String], default: [] },
    sector: {
      type: String,
      required: true,
      enum: ["healthcare", "education", "service", "corporate"],
    },
  },
  { timestamps: true },
);

// Prevent recompilation of model in hot reload
export default mongoose.models.Bill ||
  mongoose.model<IBill>("Bill", BillSchema);
