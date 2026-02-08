import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || "");

export async function summarizeWithGemini(
  billText: string,
  sector: string,
): Promise<string> {
  if (!process.env.GOOGLE_API_KEY) {
    console.warn("GOOGLE_API_KEY is not set. Returning mock summary.");
    return "Summary unavailable: API Key not configured.";
  }

  try {
    const model = genAI.getGenerativeModel({ model: "gemini-pro" }); // Or gemini-1.5-pro if available/preferred

    const prompt = `
      You are a labor union representative and legal advocate for women in the ${sector} industry. 
      Summarize this legislation in 3 sentences. 
      Focus on: 
      1. Does this affect my shift/hours? 
      2. Does this affect my bodily autonomy? 
      3. What action should I take? 
      Tone: Empathetic, clear, protective.

      Legislation Text:
      ${billText.substring(0, 10000)} // Truncate to avoid context limits if text is huge
    `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    return text;
  } catch (error) {
    console.error("Error in summarizeWithGemini:", error);
    return "Error generating summary. Please check logs.";
  }
}
