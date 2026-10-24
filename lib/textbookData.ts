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
      library_tab: "📚 विषय लायब्ररी",
      simpler_btn: "सोप्या भाषेत सांगा",
      example_btn: "उदाहरण द्या",
    },
  },
  Bengali: {
    code: "bn",
    label: "বাংলা (Bengali)",
    bcp47: "bn-IN",
    greeting: "নমস্কার! আমি বিদ্যাবাণী, আপনার পাঠ্যবই-ভিত্তিক এআই শিক্ষিকা।",
    ui: {
      ask_tab: "🗣️ শিক্ষককে জিজ্ঞাসা করুন",
      quiz_tab: "📝 অনুশীলন কুইজ",
      library_tab: "📚 বিষয় লাইব্রেরি",
      simpler_btn: "সহজভাবে ব্যাখ্যা করুন",
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
      library_tab: "📚 વિષય પુસ્તકાલય",
      simpler_btn: "સરળ રીતે સમજાવો",
      example_btn: "ઉદાહરણ આપો",
    },
  },
};

export interface ChapterInfo {
  id: string;
  title: string;
  shortName: string;
  subject: "Biology" | "Chemistry" | "Physics";
  pages: number;
  chunks: number;
  description: string;
}

export const CHAPTERS: ChapterInfo[] = [
  {
    id: "biology",
    title: "NCERT Class 10 Biology: Life Processes",
    shortName: "Life Processes",
    subject: "Biology",
    pages: 4,
    chunks: 9,
    description: "Autotrophic nutrition, stomata, human digestion, cellular respiration, and alveoli.",
  },
  {
    id: "chemistry",
    title: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    shortName: "Chemical Reactions",
    subject: "Chemistry",
    pages: 5,
    chunks: 11,
    description: "Balancing equations, combination, decomposition, displacement, double displacement, redox, and corrosion.",
  },
  {
    id: "physics",
    title: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    shortName: "Light & Optics",
    subject: "Physics",
    pages: 6,
    chunks: 14,
    description: "Laws of reflection, spherical mirrors, Snell's law, refractive index, lens formula, and power in Dioptres.",
  },
];

export interface TextbookChunk {
  id: string;
  chapter: string;
  page: number;
  section: string;
  text: string;
  keywords: string[];
}

