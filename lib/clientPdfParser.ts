import { TextbookChunk } from "./textbookData";

// Dynamically load PDF.js from CDN with worker
let pdfjsPromise: Promise<any> | null = null;

function loadPdfJs(): Promise<any> {
  if (typeof window === "undefined") {
    return Promise.reject(new Error("PDF.js can only be loaded in a browser environment."));
  }

  if ((window as any).pdfjsLib) {
    return Promise.resolve((window as any).pdfjsLib);
  }

  if (pdfjsPromise) return pdfjsPromise;

  pdfjsPromise = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
    script.async = true;
    script.onload = () => {
      const pdfjs = (window as any).pdfjsLib;
      if (pdfjs) {
        pdfjs.GlobalWorkerOptions.workerSrc =
          "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
        resolve(pdfjs);
      } else {
        reject(new Error("pdfjsLib not found on window after script load."));
      }
    };
    script.onerror = () => reject(new Error("Failed to load PDF.js from CDN."));
    document.head.appendChild(script);
  });

  return pdfjsPromise;
}

export function extractKeywords(text: string): string[] {
  const stopWords = new Set([
    "the", "and", "is", "in", "to", "of", "it", "with", "as", "for", "on", "at",
    "by", "this", "that", "from", "are", "be", "or", "an", "which", "can", "have",
    "has", "had", "was", "were", "but", "not", "into", "all", "also", "their", "more",
    "such", "when", "then", "will", "would", "they", "there", "about", "other"
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

export async function parsePdfLocallyInBrowser(
  file: File,
  onProgress?: (status: string) => void
): Promise<{
  pages: { pageNum: number; text: string }[];
  totalPages: number;
}> {
  onProgress?.("⚡ Initializing fast local PDF reader...");
  const pdfjs = await loadPdfJs();

  onProgress?.("⚡ Reading document into memory...");
  const arrayBuffer = await file.arrayBuffer();

  onProgress?.("⚡ Scanning document pages...");
  const loadingTask = pdfjs.getDocument({
    data: new Uint8Array(arrayBuffer),
    disableFontFace: true,
  });

  const pdf = await loadingTask.promise;
  // Read first 30 pages for lightning-fast performance (covers full chapter)
  const maxPages = Math.min(pdf.numPages, 30);
  const validPages: { pageNum: number; text: string }[] = [];

  for (let i = 1; i <= maxPages; i++) {
    onProgress?.(`⚡ Extracting text from page ${i} of ${maxPages}...`);
    try {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const strings = textContent.items.map((item: any) => item.str || "").filter(Boolean);
      const pageText = strings.join(" ").replace(/\s+/g, " ").trim();

      if (pageText.length > 30) {
        validPages.push({ pageNum: i, text: pageText });
      }
    } catch (e) {
      console.warn(`Could not extract page ${i}:`, e);
    }
  }

  return { pages: validPages, totalPages: pdf.numPages };
}

export function buildChunksFromPages(
  pages: { pageNum: number; text: string }[],
  chapterTitle: string,
  chapterId: string
): TextbookChunk[] {
  const chunks: TextbookChunk[] = [];

  pages.forEach((p) => {
    const rawParagraphs = p.text
      .split(/(?<=[.!?])\s+/)
      .map((s) => s.trim())
      .filter((s) => s.length > 20);

    let currentSentences: string[] = [];
    let currentWords = 0;

    const commitChunk = () => {
      if (currentSentences.length === 0) return;
      const joined = currentSentences.join(" ");
      const section =
        currentSentences[0].slice(0, 50).replace(/[^a-zA-Z0-9\s]/g, "").trim() ||
        `Page ${p.pageNum} Core Concept`;

      chunks.push({
        id: `${chapterId}_p${p.pageNum}_c${chunks.length + 1}`,
        chapter: chapterTitle,
        page: p.pageNum,
        section,
        text: joined,
        keywords: extractKeywords(joined),
      });

      currentSentences = [];
      currentWords = 0;
    };

    for (const sent of rawParagraphs) {
      const wCount = sent.split(/\s+/).length;
      if (currentWords + wCount > 200 && currentSentences.length > 0) {
        commitChunk();
      }
      currentSentences.push(sent);
      currentWords += wCount;
    }
    commitChunk();
  });

  return chunks;
}
