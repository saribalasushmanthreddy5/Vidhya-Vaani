export interface LanguageMeta {
  code: string;
  label: string;
  bcp47: string;
  greeting: string;
  ui: {
    ask_tab: string;
    quiz_tab: string;
    library_tab: string;
    simpler_btn: string;
    example_btn: string;
  };
}

export const LANGUAGES: Record<string, LanguageMeta> = {
  English: {
    code: "en",
    label: "English (Indian Accent)",
    bcp47: "en-IN",
    greeting: "Hello and welcome! I am VidyaVaani, your grounded AI tutor.",
    ui: {
      ask_tab: "🗣️ Ask Tutor",
      quiz_tab: "📝 Practice Quiz",
      library_tab: "📚 Subjects Library",
      simpler_btn: "Explain Simpler",
      example_btn: "Give an Example",
    },
  },
  Hindi: {
    code: "hi",
    label: "हिंदी (Hindi)",
    bcp47: "hi-IN",
    greeting: "नमस्ते! मैं विद्यावाणी हूँ, आपकी पाठ्यपुस्तक-आधारित एआई शिक्षिका।",
    ui: {
      ask_tab: "🗣️ शिक्षक से पूछें",
      quiz_tab: "📝 अभ्यास प्रश्नोत्तरी",
      library_tab: "📚 विषय पुस्तकालय",
      simpler_btn: "सरल भाषा में समझाएं",
      example_btn: "एक उदाहरण दें",
    },
  },
  Kannada: {
    code: "kn",
    label: "ಕನ್ನಡ (Kannada)",
    bcp47: "kn-IN",
    greeting: "ನಮಸ್ಕಾರ! ನಾನು ವಿದ್ಯಾವಾಣಿ, ನಿಮ್ಮ ಪಠ್ಯಪುಸ್ತಕ-ಆಧಾರಿತ AI ಶಿಕ್ಷಕಿ.",
    ui: {
      ask_tab: "🗣️ ಶಿಕ್ಷಕರನ್ನು ಕೇಳಿ",
      quiz_tab: "📝 ಅಭ್ಯಾಸ ರಸಪ್ರಶ್ನೆ",
      library_tab: "📚 ವಿಷಯ ಗ್ರಂಥಾಲಯ",
      simpler_btn: "ಸರಳವಾಗಿ ವಿವರಿಸಿ",
      example_btn: "ಉದಾಹರಣೆ ನೀಡಿ",
    },
  },
  Telugu: {
    code: "te",
    label: "తెలుగు (Telugu)",
    bcp47: "te-IN",
    greeting: "నమస్కారం! నేను విద్యావాణిని, మీ పాఠ్యపుస్తక ఆధారిత AI ట్యూటర్.",
    ui: {
      ask_tab: "🗣️ ట్యూటర్‌ని అడగండి",
      quiz_tab: "📝 ప్రాక్టీస్ క్విజ్",
      library_tab: "📚 సబ్జెక్ట్స్ లైబ్రరీ",
      simpler_btn: "సులభంగా వివరించండి",
      example_btn: "ఒక ఉదాహరణ ఇవ్వండి",
    },
  },
  Tamil: {
    code: "ta",
    label: "தமிழ் (Tamil)",
    bcp47: "ta-IN",
    greeting: "வணக்கம்! நான் வித்யாவாணி, உங்கள் பாடப்புத்தக அடிப்படையிலான AI ஆசிரியர்.",
    ui: {
      ask_tab: "🗣️ ஆசிரியரிடம் கேளுங்கள்",
      quiz_tab: "📝 பயிற்சி வினாடி வினா",
      library_tab: "📚 பாட நூலகம்",
      simpler_btn: "எளிமையாக விளக்குங்கள்",
      example_btn: "ஒரு உதாரணம் கொடுங்கள்",
    },
  },
  Malayalam: {
    code: "ml",
    label: "മലയാളം (Malayalam)",
    bcp47: "ml-IN",
    greeting: "നമസ്കാരം! ഞാൻ വിദ്യാവാണി, നിങ്ങളുടെ പാഠപുസ്തക അടിസ്ഥാനമാക്കിയുള്ള AI അധ്യാപിക.",
    ui: {
      ask_tab: "🗣️ അധ്യാപകനോട് ചോദിക്കുക",
      quiz_tab: "📝 പരിശീലന ക്വിസ്",
      library_tab: "📚 വിഷയ ലൈബ്രറി",
      simpler_btn: "ലളിതമായി വിശദീകരിക്കുക",
      example_btn: "ഒരു ഉദാഹരണം നൽകുക",
    },
  },
  Marathi: {
    code: "mr",
    label: "मराठी (Marathi)",
    bcp47: "mr-IN",
    greeting: "नमस्कार! मी विद्यावाणी, तुमची पाठ्यपुस्तक-आधारित AI शिक्षिका.",
    ui: {
      ask_tab: "🗣️ शिक्षकांना विचारा",
      quiz_tab: "📝 सराव प्रश्नमंजुषा",
      library_tab: "📚 विषय ग्रंथालय",
      simpler_btn: "सोप्या भाषेत समजावून सांगा",
      example_btn: "एक उदाहरण द्या",
    },
  },
  Bengali: {
    code: "bn",
    label: "বাংলা (Bengali)",
    bcp47: "bn-IN",
    greeting: "নমস্কার! আমি বিদ্যাবাণী, আপনার পাঠ্যবই-ভিত্তিক এআই গৃহশিক্ষক।",
    ui: {
      ask_tab: "🗣️ শিক্ষককে জিজ্ঞাসা করুন",
      quiz_tab: "📝 কুইজ অনুশীলন",
      library_tab: "📚 বিষয় গ্রন্থাগার",
      simpler_btn: "সহজ ভাষায় ব্যাখ্যা করুন",
      example_btn: "একটি উদাহরণ দিন",
    },
  },
  Gujarati: {
    code: "gu",
    label: "ગુજરાતી (Gujarati)",
    bcp47: "gu-IN",
    greeting: "નમસ્તે! હું વિદ્યાવાણી છું, તમારી પાઠ્યપુસ્તક-આધારિત AI શિક્ષિકા.",
    ui: {
      ask_tab: "🗣️ શિક્ષકને પૂછો",
      quiz_tab: "📝 પ્રેક્ટિસ ક્વિઝ",
      library_tab: "📚 વિષય લાયબ્રેરી",
      simpler_btn: "સરળ રીતે સમજાવો",
      example_btn: "એક ઉદાહરણ આપો",
    },
  },
};