export const TEXTBOOK_CHUNKS: TextbookChunk[] = [
  // ==========================================
  // 1. BIOLOGY: LIFE PROCESSES
  // ==========================================
  {
    id: "bio_1",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 1,
    section: "What are Life Processes & Autotrophic Nutrition",
    text: "All living organisms perform basic maintenance functions to keep themselves alive, even when resting. These maintenance jobs are called life processes. Energy comes from outside the body in the form of food. Autotrophic organisms like green plants take in substances from outside and convert them into stored forms of energy through photosynthesis.",
    keywords: ["life processes", "maintenance", "autotrophic", "energy", "nutrition", "food"],
  },
  {
    id: "bio_2",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 1,
    section: "Photosynthesis Chemical Equation & Steps",
    text: "Definition: Photosynthesis is the process by which green plants synthesize organic food (carbohydrates) from carbon dioxide (CO2) and water (H2O) using solar energy trapped by chlorophyll, releasing oxygen.\nChemical Equation: 6CO2 + 12H2O + Sunlight + Chlorophyll ---> C6H12O6 (Glucose) + 6O2 + 6H2O.\nSteps:\n1. Absorption of light energy by chlorophyll in chloroplasts.\n2. Conversion of light energy to chemical energy and splitting of water into hydrogen and oxygen.\n3. Reduction of carbon dioxide to carbohydrates (glucose).",
    keywords: ["photosynthesis", "equation", "chlorophyll", "chloroplast", "glucose", "co2", "h2o", "oxygen", "solar energy", "light energy"],
  },
  {
    id: "bio_3",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 2,
    section: "Structure and Function of Stomata & Guard Cells",
    text: "Stomata are microscopic pores found on the surface of leaves through which massive amounts of gaseous exchange take place for photosynthesis. Each stomatal pore is flanked by kidney-shaped guard cells. When water flows into guard cells, they swell, become turgid, and open the stomatal pore. When guard cells lose water, they shrink and become flaccid, closing the pore.",
    keywords: ["stomata", "guard cells", "pore", "leaf", "leaves", "gas exchange", "turgid", "flaccid", "water"],
  },
  {
    id: "bio_4",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 2,
    section: "Desert Plant Adaptations & Mineral Nutrients",
    text: "Desert plants take up carbon dioxide at night when temperatures are cooler to minimize water loss through transpiration. They synthesize an intermediate acid acted upon during the day by sunlight energy. Terrestrial plants absorb water and essential minerals like Nitrogen, Phosphorus, Iron, and Magnesium from soil. Nitrogen is vital for synthesizing proteins.",
    keywords: ["desert plants", "night", "transpiration", "nitrogen", "soil", "minerals", "phosphorus", "iron", "magnesium", "protein"],
  },
  {
    id: "bio_5",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 3,
    section: "Heterotrophic Nutrition Types",
    text: "Heterotrophs depend on organic substances synthesized by autotrophs. Saprophytes break down food outside the body and absorb it (bread moulds, yeast, mushrooms). Parasites derive nutrition without killing the host (Cuscuta/Amarbel, ticks, tapeworms). Holozoic organisms ingest complex organic food and digest it internally (Amoeba, Humans).",
    keywords: ["heterotrophic", "saprophytic", "parasitic", "holozoic", "amoeba", "fungi", "cuscuta", "host", "nutrition"],
  },
  {
    id: "bio_6",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 3,
    section: "Human Alimentary Canal & Stomach Digestion (HCl & Pepsin)",
    text: "In the mouth, salivary amylase breaks starch into simple sugars (maltose). In the stomach, gastric glands secrete:\n1. Hydrochloric Acid (HCl): Creates an acidic pH (1.5-2.5) necessary for pepsin to act and kills ingested pathogens.\n2. Pepsin: A protein-digesting enzyme breaking proteins into peptones.\n3. Mucus: Protects the inner stomach lining from excoriation by HCl.",
    keywords: ["stomach", "hcl", "hydrochloric acid", "pepsin", "mucus", "salivary amylase", "mouth", "digestion", "acid", "gastric"],
  },
  {
    id: "bio_7",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 3,
    section: "Small Intestine: Bile Juice, Pancreatic Enzymes, and Villi",
    text: "The small intestine is the site of complete digestion of carbohydrates, proteins, and fats. Bile juice from the liver makes the acidic food alkaline and emulsifies large fat globules into small micelles. Pancreatic juice contains Trypsin (digests proteins) and Lipase (breaks down emulsified fats). Intestinal villi increase the surface area for rapid nutrient absorption into blood capillaries.",
    keywords: ["small intestine", "bile juice", "liver", "pancreas", "trypsin", "lipase", "villi", "emulsify", "fats", "absorption"],
  },
  {
    id: "bio_8",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 4,
    section: "Breakdown of Glucose: Aerobic vs Anaerobic Respiration",
    text: "Cellular respiration breaks down 6-carbon glucose in the cytoplasm into two 3-carbon pyruvate molecules.\n1. Aerobic Respiration (in Mitochondria with O2): Produces CO2, H2O, and 38 ATP molecules per glucose.\n2. Anaerobic Fermentation in Yeast (without O2): Produces Ethanol (C2H5OH), CO2, and 2 ATP.\n3. Anaerobic in Muscle Cells (lack of O2): Produces Lactic acid and 2 ATP. Rapid accumulation of lactic acid causes muscle cramps during vigorous exercise.",
    keywords: ["respiration", "aerobic", "anaerobic", "mitochondria", "pyruvate", "atp", "glucose", "yeast", "ethanol", "lactic acid", "muscle cramps", "exercise"],
  },
  {
    id: "bio_9",
    chapter: "NCERT Class 10 Biology: Life Processes",
    page: 4,
    section: "Human Lungs and Alveoli Surface",
    text: "Within human lungs, the respiratory passage branches repeatedly into smaller tubes ending in tiny balloon-like structures called Alveoli. Alveoli provide an extensive, ultra-thin moist surface lined with an extensive network of blood capillaries for rapid gaseous exchange between oxygen and carbon dioxide.",
    keywords: ["lungs", "alveoli", "respiratory", "capillaries", "gas exchange", "oxygen", "co2", "breathing"],
  },

  // ==========================================
  // 2. CHEMISTRY: CHEMICAL REACTIONS & EQUATIONS
  // ==========================================
  {
    id: "chem_1",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 1,
    section: "Chemical Equations & Law of Conservation of Mass",
    text: "A chemical reaction is represented by a balanced chemical equation. According to the Law of Conservation of Mass, mass can neither be created nor destroyed in a chemical reaction. Therefore, the total number of atoms of each element on the reactants side must equal the total number of atoms on the products side. Physical states are represented as (s) for solid, (l) for liquid, (g) for gas, and (aq) for aqueous solutions.",
    keywords: ["chemical reaction", "chemical equation", "balancing", "conservation of mass", "reactants", "products", "coefficients", "states"],
  },
  {
    id: "chem_2",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 2,
    section: "Combination Reactions & Quicklime",
    text: "In a Combination Reaction, two or more reactants combine to form a single product: A + B ---> AB. A key example is the reaction of Quicklime (Calcium Oxide - CaO) with water to form Slaked Lime (Calcium Hydroxide - Ca(OH)2): CaO(s) + H2O(l) ---> Ca(OH)2(aq) + Heat. This reaction is highly exothermic. Slaked lime is used for whitewashing walls, where it reacts slowly with atmospheric CO2 to form a shiny layer of Calcium Carbonate (CaCO3).",
    keywords: ["combination reaction", "quicklime", "calcium oxide", "slaked lime", "calcium hydroxide", "whitewashing", "exothermic", "caco3"],
  },
  {
    id: "chem_3",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 2,
    section: "Decomposition Reactions & Electrolysis of Water",
    text: "A Decomposition Reaction is one where a single compound breaks down into two or more simpler substances upon supply of heat (thermal), electricity (electrolytic), or light (photolytic). Thermal decomposition of Ferrous Sulphate: 2FeSO4(s) ---> Fe2O3(s) + SO2(g) + SO3(g). Electrolysis of water breaks H2O into Hydrogen and Oxygen gases in a 2:1 volume ratio collected at cathode and anode respectively. Silver Chloride turns grey in sunlight: 2AgCl(s) ---> 2Ag(s) + Cl2(g), used in black and white photography.",
    keywords: ["decomposition", "thermal decomposition", "electrolysis", "hydrogen", "oxygen", "silver chloride", "photography", "ferrous sulphate"],
  },
  {
    id: "chem_4",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 3,
    section: "Displacement and Double Displacement Reactions",
    text: "In a Displacement Reaction, a more reactive element displaces a less reactive element from its compound. For example, when an iron nail is dipped in blue Copper Sulphate solution: Fe(s) + CuSO4(aq) ---> FeSO4(aq) + Cu(s). The blue colour fades to light green as copper deposits on the iron nail. In a Double Displacement Reaction, there is an exchange of ions between reactants. Mixing Sodium Sulphate and Barium Chloride produces an insoluble white precipitate of Barium Sulphate: Na2SO4(aq) + BaCl2(aq) ---> BaSO4(s) [White Precipitate] + 2NaCl(aq).",
    keywords: ["displacement", "iron nail", "copper sulphate", "reactivity series", "double displacement", "barium sulphate", "precipitate", "precipitation"],
  },
  {
    id: "chem_5",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 4,
    section: "Redox Reactions (Oxidation & Reduction)",
    text: "Oxidation is defined as the gain of oxygen or the loss of hydrogen (or loss of electrons). Reduction is defined as the loss of oxygen or the gain of hydrogen (or gain of electrons). Reactions in which both oxidation and reduction occur simultaneously are called Redox Reactions. In CuO + H2 ---> Cu + H2O, Copper Oxide is reduced to copper, while Hydrogen is oxidized to water. Substance oxidized is the reducing agent; substance reduced is the oxidizing agent.",
    keywords: ["redox", "oxidation", "reduction", "cuo", "hydrogen", "oxidizing agent", "reducing agent", "electrons"],
  },
  {
    id: "chem_6",
    chapter: "NCERT Class 10 Chemistry: Chemical Reactions & Equations",
    page: 5,
    section: "Corrosion and Rancidity",
    text: "Corrosion is the gradual deterioration of metals caused by chemical or electrochemical reaction with atmospheric moisture, air, and acids. Rusting of iron forms hydrated iron(III) oxide: 4Fe + 3O2 + 2xH2O ---> 2Fe2O3.xH2O (Rust). Galvanization (coating iron with zinc) and painting prevent corrosion. Rancidity occurs when fats and oils in food are oxidized over time, producing an unpleasant smell and sour taste. It is prevented by adding antioxidants, packaging food in airtight containers, or flushing potato chip bags with unreactive Nitrogen gas.",
    keywords: ["corrosion", "rusting", "iron", "galvanization", "zinc", "rancidity", "fats", "oils", "antioxidants", "nitrogen"],
  },

  // ==========================================
  // 3. PHYSICS: LIGHT - REFLECTION AND REFRACTION
  // ==========================================
  {
    id: "phys_1",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 1,
    section: "Laws of Reflection & Spherical Mirrors",
    text: "Light travels in straight lines in homogeneous media. The Laws of Reflection state: 1. The angle of incidence (i) equals the angle of reflection (r): ∠i = ∠r. 2. The incident ray, the reflected ray, and the normal at the point of incidence all lie in the same plane. Spherical mirrors have curved reflecting surfaces: Concave mirrors curve inwards towards the center of curvature; Convex mirrors curve outwards. The focal length (f) of a spherical mirror of radius of curvature R is: f = R / 2.",
    keywords: ["light", "reflection", "laws of reflection", "concave mirror", "convex mirror", "focal length", "radius of curvature", "normal"],
  },
  {
    id: "phys_2",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 2,
    section: "Mirror Formula and Magnification",
    text: "The Mirror Formula connects object distance (u), image distance (v), and focal length (f): 1/v + 1/u = 1/f. According to Cartesian sign convention, the pole is taken as origin, object is placed to the left of the mirror (u is always negative). Linear Magnification (m) produced by a spherical mirror is the ratio of image height (h') to object height (h): m = h'/h = -v/u. A negative magnification indicates a real, inverted image; a positive magnification indicates a virtual, erect image.",
    keywords: ["mirror formula", "object distance", "image distance", "focal length", "magnification", "sign convention", "real image", "virtual image"],
  },
  {
    id: "phys_3",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 3,
    section: "Applications of Concave and Convex Mirrors",
    text: "Concave mirrors produce enlarged virtual images when the object is placed between the pole and focus. They are used in torches, vehicle headlights, solar furnaces (to concentrate intense solar radiation), and by dentists to inspect magnified teeth. Convex mirrors always form virtual, erect, and diminished images, providing a wide field of view. They are universally used as rear-view mirrors in automobiles to allow drivers to view traffic behind them safely.",
    keywords: ["concave mirror uses", "convex mirror uses", "rear-view mirror", "solar furnace", "dentist mirror", "diminished", "field of view"],
  },
  {
    id: "phys_4",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 4,
    section: "Refraction of Light and Snell's Law",
    text: "Refraction is the bending of light as it passes obliquely from one transparent optical medium to another of different optical density due to a change in the speed of light. Snell's Law of Refraction states: The ratio of the sine of the angle of incidence to the sine of the angle of refraction is constant for a given pair of media: sin(i) / sin(r) = constant = n21 (Refractive Index). When light travels from a rarer to a denser medium, it bends towards the normal; from denser to rarer, it bends away from the normal. Absolute refractive index n = c / v (speed of light in vacuum / speed of light in medium).",
    keywords: ["refraction", "snell's law", "refractive index", "speed of light", "rarer medium", "denser medium", "normal", "bending"],
  },
  {
    id: "phys_5",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 5,
    section: "Spherical Lenses & Lens Formula",
    text: "A lens is a transparent optical material bounded by two surfaces. A Convex Lens is thicker at the center and converges light rays to a real focus. A Concave Lens is thinner at the center and diverges light rays from a virtual focus. The Lens Formula connects object distance (u), image distance (v), and focal length (f): 1/v - 1/u = 1/f. Linear magnification for a lens is: m = h'/h = +v/u.",
    keywords: ["lens", "convex lens", "concave lens", "converging lens", "diverging lens", "lens formula", "magnification"],
  },
  {
    id: "phys_6",
    chapter: "NCERT Class 10 Physics: Light - Reflection and Refraction",
    page: 6,
    section: "Power of a Lens & Dioptres",
    text: "The Power of a lens (P) is a measure of its ability to converge or diverge light rays. It is defined as the reciprocal of its focal length expressed in meters: P = 1 / f (in meters). The SI unit of lens power is the Dioptre (symbol D). One Dioptre is the power of a lens whose focal length is 1 meter (1 D = 1 m^-1). A convex lens has a positive focal length and positive power (+D), used for hypermetropia. A concave lens has a negative focal length and negative power (-D), used for myopia. For thin lenses placed in contact, net power is the algebraic sum: P = P1 + P2.",
    keywords: ["power of lens", "dioptre", "diopter", "focal length in meters", "myopia", "hypermetropia", "convex lens power", "concave lens power"],
  },
];

