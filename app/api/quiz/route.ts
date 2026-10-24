import { NextRequest, NextResponse } from "next/server";
import { TEXTBOOK_CHUNKS } from "@/lib/textbookData";

export const dynamic = "force-dynamic";

interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  topic: string;
  explanation: string;
  page: number;
}

// Comprehensive Bank of 20 Curated NCERT Questions across all chapter concepts
const MASTER_QUESTION_BANK: QuizQuestion[] = [
  {
    question: "What is the primary site of complete digestion of carbohydrates, proteins, and fats in the human body?",
    options: ["Stomach", "Small Intestine", "Large Intestine", "Mouth"],
    correct_index: 1,
    topic: "Digestion & Small Intestine",
    explanation: "The small intestine is the site of complete digestion, assisted by bile juice and pancreatic enzymes.",
    page: 3
  },
  {
    question: "Which of the following describes the balanced chemical equation for Photosynthesis?",
    options: [
      "6CO2 + 12H2O + Sunlight + Chlorophyll ---> C6H12O6 + 6O2 + 6H2O",
      "C6H12O6 + 6O2 ---> 6CO2 + 6H2O + Energy",
      "6CO2 + 6H2O ---> C2H5OH + 2ATP",
      "Pyruvate ---> Lactic acid + 2ATP"
    ],
    correct_index: 0,
    topic: "Photosynthesis Equation",
    explanation: "Photosynthesis converts 6CO2 + 12H2O using light trapped by chlorophyll into glucose, oxygen, and water.",
    page: 1
  },
  {
    question: "Why does hydrochloric acid (HCl) secrete in the stomach during digestion?",
    options: [
      "To emulsify large fat globules",
      "To break down complex starch into maltose",
      "To create an acidic pH (1.5-2.5) that activates pepsin and destroys pathogens",
      "To absorb water and electrolytes from undigested food"
    ],
    correct_index: 2,
    topic: "Gastric Juice & Stomach Acid",
    explanation: "HCl creates an acidic pH (1.5-2.5) that activates inactive pepsinogen into active pepsin.",
    page: 3
  },
  {
    question: "During vigorous muscular exercise in humans, sudden painful muscle cramps occur due to the accumulation of:",
    options: ["Ethanol", "Lactic Acid", "Carbon Dioxide", "Hydrochloric Acid"],
    correct_index: 1,
    topic: "Cellular Respiration & Muscle Cramps",
    explanation: "Anaerobic respiration in human muscle cells produces lactic acid due to oxygen lack, causing cramps.",
    page: 4
  },
  {
    question: "How do guard cells control the opening and closing of the stomatal pore in plant leaves?",
    options: [
      "By changing temperature within the leaf",
      "By swelling when water enters to open the pore, and shrinking when water is lost to close it",
      "By producing chlorophyll crystals",
      "By releasing oxygen gas directly into the atmosphere"
    ],
    correct_index: 1,
    topic: "Stomatal Gas Exchange",
    explanation: "Water entering guard cells makes them turgid, opening the pore; losing water causes them to shrink and close.",
    page: 2
  },
  {
    question: "Which enzyme present in human saliva initiates the chemical digestion of dietary starch into maltose?",
    options: ["Pepsin", "Salivary Amylase", "Trypsin", "Lipase"],
    correct_index: 1,
    topic: "Mouth Digestion & Enzymes",
    explanation: "Salivary amylase breaks down complex starch molecules into simple disaccharide sugars (maltose).",
    page: 3
  },
  {
    question: "How do desert plants adapt their photosynthetic process to minimize transpiration water loss?",
    options: [
      "They absorb water directly from night air",
      "They take in carbon dioxide at night and form an intermediate acid acted upon by sunlight during the day",
      "They perform photosynthesis without using chlorophyll",
      "They close their stomata permanently throughout their life cycle"
    ],
    correct_index: 1,
    topic: "Desert Plant Adaptations",
    explanation: "Desert plants take up CO2 at night to reduce daytime transpiration when temperatures are extreme.",
    page: 2
  },
  {
    question: "What is the crucial biological role of mucus secreted by the gastric glands in the human stomach?",
    options: [
      "To digest dietary proteins into amino acids",
      "To protect the inner lining of the stomach from erosion by hydrochloric acid (HCl)",
      "To emulsify dietary fats into micelles",
      "To activate the protein enzyme trypsin"
    ],
    correct_index: 1,
    topic: "Stomach Mucus Protection",
    explanation: "Mucus forms a protective barrier preventing strong hydrochloric acid from excoriating the stomach wall.",
    page: 3
  },
  {
    question: "Which essential nutrient absorbed by terrestrial plants from the soil is vital for the synthesis of proteins?",
    options: ["Nitrogen", "Chlorine", "Helium", "Neon"],
    correct_index: 0,
    topic: "Plant Mineral Nutrition",
    explanation: "Nitrogen absorbed as nitrates or nitrites from soil is essential for plants to build amino acids and proteins.",
    page: 2
  },
  {
    question: "In cellular respiration, what is the fate of 6-carbon glucose during the initial cytoplasmic stage?",
    options: [
      "Direct conversion into 38 ATP molecules",
      "Breakdown into two 3-carbon molecules of pyruvate",
      "Conversion directly into ethanol and lactic acid",
      "Immediate release of carbon dioxide without energy"
    ],
    correct_index: 1,
    topic: "Glucose Breakdown & Glycolysis",
    explanation: "In cytoplasm, 6-carbon glucose is cleaved into two 3-carbon pyruvate molecules before entering mitochondria.",
    page: 4
  },
  {
    question: "What are the tiny balloon-like structures in human lungs that provide an ultra-thin surface for rapid gas exchange called?",
    options: ["Bronchioles", "Alveoli", "Villi", "Trachea"],
    correct_index: 1,
    topic: "Respiratory System & Alveoli",
    explanation: "Alveoli provide an extensive, ultra-thin moist surface lined with blood capillaries for rapid O2 and CO2 diffusion.",
    page: 4
  },
  {
    question: "Which of the following organisms exhibits saprophytic nutrition by breaking down food outside its body and then absorbing it?",
    options: ["Bread mould (Fungi)", "Amoeba", "Cuscuta (Amarbel)", "Tapeworm"],
    correct_index: 0,
    topic: "Heterotrophic Nutrition Types",
    explanation: "Saprophytes like bread moulds, yeast, and mushrooms secrete digestive enzymes outside and absorb nutrients.",
    page: 3
  },
  {
    question: "What role does bile juice secreted by the liver play in the small intestine?",
    options: [
      "Acidifies food and digests starch",
      "Makes acidic food alkaline and emulsifies large fat globules into smaller droplets",
      "Breaks proteins into peptones",
      "Absorbs excess water from undigested matter"
    ],
    correct_index: 1,
    topic: "Liver & Bile Emulsification",
    explanation: "Bile creates an alkaline medium for pancreatic enzymes and emulsifies fats so lipase can act efficiently.",
    page: 3
  },
  {
    question: "Which enzyme present in pancreatic juice is specifically responsible for digesting proteins into peptides?",
    options: ["Lipase", "Trypsin", "Pepsin", "Salivary amylase"],
    correct_index: 1,
    topic: "Pancreatic Enzymes",
    explanation: "Pancreatic trypsin acts in the alkaline small intestine to digest proteins into peptides and amino acids.",
    page: 3
  },
  {
    question: "What is the net energy yield (ATP) per glucose molecule during aerobic cellular respiration in mitochondria?",
    options: ["2 ATP", "38 ATP", "4 ATP", "12 ATP"],
    correct_index: 1,
    topic: "Aerobic Respiration Energy Yield",
    explanation: "Aerobic breakdown of glucose in the presence of oxygen in mitochondria yields approximately 38 ATP molecules.",
    page: 4
  },
  {
    question: "What are the tiny finger-like projections on the inner wall of the small intestine that maximize nutrient absorption?",
    options: ["Guard cells", "Alveoli", "Villi", "Cilia"],
    correct_index: 2,
    topic: "Intestinal Villi & Absorption",
    explanation: "Villi vastly increase the surface area of the intestinal mucosa and are richly supplied with blood vessels.",
    page: 3
  },
  {
    question: "What are the end products of anaerobic fermentation carried out by yeast cells in the absence of oxygen?",
    options: [
      "Lactic acid + 38 ATP",
      "Ethanol + Carbon Dioxide + 2 ATP",
      "Water + Carbon Dioxide + 38 ATP",
      "Pyruvate + Oxygen"
    ],
    correct_index: 1,
    topic: "Anaerobic Fermentation in Yeast",
    explanation: "In yeast, fermentation converts pyruvate anaerobically into Ethanol (C2H5OH), CO2, and 2 ATP molecules.",
    page: 4
  },
  {
    question: "Which of the following is a parasitic plant that derives nutrition directly from host plants without killing them?",
    options: ["Mushroom", "Cuscuta (Amarbel)", "Yeast", "Amoeba"],
    correct_index: 1,
    topic: "Parasitic Nutrition",
    explanation: "Cuscuta (Amarbel) is an ectoparasitic plant that taps into host vascular tissue for organic nutrients.",
    page: 3
  },
  {
    question: "Which organelle inside plant leaf cells contains the green pigment chlorophyll required to capture solar photons?",
    options: ["Mitochondria", "Chloroplast", "Ribosome", "Golgi apparatus"],
    correct_index: 1,
    topic: "Chloroplast & Photosynthesis",
    explanation: "Chloroplasts contain chlorophyll pigments that absorb light energy to drive the photosynthetic split of water.",
    page: 1
  },
  {
    question: "During photosynthesis, the splitting of water molecules (photolysis) releases which vital gas into the atmosphere?",
    options: ["Carbon Dioxide", "Nitrogen", "Oxygen", "Methane"],
    correct_index: 2,
    topic: "Photolysis & Oxygen Generation",
    explanation: "Splitting of water (H2O) into hydrogen and oxygen under light energy releases breathable oxygen gas.",
    page: 1
  }
];

