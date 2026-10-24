import { NextRequest, NextResponse } from "next/server";
import { extractText } from "unpdf";
import { TextbookChunk, ChapterInfo } from "@/lib/textbookData";

export const dynamic = "force-dynamic";

function sanitizeFilename(name: string): string {
  return name.replace(/\.[^/.]+$/, "").replace(/[_-]/g, " ").trim();
}

function extractKeywords(text: string): string[] {
  const stopWords = new Set([
    "the", "and", "is", "in", "to", "of", "it", "with", "as", "for", "on", "at",
    "by", "this", "that", "from", "are", "be", "or", "an", "which", "can", "have",
    "has", "had", "was", "were", "but", "not", "into", "all", "also", "their", "more"
  ]);
  const tokens = text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 3 && !stopWords.has(w));

  const counts: Record<string, number> = {};
  tokens.forEach((t) => {
    counts[t] = (counts[t] || 0) + 1;
  });

  return Object.keys(counts)
    .sort((a, b) => counts[b] - counts[a])
    .slice(0, 10);
}

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;
    const userTitle = (formData.get("title") as string | null)?.trim();
    const userSubject = (formData.get("subject") as string | null)?.trim() || "Custom Subject";

    if (!file) {
      return NextResponse.json({ error: "No file uploaded. Please select a PDF or text file." }, { status: 400 });
    }

    const fileName = file.name || "Uploaded_Subject.pdf";
    const baseTitle = userTitle || sanitizeFilename(fileName);
    const chapterTitle = baseTitle.startsWith("NCERT") ? baseTitle : `Uploaded: ${baseTitle}`;
    const shortName = baseTitle.slice(0, 30);
    const chapterId = `custom_${Date.now()}_${Math.random().toString(36).substring(7)}`;

    const arrayBuffer = await file.arrayBuffer();
    const uint8Array = new Uint8Array(arrayBuffer);

    let pagesText: string[] = [];

    if (fileName.toLowerCase().endsWith(".pdf") || file.type === "application/pdf") {
      try {
        const extracted = await extractText(uint8Array, { mergePages: false });
        pagesText = Array.isArray(extracted.text) ? extracted.text : [String(extracted.text || "")];
      } catch (pdfErr: any) {
        console.warn("unpdf extraction error:", pdfErr);
        return NextResponse.json(
          { error: `Could not parse PDF: ${pdfErr?.message || "File might be password-protected or corrupt."}` },
          { status: 422 }
        );
      }
    } else {
      // Plain text or markdown file
      const rawText = new TextDecoder("utf-8").decode(uint8Array);
      // Paginate by ~350 words
      const words = rawText.split(/\s+/);
      const pageSize = 350;
      for (let i = 0; i < words.length; i += pageSize) {
        pagesText.push(words.slice(i, i + pageSize).join(" "));
      }
    }

    // Filter out completely blank pages
    const validPages = pagesText
      .map((t, idx) => ({ pageNum: idx + 1, text: t.trim() }))
      .filter((p) => p.text.length > 20);

    if (validPages.length === 0) {
      return NextResponse.json(
        {
          error:
            "No readable text found in this PDF. It may be a scanned image-only PDF without OCR selectable text.",
        },
        { status: 422 }
      );
    }

    // Chunk text per page
    const chunks: TextbookChunk[] = [];
    validPages.forEach((p) => {
      // Split page into paragraphs
      const paragraphs = p.text
        .split(/\n\s*\n/)
        .map((para) => para.replace(/\s+/g, " ").trim())
        .filter((para) => para.length > 40);

      if (paragraphs.length === 0) {
        paragraphs.push(p.text.replace(/\s+/g, " ").trim());
      }

      // Group short paragraphs to ~150-250 words
      let currentGroup: string[] = [];
      let currentWordCount = 0;

      const saveGroup = () => {
        if (currentGroup.length === 0) return;
        const joined = currentGroup.join("\n\n");
        const firstLine = currentGroup[0].slice(0, 60).replace(/[^a-zA-Z0-9\s]/g, "").trim();
        const section = firstLine || `Page ${p.pageNum} Concepts`;

        chunks.push({
          id: `${chapterId}_p${p.pageNum}_c${chunks.length + 1}`,
          chapter: chapterTitle,
          page: p.pageNum,
          section: section,
          text: joined,
          keywords: extractKeywords(joined),
        });

        currentGroup = [];
        currentWordCount = 0;
      };

      for (const para of paragraphs) {
        const wCount = para.split(/\s+/).length;
        if (currentWordCount + wCount > 220 && currentGroup.length > 0) {
          saveGroup();
        }
        currentGroup.push(para);
        currentWordCount += wCount;
      }
      saveGroup();
    });

    if (chunks.length === 0) {
      return NextResponse.json(
        { error: "Could not create textbook index chunks from this document." },
        { status: 422 }
      );
    }

    // AI summary and curated prompt generation
    let description = `Uploaded custom study module containing ${validPages.length} pages and ${chunks.length} indexed chunks.`;
    let curatedPrompts: Array<{ label: string; query: string }> = [
      {
        label: `Overview of ${shortName} 📖`,
        query: `Give me a clear conceptual overview of ${chapterTitle} based on the uploaded textbook.`,
      },
      {
        label: `Key terms & definitions 🔍`,
        query: `What are the key terms, laws, and definitions explained in ${chapterTitle}?`,
      },
      {
        label: `Important exam questions 📝`,
        query: `What are the top 3 most important questions that could be asked in exams from ${chapterTitle}?`,
      },
      {
        label: `Everyday examples 💡`,
        query: `Give an everyday, real-world intuitive example to help understand ${chapterTitle}.`,
      },
    ];

    const apiKey = process.env.GEMINI_API_KEY;
    if (apiKey) {
      try {
        const sampleContext = chunks.slice(0, 4).map((c) => `[Page ${c.page} - ${c.section}]: ${c.text}`).join("\n\n");
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key=${apiKey}`;

        const aiPrompt = `Analyze these excerpts from a newly uploaded student textbook file: "${chapterTitle}".
Text excerpts:
${sampleContext}

Provide a JSON object with:
1. "description": A concise, engaging 1-sentence summary of what this chapter teaches.
2. "prompts": An array of 4 student doubt questions (each with "label" under 30 chars with an emoji, and "query").

Return strictly valid JSON:
{
  "description": "...",
  "prompts": [
    { "label": "...", "query": "..." }
  ]
}`;

        const aiResp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ role: "user", parts: [{ text: aiPrompt }] }],
            generationConfig: { temperature: 0.3, maxOutputTokens: 600 },
          }),
        });

        if (aiResp.ok) {
          const aiData = await aiResp.json();
          const rawText = aiData.candidates?.[0]?.content?.parts?.[0]?.text || "";
          const match = rawText.match(/\{[\s\S]*\}/);
          if (match) {
            const parsed = JSON.parse(match[0]);
            if (parsed.description && typeof parsed.description === "string") {
              description = parsed.description;
            }
            if (Array.isArray(parsed.prompts) && parsed.prompts.length >= 3) {
              curatedPrompts = parsed.prompts.slice(0, 4).map((p: any) => ({
                label: String(p.label || "Study question ❓"),
                query: String(p.query || "Explain this topic"),
              }));
            }
          }
        }
      } catch (aiErr) {
        console.warn("AI metadata generation fallback:", aiErr);
      }
    }

    const chapter: ChapterInfo = {
      id: chapterId,
      title: chapterTitle,
      shortName,
      subject: userSubject,
      pages: validPages.length,
      chunks: chunks.length,
      description,
      isCustom: true,
    };

    return NextResponse.json({
      success: true,
      chapter,
      chunks,
      curatedPrompts,
      message: `Successfully indexed ${chunks.length} chunks across ${validPages.length} pages.`,
    });
  } catch (error: any) {
    console.error("Upload API error:", error);
    return NextResponse.json(
      { error: error?.message || "Failed to process and index the uploaded file." },
      { status: 500 }
    );
  }
}