export interface TextbookChunk {
  id: string;
  chapter: string;
  page: number;
  section: string;
  text: string;
  keywords: string[];
}

export const TEXTBOOK_CHUNKS: TextbookChunk[] = [
  {
    id: "chunk_1",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 1,
    section: "What are Life Processes & Autotrophic Nutrition",
    text: "All living organisms perform basic maintenance functions to keep themselves alive, even when resting. These maintenance jobs are called life processes. Energy comes from outside the body in the form of food. Autotrophic organisms like green plants take in substances from outside and convert them into stored forms of energy through photosynthesis.",
    keywords: ["life processes", "maintenance", "autotrophic", "energy", "nutrition", "food"],
  },
  {
    id: "chunk_2",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 1,
    section: "Photosynthesis Chemical Equation & Steps",
    text: "Definition: Photosynthesis is the process by which green plants synthesize organic food (carbohydrates) from carbon dioxide (CO2) and water (H2O) using solar energy trapped by chlorophyll, releasing oxygen.\nChemical Equation: 6CO2 + 12H2O + Sunlight + Chlorophyll ---> C6H12O6 (Glucose) + 6O2 + 6H2O.\nSteps:\n1. Absorption of light energy by chlorophyll in chloroplasts.\n2. Conversion of light energy to chemical energy and splitting of water into hydrogen and oxygen.\n3. Reduction of carbon dioxide to carbohydrates (glucose).",
    keywords: ["photosynthesis", "equation", "chlorophyll", "chloroplast", "glucose", "co2", "h2o", "oxygen", "solar energy", "light energy"],
  },
  {
    id: "chunk_3",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 2,
    section: "Structure and Function of Stomata & Guard Cells",
    text: "Stomata are microscopic pores found on the surface of leaves through which massive amounts of gaseous exchange take place for photosynthesis. Each stomatal pore is flanked by kidney-shaped guard cells. When water flows into guard cells, they swell, become turgid, and open the stomatal pore. When guard cells lose water, they shrink and become flaccid, closing the pore.",
    keywords: ["stomata", "guard cells", "pore", "leaf", "leaves", "gas exchange", "turgid", "flaccid", "water"],
  },
  {
    id: "chunk_4",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 2,
    section: "Desert Plant Adaptations & Mineral Nutrients",
    text: "Desert plants take up carbon dioxide at night when temperatures are cooler to minimize water loss through transpiration. They synthesize an intermediate acid acted upon during the day by sunlight energy. Terrestrial plants absorb water and essential minerals like Nitrogen, Phosphorus, Iron, and Magnesium from soil. Nitrogen is vital for synthesizing proteins.",
    keywords: ["desert plants", "night", "transpiration", "nitrogen", "soil", "minerals", "phosphorus", "iron", "magnesium", "protein"],
  },
  {
    id: "chunk_5",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 3,
    section: "Heterotrophic Nutrition Types",
    text: "Heterotrophs depend on organic substances synthesized by autotrophs. Saprophytes break down food outside the body and absorb it (bread moulds, yeast, mushrooms). Parasites derive nutrition without killing the host (Cuscuta/Amarbel, ticks, tapeworms). Holozoic organisms ingest complex organic food and digest it internally (Amoeba, Humans).",
    keywords: ["heterotrophic", "saprophytic", "parasitic", "holozoic", "amoeba", "fungi", "cuscuta", "host", "nutrition"],
  },
  {
    id: "chunk_6",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 3,
    section: "Human Alimentary Canal & Stomach Digestion (HCl & Pepsin)",
    text: "In the mouth, salivary amylase breaks starch into simple sugars (maltose). In the stomach, gastric glands secrete:\n1. Hydrochloric Acid (HCl): Creates an acidic pH (1.5-2.5) necessary for pepsin to act and kills ingested pathogens.\n2. Pepsin: A protein-digesting enzyme breaking proteins into peptones.\n3. Mucus: Protects the inner stomach lining from excoriation by HCl.",
    keywords: ["stomach", "hcl", "hydrochloric acid", "pepsin", "mucus", "salivary amylase", "mouth", "digestion", "acid", "gastric"],
  },
  {
    id: "chunk_7",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 3,
    section: "Small Intestine: Bile Juice, Pancreatic Enzymes, and Villi",
    text: "The small intestine is the site of complete digestion of carbohydrates, proteins, and fats. Bile juice from the liver makes the acidic food alkaline and emulsifies large fat globules into small micelles. Pancreatic juice contains Trypsin (digests proteins) and Lipase (breaks down emulsified fats). Intestinal villi increase the surface area for rapid nutrient absorption into blood capillaries.",
    keywords: ["small intestine", "bile juice", "liver", "pancreas", "trypsin", "lipase", "villi", "emulsify", "fats", "absorption"],
  },
  {
    id: "chunk_8",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 4,
    section: "Breakdown of Glucose: Aerobic vs Anaerobic Respiration",
    text: "Cellular respiration breaks down 6-carbon glucose in the cytoplasm into two 3-carbon pyruvate molecules.\n1. Aerobic Respiration (in Mitochondria with O2): Produces CO2, H2O, and 38 ATP molecules per glucose.\n2. Anaerobic Fermentation in Yeast (without O2): Produces Ethanol (C2H5OH), CO2, and 2 ATP.\n3. Anaerobic in Muscle Cells (lack of O2): Produces Lactic acid and 2 ATP. Rapid accumulation of lactic acid causes muscle cramps during vigorous exercise.",
    keywords: ["respiration", "aerobic", "anaerobic", "mitochondria", "pyruvate", "atp", "glucose", "yeast", "ethanol", "lactic acid", "muscle cramps", "exercise"],
  },
  {
    id: "chunk_9",
    chapter: "NCERT Class 10 Science - Chapter 6: Life Processes",
    page: 4,
    section: "Human Lungs and Alveoli Surface",
    text: "Within human lungs, the respiratory passage branches repeatedly into smaller tubes ending in tiny balloon-like structures called Alveoli. Alveoli provide an extensive, ultra-thin moist surface lined with an extensive network of blood capillaries for rapid gaseous exchange between oxygen and carbon dioxide.",
    keywords: ["lungs", "alveoli", "respiratory", "capillaries", "gas exchange", "oxygen", "co2", "breathing"],
  },
  {
    id: "chunk_10",
    chapter: "NCERT Class 10 Science - Chapter 2: Acids, Bases and Salts",
    page: 18,
    section: "Common Salt (Sodium Chloride - NaCl) & Chemical Properties",
    text: "Sodium Chloride (NaCl), commonly known as table salt or common salt, is formed by the neutralization reaction between Hydrochloric Acid (HCl) and Sodium Hydroxide (NaOH): HCl + NaOH ---> NaCl + H2O. It is an essential raw material for producing chemicals like Sodium Hydroxide (caustic soda), Baking Soda (NaHCO3), Washing Soda (Na2CO3.10H2O), and Bleaching Powder (CaOCl2). In living organisms, sodium ions are vital for nerve impulse transmission and electrolyte balance.",
    keywords: ["nacl", "sodium chloride", "salt", "common salt", "neutralization", "naoh", "hcl", "table salt", "acids", "bases", "salts"],
  },
  {
    id: "chunk_11",
    chapter: "NCERT Class 10 Science - Chapter 13: Magnetic Effects of Electric Current",
    page: 224,
    section: "Magnetism, Magnetic Field & Field Lines",
    text: "Magnetism is a fundamental physical force mediated by magnetic fields. A magnet produces a region of influence around itself called a Magnetic Field. Hans Christian Oersted in 1820 discovered that an electric current carrying wire produces an associated magnetic field around it. Magnetic field lines emerge from the North pole and merge at the South pole outside the magnet, forming continuous closed loops.",
    keywords: ["magnetism", "magnet", "magnetic field", "magnetic", "field lines", "north pole", "south pole", "oersted", "electric current", "electromagnetism"],
  },
  {
    id: "chunk_12",
    chapter: "NCERT Class 10 Science - Chapter 1: Chemical Reactions and Equations",
    page: 6,
    section: "Chemical Equations, Balancing & Types of Reactions",
    text: "A chemical reaction involves chemical change where reactants transform into new products with different properties. Chemical reactions are represented by balanced chemical equations where the number of atoms of each element remains conserved according to the Law of Conservation of Mass. Major types include Combination, Decomposition, Displacement, Double Displacement, and Redox (Oxidation-Reduction) reactions.",
    keywords: ["chemical reaction", "chemical reactions", "equations", "reactants", "products", "oxidation", "reduction", "displacement", "balancing"],
  },
];

