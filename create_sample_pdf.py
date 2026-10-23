"""
Utility script to generate a sample textbook chapter PDF for VidyaVaani.
Topic: NCERT Class 10 Science - Chapter 6: Life Processes (Photosynthesis, Digestion, & Respiration)
Used for immediate testing, evaluation, and demoing without requiring manual PDF uploads.
"""

import pymupdf as fitz


def generate_sample_chapter_pdf(output_path="sample_chapter.pdf"):
    doc = fitz.open()

    pages_content = [
        # Page 1
        (
            "CHAPTER 6: LIFE PROCESSES",
            "1. What are Life Processes?\n\n"
            "All living organisms perform basic maintenance functions to keep themselves alive, "
            "even when they are resting or asleep. The processes which together perform this maintenance job "
            "are called life processes. Since these maintenance processes are needed to prevent damage and break-down, "
            "energy is needed for them. This energy comes from outside the body of the individual organism in the form of food.\n\n"
            "2. Autotrophic Nutrition and Photosynthesis\n\n"
            "Autotrophic organisms include green plants and some bacteria. They take in substances from the outside "
            "and convert them into stored forms of energy. Carbon and energy requirements of the autotrophic organism "
            "are fulfilled by photosynthesis.\n\n"
            "Definition: Photosynthesis is the process by which green plants synthesize organic food (carbohydrates) "
            "from carbon dioxide (CO2) and water (H2O) using solar energy trapped by chlorophyll, releasing oxygen.\n\n"
            "Chemical Equation of Photosynthesis:\n"
            "6CO2 + 12H2O + Sunlight + Chlorophyll ---> C6H12O6 (Glucose) + 6O2 + 6H2O\n\n"
            "Key Steps in Photosynthesis:\n"
            "1. Absorption of light energy by chlorophyll molecules present in chloroplasts.\n"
            "2. Conversion of light energy into chemical energy and splitting of water molecules into hydrogen and oxygen.\n"
            "3. Reduction of carbon dioxide into carbohydrates like glucose and starch."
        ),
        # Page 2
        (
            "PLANT GAS EXCHANGE AND STOMATA",
            "3. Structure and Function of Stomata\n\n"
            "Stomata are microscopic pores found on the surface of the leaves through which massive amounts "
            "of gaseous exchange take place in the plant for the purpose of photosynthesis.\n\n"
            "Each stomatal pore is flanked by a pair of kidney-shaped specialized cells called Guard Cells.\n"
            "- Opening and Closing: The opening and closing of the pore is a function of the guard cells.\n"
            "- When water flows into guard cells, they swell, become turgid, and cause the stomatal pore to open.\n"
            "- When guard cells lose water, they shrink and become flaccid, causing the stomatal pore to close.\n\n"
            "4. Desert Plant Adaptations\n\n"
            "Desert plants take up carbon dioxide at night when temperatures are cooler to minimize water loss "
            "through transpiration. They synthesize an intermediate organic acid, which is acted upon during the day "
            "by the energy absorbed by chlorophyll in sunlight.\n\n"
            "5. Essential Mineral Nutrients Absorbed from Soil\n\n"
            "Plants also require other raw materials for building their body. Water used in photosynthesis is taken up "
            "from the soil by roots in terrestrial plants. Other materials like Nitrogen, Phosphorus, Iron, and Magnesium "
            "are taken up from the soil. Nitrogen is an essential element used in the synthesis of proteins and other "
            "vital biochemical compounds."
        ),
        # Page 3
        (
            "HETEROTROPHIC NUTRITION & HUMAN DIGESTIVE SYSTEM",
            "6. Types of Heterotrophic Nutrition\n\n"
            "Heterotrophs depend on organic substances synthesized by autotrophs:\n"
            "- Saprophytic Nutrition: Organisms break down food outside the body and absorb it (e.g., bread moulds, yeast, mushrooms).\n"
            "- Parasitic Nutrition: Organisms derive nutrition without killing the host (e.g., Cuscuta/Amarbel, ticks, lice, tapeworms).\n"
            "- Holozoic Nutrition: Ingestion of complex organic matter followed by internal digestion (e.g., Amoeba, Humans).\n\n"
            "7. The Human Alimentary Canal and Digestion\n\n"
            "The human digestive tract is a long continuous muscular tube:\n\n"
            "a. Mouth: Teeth chew food, and saliva secreted by salivary glands contains the enzyme Salivary Amylase, "
            "which breaks down starch into simple sugars (maltose).\n\n"
            "b. Stomach: Muscular walls churn the food. Gastric glands in the stomach wall secrete:\n"
            "  * Hydrochloric Acid (HCl): Creates an acidic medium (pH 1.5 - 2.5) necessary for pepsin action and kills pathogens.\n"
            "  * Pepsin: An active protein-digesting enzyme that breaks complex proteins into peptones.\n"
            "  * Mucus: Protects the inner mucosal lining of the stomach from excoriation by HCl under normal conditions.\n\n"
            "c. Small Intestine: The site of complete digestion of carbohydrates, proteins, and fats:\n"
            "  * Bile Juice (from Liver): Alkaline juice that neutralizes stomach acid and emulsifies large fat globules into small micelles.\n"
            "  * Pancreatic Juice (from Pancreas): Contains Trypsin for digesting proteins and Lipase for breaking down emulsified fats.\n"
            "  * Intestinal Villi: Tiny finger-like projections rich in blood vessels that increase surface area for nutrient absorption."
        ),
        # Page 4
        (
            "CELLULAR RESPIRATION AND ENERGY GENERATION",
            "8. Breakdown of Glucose by Various Pathways\n\n"
            "Respiration is the cellular biochemical process where food molecules (glucose) are broken down to release ATP energy.\n"
            "The first step takes place in the cytoplasm: 6-carbon Glucose is split into two 3-carbon molecules called Pyruvate.\n\n"
            "Subsequent pathways of Pyruvate breakdown:\n\n"
            "Pathway A: Aerobic Respiration (In Presence of Oxygen)\n"
            "- Location: Mitochondria of cells.\n"
            "- Products: Carbon dioxide (CO2), Water (H2O), and a large amount of energy (~38 ATP molecules per glucose).\n\n"
            "Pathway B: Anaerobic Fermentation in Yeast (Absence of Oxygen)\n"
            "- Location: Cytoplasm of yeast cells.\n"
            "- Products: Ethanol (C2H5OH), Carbon dioxide (CO2), and 2 ATP molecules.\n\n"
            "Pathway C: Anaerobic Respiration in Human Muscle Cells (Lack of Oxygen)\n"
            "- Occurs during strenuous muscular exercise when oxygen demand outstrips supply.\n"
            "- Products: Lactic acid (a 3-carbon molecule) and 2 ATP.\n"
            "- The rapid accumulation of lactic acid in muscle fibers causes intense muscle cramps and fatigue.\n\n"
            "9. Human Respiratory Surface\n\n"
            "Within the lungs, the respiratory passage divides into smaller tubes terminating in balloon-like structures "
            "called Alveoli. Alveoli provide an extensive thin surface with a dense capillary network for efficient exchange of O2 and CO2."
        )
    ]

    for title, text in pages_content:
        page = doc.new_page(width=595, height=842)  # A4 size
        # Header banner
        page.draw_rect(fitz.Rect(40, 30, 555, 70), color=(0.15, 0.45, 0.8), fill=(0.92, 0.95, 0.99))
        page.insert_text(fitz.Point(50, 55), title, fontsize=14, color=(0.08, 0.25, 0.55), fontname="hebo")
        # Content
        page.insert_textbox(fitz.Rect(45, 85, 550, 780), text, fontsize=10.5, fontname="helv", lineheight=1.4)
        # Footer
        page_num_str = f"Page {doc.page_count} - NCERT Class X Science - VidyaVaani Reference Material"
        page.insert_text(fitz.Point(120, 815), page_num_str, fontsize=9, color=(0.5, 0.5, 0.5), fontname="helv")

    doc.save(output_path)
    doc.close()
    print(f"Sample chapter successfully created at: {output_path}")

if __name__ == "__main__":
    generate_sample_chapter_pdf()
