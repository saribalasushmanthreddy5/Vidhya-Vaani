import { NextRequest, NextResponse } from "next/server";
import { TEXTBOOK_CHUNKS } from "@/lib/textbookData";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { language = "English" } = body;

    const apiKey = process.env.GEMINI_API_KEY;
    const candidateModels = [
      process.env.GEMINI_MODEL,
      "gemini-3.5-flash-lite",
      "gemini-3.5-flash",
      "gemini-3.8-flash",
    ].filter(Boolean) as string[];

    const defaultQuiz = [
      {
        question: "What is the primary site of complete digestion of carbohydrates, proteins, and fats in the human body?",
        options: ["Stomach", "Small Intestine", "Large Intestine", "Mouth"],
        correct_index: 1,
        topic: "Digestion & Enzymes",
        explanation: "The small intestine is the site of complete digestion, assisted by bile juice and pancreatic enzymes.",
        page: 3
      },
      {
        question: "Which of the following describes the chemical equation for Photosynthesis?",
        options: [
          "6CO2 + 12H2O + Sunlight ---> C6H12O6 + 6O2 + 6H2O",
          "C6H12O6 + 6O2 ---> 6CO2 + 6H2O + Energy",
          "6CO2 + 6H2O ---> C2H5OH + 2ATP",
          "Pyruvate ---> Lactic acid + 2ATP"
        ],
        correct_index: 0,
        topic: "Photosynthesis & Chlorophyll",
        explanation: "6CO2 + 12H2O with solar energy trapped by chlorophyll synthesizes glucose, water, and oxygen.",
        page: 1
      },
      {
        question: "Why does hydrochloric acid (HCl) secrete in the stomach during digestion?",
        options: [
          "To emulsify large fat globules",
          "To break down complex starch into maltose",
          "To create an acidic medium necessary for pepsin action and kill pathogens",
          "To absorb water from undigested food"
        ],
        correct_index: 2,
        topic: "Gastric Juice & Stomach Acid",
        explanation: "HCl creates an acidic pH (1.5-2.5) that activates pepsin to digest proteins.",
        page: 3
      },
      {
        question: "During vigorous muscular exercise in humans, sudden cramps occur due to the accumulation of:",
        options: ["Ethanol", "Lactic Acid", "Carbon Dioxide", "Hydrochloric Acid"],
        correct_index: 1,
        topic: "Cellular Respiration & Muscle Fatigue",
        explanation: "Anaerobic respiration in muscle cells produces lactic acid, causing cramps.",
        page: 4
      },
      {
        question: "How do guard cells control the opening and closing of stomata?",
        options: [
          "By changing temperature",
          "By swelling when water enters and shrinking when water is lost",
          "By producing chlorophyll",
          "By releasing oxygen into the air"
        ],
        correct_index: 1,
        topic: "Stomatal Gas Exchange",
        explanation: "Water entering guard cells makes them turgid, opening the pore; losing water causes them to shrink and close the pore.",
        page: 2
      }
    ];

    const contextSample = TEXTBOOK_CHUNKS.map(c => `[Page ${c.page}]: ${c.text}`).join("\n\n");
    const prompt = `Based ONLY on the following textbook excerpts:
${contextSample}

Generate a 5-question multiple choice quiz for school students in ${language}.
Format your response as a valid, pure JSON array without markdown code blocks, with each object containing:
- "question": string
- "options": array of 4 strings
- "correct_index": integer (0, 1, 2, or 3)
- "topic": string (concise concept name like 'Photosynthesis', 'Respiration', 'Digestion')
- "explanation": string
- "page": integer (the page number cited)`;

    for (const model of candidateModels) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
        const resp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: prompt }] }],
            generationConfig: { temperature: 0.3 }
          })
        });

        if (resp.ok) {
          const data = await resp.json();
          const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
          const cleanJson = rawText.replace(/```json/g, "").replace(/```/g, "").trim();

          const parsed = JSON.parse(cleanJson);
          if (Array.isArray(parsed) && parsed.length >= 3) {
            return NextResponse.json({ quiz: parsed });
          }
        }
      } catch {
        // Continue to next model
      }
    }

    return NextResponse.json({ quiz: defaultQuiz });
  } catch (error: any) {
    console.error("Quiz API error:", error);
    return NextResponse.json({ error: error?.message || "Failed to generate quiz" }, { status: 500 });
  }
}
