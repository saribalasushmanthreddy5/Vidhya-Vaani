import { NextRequest, NextResponse } from "next/server";
import { TEXTBOOK_CHUNKS, getRandomizedCuratedQuiz } from "@/lib/textbookData";

export const dynamic = "force-dynamic";

export async function POST(req: NextRequest) {
  let requestedChapter = "NCERT Class 10 Biology: Life Processes";
  try {
    const body = await req.json().catch(() => ({}));
    const { language = "English", chapter = "NCERT Class 10 Biology: Life Processes", seed = Date.now() } = body;
    requestedChapter = chapter;

    const apiKey = process.env.GEMINI_API_KEY;
    const candidateModels = [
      process.env.GEMINI_MODEL,
      "gemini-3.5-flash-lite",
      "gemini-3.5-flash",
      "gemini-flash-lite-latest",
      "gemini-3.8-flash",
    ].filter(Boolean) as string[];

    // Filter textbook chunks to the requested chapter, or fallback to all
    const chapLower = chapter.toLowerCase();
    let relevantChunks = TEXTBOOK_CHUNKS.filter((c) => {
      const cLower = c.chapter.toLowerCase();
      if (chapLower.includes("chem")) return cLower.includes("chem");
      if (chapLower.includes("phys") || chapLower.includes("light")) return cLower.includes("phys") || cLower.includes("light");
      if (chapLower.includes("bio") || chapLower.includes("life")) return cLower.includes("bio") || cLower.includes("life");
      return cLower.includes(chapLower);
    });
    if (relevantChunks.length === 0) relevantChunks = TEXTBOOK_CHUNKS;

    // Pick 4-5 random chunks from relevant chapter to inject fresh conceptual focus every time
    const shuffled = [...relevantChunks].sort(() => Math.random() - 0.5);
    const randomizedChunks = shuffled.slice(0, 5);
    const contextSample = randomizedChunks
      .map((c) => `[${c.chapter} - Page ${c.page} - ${c.section}]: ${c.text}`)
      .join("\n\n");

    const prompt = `You are VidyaVaani AI, generating a FRESH, UNIQUE 5-question multiple-choice quiz for Indian school students on "${chapter}".
Target Language: ${language}
Session Nonce: ${seed}_${Math.random().toString(36).substring(7)}

Textbook Excerpts:
${contextSample}

Instructions:
1. Generate EXACTLY 5 questions based on these concepts from "${chapter}".
2. Ensure the questions and options are varied, testing conceptual understanding (definition, equation, formula, experiment, or everyday application).
3. DO NOT repeat common default questions; formulate novel questions in ${language}.
4. Return strictly a raw JSON array of 5 objects without markdown fences, intro, or outro.

Required JSON Structure:
[
  {
    "question": "Clear question text in ${language}",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "topic": "Concise concept name",
    "explanation": "Clear explanation referencing [Page X]",
    "page": 1
  }
]`;

    if (apiKey) {
      for (const model of candidateModels) {
        try {
          const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
          const resp = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              contents: [{ role: "user", parts: [{ text: prompt }] }],
              generationConfig: {
                temperature: 0.85,
                maxOutputTokens: 1200,
              },
            }),
          });

          if (resp.ok) {
            const data = await resp.json();
            const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text || "";

            // Robust JSON extraction finding outermost array brackets
            const match = rawText.match(/\[\s*\{[\s\S]*\}\s*\]/);
            const cleanJson = match ? match[0] : rawText.replace(/```(?:json)?/gi, "").replace(/```/g, "").trim();

            const parsed = JSON.parse(cleanJson);
            if (Array.isArray(parsed) && parsed.length >= 4) {
              const validated = parsed.slice(0, 5).map((item, idx) => ({
                question: String(item.question || `Question ${idx + 1}`),
                options:
                  Array.isArray(item.options) && item.options.length === 4
                    ? item.options.map(String)
                    : ["Option A", "Option B", "Option C", "Option D"],
                correct_index:
                  typeof item.correct_index === "number" && item.correct_index >= 0 && item.correct_index < 4
                    ? item.correct_index
                    : 0,
                topic: String(item.topic || `${chapter} Core Concept`),
                explanation: String(item.explanation || "Grounded in NCERT textbook."),
                page: Number(item.page || 1),
              }));

              return NextResponse.json(
                { quiz: validated, source: "dynamic-ai", seed, chapter },
                { headers: { "Cache-Control": "no-store, max-age=0" } }
              );
            }
          }
        } catch {
          // Continue to next candidate model
        }
      }
    }

    // Dynamic Fallback: Randomly sample and shuffle 5 questions from the 40-question bank for this chapter
    const dynamicFallback = getRandomizedCuratedQuiz(requestedChapter);
    return NextResponse.json(
      { quiz: dynamicFallback, source: "curated-randomized", seed, chapter: requestedChapter },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  } catch (error: any) {
    console.error("Quiz API error:", error);
    const dynamicFallback = getRandomizedCuratedQuiz(requestedChapter);
    return NextResponse.json(
      { quiz: dynamicFallback, source: "fallback-safe", error: error?.message, chapter: requestedChapter },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  }
}