export function retrieveRelevantPassages(query: string, topK: number = 3): { chunk: TextbookChunk; score: number; isRelevant: boolean }[] {
  const qTokens = query.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);

  const scored = TEXTBOOK_CHUNKS.map((chunk) => {
    let score = 0;
    const textLower = chunk.text.toLowerCase();
    const secLower = chunk.section.toLowerCase();

    for (const token of qTokens) {
      if (token.length < 2) continue;
      // Exact word match
      if (secLower.includes(token)) score += 4.0;
      if (textLower.includes(token)) score += 2.0;
      if (chunk.keywords.some((kw) => kw.toLowerCase() === token || kw.toLowerCase().includes(token))) score += 5.0;
    }

    return { chunk, score, isRelevant: score > 0 };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK);
}

export function getCuratedPrompts(languageKey: string = "English") {
  if (languageKey === "Hindi") {
    return [
      { label: "प्रकाश संश्लेषण क्या है? 🌱", query: "प्रकाश संश्लेषण की रासायनिक समीकरण क्या है?" },
      { label: "वायवीय और अवायवीय श्वसन 🫀", query: "वायवीय और अवायवीय श्वसन में क्या अंतर है?" },
      { label: "आमाशय में HCl की भूमिका 🧪", query: "आमाशय में हाइड्रोक्लोरिक अम्ल (HCl) की क्या भूमिका है?" },
      { label: "द्वार कोशिकाएं कैसे खुलती हैं? 🍃", query: "द्वार कोशिकाएं रंध्रों को कैसे खोलती और बंद करती हैं?" },
      { label: "मांसपेशियों में ऐंठन और लैक्टिक एसिड ⚡", query: "व्यायाम के दौरान मांसपेशियों में लैक्टिक एसिड क्यों बनता है?" },
    ];
  } else if (languageKey === "Kannada") {
    return [
      { label: "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆ ಎಂದರೇನು? 🌱", query: "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ರಾಸಾಯನಿಕ ಸಮೀಕರಣವೇನು?" },
      { label: "ವಾಯುವಿಕ vs ಅವಾಯುವಿಕ ಉಸಿರಾಟ 🫀", query: "ವಾಯುವಿಕ ಮತ್ತು ಅವಾಯುವಿಕ ಉಸಿರಾಟದ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?" },
      { label: "ಜಠರದಲ್ಲಿ HCl ಆಮ್ಲದ ಪಾತ್ರ 🧪", query: "ಜಠರದಲ್ಲಿ ಹೈಡ್ರೋಕ್ಲೋರಿಕ್ ಆಮ್ಲದ (HCl) ಪಾತ್ರವೇನು?" },
      { label: "ಕಾವಲು ಕೋಶಗಳ ಕಾರ್ಯವಿಧಾನ 🍃", query: "ಕಾವಲು ಕೋಶಗಳು ಪತ್ರರಂಧ್ರಗಳನ್ನು ಹೇಗೆ ತೆರೆಯುತ್ತವೆ ಮತ್ತು ಮುಚ್ಚುತ್ತವೆ?" },
      { label: "ಸ್ನಾಯುಗಳಲ್ಲಿ ಲ್ಯಾಕ್ಟಿಕ್ ಆಮ್ಲ ⚡", query: "ವ್ಯಾಯಾಮದ ಸಮಯದಲ್ಲಿ ಸ್ನಾಯು ಕೋಶಗಳಲ್ಲಿ ಲ್ಯಾಕ್ಟಿಕ್ ಆಮ್ಲ ಏಕೆ ಸಂಗ್ರಹವಾಗುತ್ತದೆ?" },
    ];
  } else if (languageKey === "Telugu") {
    return [
      { label: "కిరణజన్య సంయోగక్రియ సమీకరణం 🌱", query: "కిరణజన్య సంయోగక్రియ రసాయన సమీకరణం ఏమిటి?" },
      { label: "వాయు సహిత vs అవాయు శ్వాసక్రియ 🫀", query: "వాయు సహిత మరియు అవాయు శ్వాసక్రియ మధ్య తేడా ఏమిటి?" },
      { label: "జీర్ణాశయంలో HCl పాత్ర 🧪", query: "జీర్ణాశయంలో హైడ్రోక్లోరిక్ ఆమ్లం (HCl) పాత్ర ఏమిటి?" },
      { label: "రక్షక కణాలు మరియు పత్రరంధ్రాలు 🍃", query: "రక్షక కణాలు పత్రరంధ్రాలను ఎలా తెరుస్తాయి మరియు మూస్తాయి?" },
      { label: "కండరాల నొప్పులు & లాక్టిక్ ఆమ్లం ⚡", query: "వ్యాయామం చేసేటప్పుడు కండరాలలో లాక్టిక్ ఆమ్లం ఎందుకు పేరుకుపోతుంది?" },
    ];
  } else {
    return [
      { label: "What is Photosynthesis? 🌱", query: "What is the chemical equation of photosynthesis and how does it synthesize glucose?" },
      { label: "Aerobic vs Anaerobic Respiration 🫀", query: "What is the difference between aerobic and anaerobic respiration in terms of ATP?" },
      { label: "Role of HCl & Pepsin in Stomach 🧪", query: "What is the role of hydrochloric acid (HCl) and pepsin secreted in the stomach?" },
      { label: "How Guard Cells Open Stomata 🍃", query: "How do guard cells regulate the opening and closing of stomata in leaves?" },
      { label: "Why do Muscles Cramp during Exercise? ⚡", query: "Why does lactic acid accumulate in muscle cells during vigorous exercise?" },
    ];
  }
}
