import { NextRequest, NextResponse } from "next/server";
import { retrieveRelevantPassages, LANGUAGES } from "@/lib/textbookData";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { query, language = "English", actionType = "normal", imageBase64, imageMimeType = "image/jpeg" } = body;

    if (!query && !imageBase64) {
      return NextResponse.json({ error: "Query or image is required" }, { status: 400 });
    }

    const effectiveQuery = query || "Please read this textbook question and explain the answer step by step.";

    // Retrieve top grounded textbook passages
    const retrieved = retrieveRelevantPassages(effectiveQuery, 3);
    const hasMatch = retrieved.length > 0 && retrieved[0].score > 0;
    const topPassages = retrieved.map((r) => r.chunk);
    const topChunk = topPassages[0];

    const contextText = topPassages
      .map((p, i) => `[Source ${i + 1} - ${p.chapter} - Page ${p.page}]:\n${p.text}`)
      .join("\n\n");

    const apiKey = process.env.GEMINI_API_KEY;
    
    // Ordered candidate models (gemini-3.5-flash-lite has active free quota)
    const candidateModels = [
      process.env.GEMINI_MODEL,
      "gemini-3.5-flash-lite",
      "gemini-3.5-flash",
      "gemini-3.8-flash",
    ].filter(Boolean) as string[];

    let answer = "";
    let callSucceeded = false;

    let promptInstruction = "";
    if (actionType === "simpler") {
      promptInstruction = "Explain this concept in very simple, easy-to-understand terms suitable for a 5th-grade student. Use clear analogies.";
    } else if (actionType === "example") {
      promptInstruction = "Provide an intuitive, everyday real-world example from daily life in India to illustrate this concept.";
    } else {
      promptInstruction = "Provide a clear, engaging explanation tailored for a school learner.";
    }

    const systemPrompt = `You are VidyaVaani (ವಿಧ್ಯಾವಾಣಿ / विद्यावाणी), a compassionate, voice-first AI tutor for Indian school students.
Context from NCERT Class 10 Science textbook (Chapter: Life Processes):
${contextText}

Strict Rules:
1. Grounding & Accuracy: Answer using the provided textbook context whenever relevant. Always cite the exact page number (e.g. [Page ${topChunk?.page || 1}]).
2. "I Don't Know" Fallback (Anti-Hallucination): If the student's question or image is completely outside this textbook chapter (e.g. sports, politics, unrelated subjects, or completely off-topic), you MUST politely refuse to answer, explaining in ${language}:
   "I cannot find this topic in your textbook chapter (NCERT Class 10: Life Processes). To prevent incorrect or ungrounded explanations, please ask a question related to this chapter."
3. Multimodal: If an image of a textbook page or question is provided, extract the question from the image and solve it step-by-step grounded in NCERT concepts.
4. Language: Respond fluently in ${language}. Maintain a warm, encouraging teacher's tone.
5. Action: ${promptInstruction}
6. Voice-Readiness: Keep explanations clear, natural to speak aloud, and well-structured.`;

    // Try candidate models in order
    for (const model of candidateModels) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
        
        const userParts: any[] = [{ text: systemPrompt }];
        
        if (imageBase64) {
          // Multimodal image part for Gemini Vision (Photo-a-Question)
          userParts.push({
            inlineData: {
              mimeType: imageMimeType,
              data: imageBase64.replace(/^data:image\/\w+;base64,/, ""),
            },
          });
          userParts.push({ text: `Student snapped a photo of their textbook question: "${effectiveQuery}"` });
        } else {
          userParts.push({ text: `Student Question: ${effectiveQuery}` });
        }

        const payload = {
          contents: [
            {
              role: "user",
              parts: userParts,
            },
          ],
          generationConfig: {
            temperature: 0.25,
            maxOutputTokens: 800,
          },
        };

        const resp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (resp.ok) {
          const data = await resp.json();
          const generated = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (generated && generated.trim().length > 0) {
            answer = generated.trim();
            callSucceeded = true;
            break;
          }
        } else {
          const err = await resp.text();
          console.warn(`Model ${model} failed:`, err);
        }
      } catch (e) {
        console.warn(`Error with model ${model}:`, e);
      }
    }

    // Intelligent Fallback only if all Gemini models failed
    if (!callSucceeded || !answer) {
      if (hasMatch) {
        answer = `According to your NCERT Textbook [Page ${topChunk.page} - ${topChunk.section}]:\n\n${topChunk.text}`;
      } else {
        answer = `I cannot find this topic in your textbook chapter (NCERT Class 10: Life Processes). To prevent incorrect or ungrounded explanations, please ask a question related to this chapter (such as Photosynthesis, Digestion, Respiration, or Excretion).`;
      }
    }

    return NextResponse.json({
      answer,
      sources: hasMatch
        ? topPassages.map((p) => ({
            id: p.id,
            page: p.page,
            section: p.section,
            text: p.text,
          }))
        : [],
      language,
      query: effectiveQuery,
      timestamp: new Date().toISOString(),
    });
  } catch (error: any) {
    console.error("Chat API error:", error);
    return NextResponse.json(
      { error: error?.message || "Internal server error" },
      { status: 500 }
    );
  }
}