export function retrieveRelevantPassages(
  query: string,
  topK: number = 3,
  chapterFilter?: string
): { chunk: TextbookChunk; score: number; isRelevant: boolean }[] {
  const qTokens = query.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);

  const scored = TEXTBOOK_CHUNKS.map((chunk) => {
    let score = 0;
    const textLower = chunk.text.toLowerCase();
    const secLower = chunk.section.toLowerCase();
    const chapLower = chunk.chapter.toLowerCase();

    // Prioritize active chapter heavily if provided
    if (chapterFilter && chapLower.includes(chapterFilter.toLowerCase())) {
      score += 6.0;
    }

    for (const token of qTokens) {
      if (token.length < 2) continue;
      if (secLower.includes(token)) score += 4.0;
      if (textLower.includes(token)) score += 2.0;
      if (chunk.keywords.some((kw) => kw.toLowerCase() === token || kw.toLowerCase().includes(token))) score += 5.0;
    }

    return { chunk, score, isRelevant: score > 0 };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK);
}

export function getCuratedPrompts(languageKey: string = "English", chapterTitle?: string) {
  const chap = (chapterTitle || "").toLowerCase();

  // Chemistry Prompts
  if (chap.includes("chemistry") || chap.includes("chemical")) {
    if (languageKey === "Hindi") {
      return [
        { label: "संयोजन और वियोजन अभिक्रियाएं 🧪", query: "संयोजन और वियोजन अभिक्रिया में क्या अंतर है?" },
        { label: "बिना बुझा चूना और बुझा चूना 🧱", query: "क्विकलाइम और स्लेक्ड लाइम की रासायनिक अभिक्रिया क्या है?" },
        { label: "विस्थापन अभिक्रिया और कॉपर सल्फेट 🔵", query: "लोहे की कील डालने पर कॉपर सल्फेट का नीला रंग क्यों बदल जाता है?" },
        { label: "रेडॉक्स और संक्षारण (जंग लगना) 🛡️", query: "रेडॉक्स अभिक्रिया क्या है और लोहे पर जंग कैसे लगती है?" },
        { label: "चिप्स के पैकेट में नाइट्रोजन गैस क्यों भरते हैं? 🥔", query: "विकृतगंधिता (Rancidity) क्या है और नाइट्रोजन गैस क्यों भरी जाती है?" },
      ];
    } else if (languageKey === "Kannada") {
      return [
        { label: "ಸಂಯೋಗ ಮತ್ತು ವಿಭಜನೆ ಕ್ರಿಯೆಗಳು 🧪", query: "ಸಂಯೋಗ ಮತ್ತು ವಿಭಜನೆ ರಾಸಾಯನಿಕ ಕ್ರಿಯೆಗಳ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?" },
        { label: "ಸುಣ್ಣ ಮತ್ತು ನೀರಿನ ಕ್ರಿಯೆ 🧱", query: "ಕ್ವಿಕ್‌ಲೈಮ್ ಮತ್ತು ನೀರಿನ ನಡುವಿನ ರಾಸಾಯನಿಕ ಕ್ರಿಯೆ ಯಾವುದು?" },
        { label: "ತಾಮ್ರದ ಸಲ್ಫೇಟ್ ಮತ್ತು ಕಬ್ಬಿಣ 🔵", query: "ಕಬ್ಬಿಣದ ಮೊಳೆಯನ್ನು ತಾಮ್ರದ ಸಲ್ಫೇಟ್ ದ್ರಾವಣದಲ್ಲಿ ಇಟ್ಟಾಗ ಬಣ್ಣ ಏಕೆ ಬದಲಾಗುತ್ತದೆ?" },
        { label: "ರೆಡಾಕ್ಸ್ ಕ್ರಿಯೆ ಮತ್ತು ತುಕ್ಕು 🛡️", query: "ರೆಡಾಕ್ಸ್ ಕ್ರಿಯೆ ಎಂದರೇನು ಮತ್ತು ಕಬ್ಬಿಣಕ್ಕೆ ತುಕ್ಕು ಹೇಗೆ ಹಿಡಿಯುತ್ತದೆ?" },
      ];
    } else {
      return [
        { label: "Combination vs Decomposition Reactions 🧪", query: "What is the difference between combination and decomposition reactions with balanced equations?" },
        { label: "Why Iron Nails Turn Copper Sulphate Green 🔵", query: "Why does the blue colour of copper sulphate solution change to light green when an iron nail is dipped in it?" },
        { label: "What is a Redox Reaction? ⚖️", query: "What is a redox reaction? Explain oxidation and reduction with CuO + H2." },
        { label: "How to Prevent Rusting & Rancidity 🛡️", query: "What causes rusting of iron and food rancidity, and how are they prevented?" },
        { label: "Electrolysis of Water Ratio 💧", query: "Why is the volume of hydrogen gas collected during electrolysis of water double that of oxygen?" },
      ];
    }
  }

  // Physics Prompts
  if (chap.includes("physics") || chap.includes("light")) {
    if (languageKey === "Hindi") {
      return [
        { label: "परावर्तन और दर्पण सूत्र 🪞", query: "दर्पण सूत्र क्या है और u, v, f में क्या संबंध है?" },
        { label: "स्नेल का नियम और अपवर्तनांक 🔍", query: "प्रकाश का अपवर्तन और स्नेल का नियम क्या है?" },
        { label: "गाड़ियों में उत्तल दर्पण क्यों लगाते हैं? 🚗", query: "वाहनों में पीछे का दृश्य देखने के लिए उत्तल दर्पण का उपयोग क्यों किया जाता है?" },
        { label: "लेंस की क्षमता और डायोप्टर 👓", query: "लेंस की क्षमता (Power of lens) क्या है और डायोप्टर की परिभाषा क्या है?" },
      ];
    } else if (languageKey === "Kannada") {
      return [
        { label: "ಬೆಳಕಿನ ಪ್ರತಿಫಲನ ಮತ್ತು ದರ್ಪಣ ಸೂತ್ರ 🪞", query: "ದರ್ಪಣ ಸೂತ್ರ 1/v + 1/u = 1/f ಎಂದರೇನು?" },
        { label: "ಸ್ನೆಲ್‌ನ ನಿಯಮ ಮತ್ತು ವಕ್ರೀಭವನಾಂಕ 🔍", query: "ಬೆಳಕಿನ ವಕ್ರೀಭವನ ಮತ್ತು ಸ್ನೆಲ್‌ನ ನಿಯಮವನ್ನು ವಿವರಿಸಿ." },
        { label: "ವಾಹನಗಳಲ್ಲಿ ಪೀನ ದರ್ಪಣದ ಬಳಕೆ 🚗", query: "ವಾಹನಗಳ ಹಿನ್ನೋಟ ದರ್ಪಣವಾಗಿ ಪೀನ ದರ್ಪಣವನ್ನು ಏಕೆ ಬಳಸಲಾಗುತ್ತದೆ?" },
        { label: "ಮಸೂರದ ಸಾಮರ್ಥ್ಯ ಮತ್ತು ಡಯಾಪ್ಟರ್ 👓", query: "ಮಸೂರದ ಸಾಮರ್ಥ್ಯ P = 1/f ಮತ್ತು ಡಯಾಪ್ಟರ್ ಎಂದರೇನು?" },
      ];
    } else {
      return [
        { label: "Mirror Formula & Sign Convention 🪞", query: "What is the mirror formula 1/v + 1/u = 1/f and how are signs determined?" },
        { label: "Snell's Law of Refraction 🔍", query: "State Snell's law of refraction and define refractive index n = c/v." },
        { label: "Why Convex Mirrors for Automobiles? 🚗", query: "Why are convex mirrors preferred as rear-view mirrors in vehicles?" },
        { label: "Power of a Lens & Dioptre Unit 👓", query: "What is the power of a lens P = 1/f (in meters) and define 1 Dioptre?" },
        { label: "Convex vs Concave Lens Action ☀️", query: "What is the difference between a converging convex lens and a diverging concave lens?" },
      ];
    }
  }

  // Default Biology Prompts
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

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  topic: string;
  explanation: string;
  page: number;
  subject?: "biology" | "chemistry" | "physics";
}

