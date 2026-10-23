import { NextRequest, NextResponse } from "next/server";
import { retrieveRelevantPassages, LANGUAGES } from "@/lib/textbookData";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { query, language = "English", actionType = "normal" } = body;

    if (!query || typeof query !== "string") {
      return NextResponse.json({ error: "Query is required" }, { status: 400 });
    }

    // Retrieve top grounded textbook passages
    const retrieved = retrieveRelevantPassages(query, 3);
    const topPassages = retrieved.map((r) => r.chunk);
    const contextText = topPassages
      .map((p, i) => `[Source ${i + 1} - Page ${p.page}]: ${p.text}`)
      .join("\n\n");

    const apiKey = process.env.GEMINI_API_KEY;
    const modelName = process.env.GEMINI_MODEL || "gemini-2.5-flash";

    let answer = "";

    if (!apiKey) {
      // Fallback response with strict grounding from textbook if no API key set
      answer = `Based on NCERT Class 10 Biology [Page ${topPassages[0]?.page || 1}]:\n\n${topPassages[0]?.text || "Please refer to Chapter 6 Life Processes for details."}`;
    } else {
      let promptInstruction = "";
      if (actionType === "simpler") {
        promptInstruction = "Explain this concept in very simple, easy-to-understand terms suitable for a 5th-grade student. Use clear analogies.";
      } else if (actionType === "example") {
        promptInstruction = "Provide an intuitive, everyday real-world example from daily life in India to illustrate this concept.";
      } else {
        promptInstruction = "Provide a clear, engaging explanation strictly grounded in the provided textbook passages.";
      }

      const systemPrompt = `You are VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी), a compassionate, voice-first AI tutor for Indian school students.
You must teach strictly based on the following NCERT textbook passages:
${contextText}

Guidelines:
1. Grounding: Answer ONLY using facts from the textbook passages above. Never hallucinate.
2. Citations: Explicitly cite the textbook page number in your answer (e.g. [Page ${topPassages[0]?.page || 1}]).
3. Language: Respond in ${language}. Maintain a warm, encouraging teacher's tone.
4. Action: ${promptInstruction}
5. Voice-Readiness: Keep explanations clear, natural to speak aloud, and structured.`;

      // Direct Gemini REST call (lightning fast on Vercel serverless)
      const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${apiKey}`;
      const payload = {
        contents: [
          {
            role: "user",
            parts: [
              { text: systemPrompt },
              { text: `Student Question: ${query}` }
            ]
          }
        ],
        generationConfig: {
          temperature: 0.2,
          maxOutputTokens: 800
        }
      };

      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) {
        const errText = await resp.text();
        console.error("Gemini API error:", errText);
        // Fallback to grounded textbook excerpt
        answer = `According to your NCERT Textbook [Page ${topPassages[0]?.page || 1}]:\n\n${topPassages[0]?.text}`;
      } else {
        const data = await resp.json();
        answer = data.candidates?.[0]?.content?.parts?.[0]?.text || `[Page ${topPassages[0]?.page || 1}] ${topPassages[0]?.text}`;
      }
    }

    return NextResponse.json({
      answer,
      sources: topPassages.map((p) => ({
        id: p.id,
        page: p.page,
        section: p.section,
        text: p.text
      })),
      language,
      query,
      timestamp: new Date().toISOString()
    });
  } catch (error: any) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      { error: error?.message || "Internal server error" },
      { status: 500 }
    );
  }
}