// Fisher-Yates array shuffler
function shuffle<T>(array: T[]): T[] {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

// Generate a freshly shuffled set of questions with randomized option orders
function getRandomizedCuratedQuiz(): QuizQuestion[] {
  const chosen = shuffle(MASTER_QUESTION_BANK).slice(0, 5);
  return chosen.map((q) => {
    // Shuffle options while tracking the correct answer string
    const correctText = q.options[q.correct_index];
    const shuffledOptions = shuffle(q.options);
    const newCorrectIndex = shuffledOptions.indexOf(correctText);
    return {
      ...q,
      options: shuffledOptions,
      correct_index: newCorrectIndex
    };
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const { language = "English", seed = Date.now() } = body;

    const apiKey = process.env.GEMINI_API_KEY;
    const candidateModels = [
      process.env.GEMINI_MODEL,
      "gemini-3.5-flash-lite",
      "gemini-3.5-flash",
      "gemini-flash-lite-latest",
      "gemini-3.8-flash",
    ].filter(Boolean) as string[];

    // Pick 4-5 random chunks from textbook to inject fresh conceptual focus every time
    const randomizedChunks = shuffle(TEXTBOOK_CHUNKS).slice(0, 5);
    const contextSample = randomizedChunks
      .map(c => `[Page ${c.page} - ${c.section}]: ${c.text}`)
      .join("\n\n");

    const prompt = `You are VidyaVaani AI, generating a FRESH, UNIQUE 5-question multiple-choice quiz for Indian school students.
Target Language: ${language}
Session Nonce: ${seed}_${Math.random().toString(36).substring(7)}

Textbook Excerpts:
${contextSample}

Instructions:
1. Generate EXACTLY 5 questions based on these concepts.
2. Ensure the questions and options are varied, testing conceptual understanding (definition, equation, organ function, or everyday example).
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
                maxOutputTokens: 1200
              }
            })
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
                options: Array.isArray(item.options) && item.options.length === 4
                  ? item.options.map(String)
                  : ["Option A", "Option B", "Option C", "Option D"],
                correct_index: typeof item.correct_index === "number" && item.correct_index >= 0 && item.correct_index < 4
                  ? item.correct_index
                  : 0,
                topic: String(item.topic || "Life Processes Core Concept"),
                explanation: String(item.explanation || "Grounded in textbook."),
                page: Number(item.page || 1)
              }));

              return NextResponse.json(
                { quiz: validated, source: "dynamic-ai", seed },
                { headers: { "Cache-Control": "no-store, max-age=0" } }
              );
            }
          }
        } catch {
          // Continue to next candidate model
        }
      }
    }

    // Dynamic Fallback: Randomly sample and shuffle 5 questions from the 20-question bank
    const dynamicFallback = getRandomizedCuratedQuiz();
    return NextResponse.json(
      { quiz: dynamicFallback, source: "curated-randomized", seed },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  } catch (error: any) {
    console.error("Quiz API error:", error);
    const dynamicFallback = getRandomizedCuratedQuiz();
    return NextResponse.json(
      { quiz: dynamicFallback, source: "fallback-safe", error: error?.message },
      { headers: { "Cache-Control": "no-store, max-age=0" } }
    );
  }
}