export const MASTER_QUIZ_BANK: QuizQuestion[] = [
  // --- BIOLOGY QUESTIONS ---
  {
    question: "What is the primary site of complete digestion of carbohydrates, proteins, and fats in the human body?",
    options: ["Stomach", "Small Intestine", "Large Intestine", "Mouth"],
    correct_index: 1,
    topic: "Digestion & Small Intestine",
    explanation: "The small intestine is the site of complete digestion, assisted by bile juice and pancreatic enzymes.",
    page: 3,
    subject: "biology",
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
    page: 1,
    subject: "biology",
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
    page: 3,
    subject: "biology",
  },
  {
    question: "During vigorous muscular exercise in humans, sudden painful muscle cramps occur due to the accumulation of:",
    options: ["Ethanol", "Lactic Acid", "Carbon Dioxide", "Hydrochloric Acid"],
    correct_index: 1,
    topic: "Cellular Respiration & Muscle Cramps",
    explanation: "Anaerobic respiration in human muscle cells produces lactic acid due to oxygen lack, causing cramps.",
    page: 4,
    subject: "biology",
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
    page: 2,
    subject: "biology",
  },
  {
    question: "Which enzyme present in human saliva initiates the chemical digestion of dietary starch into maltose?",
    options: ["Pepsin", "Salivary Amylase", "Trypsin", "Lipase"],
    correct_index: 1,
    topic: "Mouth Digestion & Enzymes",
    explanation: "Salivary amylase breaks down complex starch molecules into simple disaccharide sugars (maltose).",
    page: 3,
    subject: "biology",
  },
  {
    question: "What are the tiny balloon-like structures in human lungs that provide an ultra-thin surface for rapid gas exchange called?",
    options: ["Bronchioles", "Alveoli", "Villi", "Trachea"],
    correct_index: 1,
    topic: "Respiratory System & Alveoli",
    explanation: "Alveoli provide an extensive, ultra-thin moist surface lined with blood capillaries for rapid O2 and CO2 diffusion.",
    page: 4,
    subject: "biology",
  },

  // --- CHEMISTRY QUESTIONS ---
  {
    question: "What type of chemical reaction takes place when Quicklime (CaO) vigorously reacts with water to form Slaked Lime (Ca(OH)2)?",
    options: ["Combination Reaction", "Decomposition Reaction", "Displacement Reaction", "Double Displacement Reaction"],
    correct_index: 0,
    topic: "Combination Reaction & Quicklime",
    explanation: "CaO + H2O ---> Ca(OH)2 is a combination reaction where two reactants combine into a single product, releasing heat [Page 2].",
    page: 2,
    subject: "chemistry",
  },
  {
    question: "During the electrolytic decomposition of water, what is the volume ratio of hydrogen gas to oxygen gas collected at the electrodes?",
    options: ["1 : 1", "2 : 1", "1 : 2", "3 : 1"],
    correct_index: 1,
    topic: "Electrolysis of Water",
    explanation: "Water (H2O) contains 2 parts hydrogen to 1 part oxygen by volume, producing a 2:1 volume ratio during electrolysis [Page 2].",
    page: 2,
    subject: "chemistry",
  },
  {
    question: "When an iron nail is immersed in a blue Copper Sulphate (CuSO4) solution, why does the solution turn light green?",
    options: [
      "Copper oxidizes iron into rust",
      "Iron displaces copper from copper sulphate forming light green Ferrous Sulphate (FeSO4)",
      "Iron decomposes into iron oxide",
      "Copper sulphate evaporates completely"
    ],
    correct_index: 1,
    topic: "Displacement Reaction & Iron Nail",
    explanation: "Iron is more reactive than copper, displacing it: Fe + CuSO4 ---> FeSO4 (light green) + Cu [Page 3].",
    page: 3,
    subject: "chemistry",
  },
  {
    question: "In the chemical reaction: CuO + H2 ---> Cu + H2O, which substance undergoes reduction?",
    options: ["Copper Oxide (CuO)", "Hydrogen (H2)", "Water (H2O)", "Copper (Cu)"],
    correct_index: 0,
    topic: "Redox Reactions (Oxidation & Reduction)",
    explanation: "CuO loses oxygen to become elemental Cu, which is the definition of reduction [Page 4].",
    page: 4,
    subject: "chemistry",
  },
  {
    question: "Why are bags of potato chips and oily snacks flushed with unreactive Nitrogen gas during manufacturing?",
    options: [
      "To enhance sweet taste",
      "To prevent oxidation and rancidity of fats and oils",
      "To speed up chemical fermentation",
      "To kill photosynthetic organisms"
    ],
    correct_index: 1,
    topic: "Corrosion & Rancidity Prevention",
    explanation: "Flushing snack packages with inert nitrogen prevents fats and oils from oxidizing and turning rancid [Page 5].",
    page: 5,
    subject: "chemistry",
  },

  // --- PHYSICS QUESTIONS ---
  {
    question: "What is the relationship between the focal length (f) and the radius of curvature (R) of a spherical mirror?",
    options: ["f = 2R", "f = R / 2", "f = R^2", "f = 1 / R"],
    correct_index: 1,
    topic: "Spherical Mirrors & Focal Length",
    explanation: "For spherical mirrors of small aperture, the focus lies midway between the pole and center of curvature: f = R / 2 [Page 1].",
    page: 1,
    subject: "physics",
  },
  {
    question: "Which type of mirror is universally used as rear-view mirrors in vehicles to provide drivers a wider field of view?",
    options: ["Plane Mirror", "Concave Mirror", "Convex Mirror", "Cylindrical Mirror"],
    correct_index: 2,
    topic: "Convex Mirrors in Automobiles",
    explanation: "Convex mirrors always form erect, diminished virtual images, providing a much wider field of view for motorists [Page 3].",
    page: 3,
    subject: "physics",
  },
  {
    question: "According to Snell's Law of Refraction, what ratio remains constant for light passing between two transparent media?",
    options: [
      "sin(i) / sin(r) = constant",
      "cos(i) / cos(r) = constant",
      "tan(i) * tan(r) = constant",
      "i + r = 90 degrees"
    ],
    correct_index: 0,
    topic: "Snell's Law of Refraction",
    explanation: "Snell's law states that sin(i) / sin(r) = constant = refractive index n21 for a given pair of optical media [Page 4].",
    page: 4,
    subject: "physics",
  },
  {
    question: "What is the SI unit of Power of a lens (P = 1 / f in meters)?",
    options: ["Watt (W)", "Joule (J)", "Dioptre (D)", "Lumen (lm)"],
    correct_index: 2,
    topic: "Power of a Lens & Dioptre",
    explanation: "The SI unit of lens power is the Dioptre (D). A lens of focal length 1 meter has a power of 1 Dioptre (1 D = 1 m^-1) [Page 6].",
    page: 6,
    subject: "physics",
  },
  {
    question: "A doctor prescribes a corrective optical lens with a power of +2.0 Dioptres. What type of lens is it and what is its focal length?",
    options: [
      "Convex lens with focal length +0.5 meters",
      "Concave lens with focal length -0.5 meters",
      "Convex lens with focal length +2.0 meters",
      "Concave lens with focal length -2.0 meters"
    ],
    correct_index: 0,
    topic: "Corrective Lenses & Power Calculation",
    explanation: "Positive power indicates a converging convex lens. Focal length f = 1 / P = 1 / 2.0 = +0.5 meters [Page 6].",
    page: 6,
    subject: "physics",
  },
];

export function getRandomizedCuratedQuiz(chapterTitle?: string): QuizQuestion[] {
  let filtered = [...MASTER_QUIZ_BANK];

  if (chapterTitle) {
    const chap = chapterTitle.toLowerCase();
    if (chap.includes("chem")) {
      const match = MASTER_QUIZ_BANK.filter((q) => q.subject === "chemistry");
      if (match.length >= 3) filtered = match;
    } else if (chap.includes("phys") || chap.includes("light")) {
      const match = MASTER_QUIZ_BANK.filter((q) => q.subject === "physics");
      if (match.length >= 3) filtered = match;
    } else if (chap.includes("bio") || chap.includes("life")) {
      const match = MASTER_QUIZ_BANK.filter((q) => q.subject === "biology");
      if (match.length >= 3) filtered = match;
    }
  }

  // Fisher-Yates array shuffler
  for (let i = filtered.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
  }
  const chosen = filtered.slice(0, 5);

  return chosen.map((q) => {
    const correctText = q.options[q.correct_index];
    const opts = [...q.options];
    for (let i = opts.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [opts[i], opts[j]] = [opts[j], opts[i]];
    }
    return {
      ...q,
      options: opts,
      correct_index: opts.indexOf(correctText),
    };
  });
}
