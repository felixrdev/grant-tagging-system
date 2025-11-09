import os
import re

from src.tags import PREDEFINED_TAGS

KEYWORD_MAP = {
    "agriculture": [
        "farm",
        "farming",
        "agricultural",
        "crop",
        "crops",
        "producer",
        "grower",
    ],
    "aquaculture": ["fish", "seafood", "marine", "aquatic"],
    "capacity-building": ["capacity", "development", "strengthen", "enhance"],
    "capital": ["capital", "funding", "investment", "finance"],
    "climate": ["climate", "weather", "greenhouse", "carbon"],
    "community-benefit": ["community", "public", "benefit"],
    "conservation": ["conserve", "conservation", "preserve", "protection"],
    "cost-share": ["cost-share", "cost share", "reimbursement", "matching"],
    "dairy": ["dairy", "milk", "cattle", "cow"],
    "distribution": ["distribute", "distribution", "delivery", "transport"],
    "drought": ["drought", "dry", "water shortage"],
    "education": [
        "education",
        "educational",
        "learning",
        "teach",
        "school",
        "student",
        "curricula",
        "training program",
    ],
    "equipment": ["equipment", "machinery", "tool", "implement"],
    "equine": ["equine", "horse", "horses"],
    "equine-owners": ["equine owner", "horse owner"],
    "food-safety": ["food safety", "safe", "sanitation", "inspection"],
    "farmer": ["farmer", "grower", "producer", "rancher"],
    "farm-to-school": ["farm to school", "school meal", "school food"],
    "grant": ["grant", "funding", "financial assistance"],
    "infrastructure": [
        "infrastructure",
        "facility",
        "facilities",
        "building",
        "construction",
    ],
    "irrigation": ["irrigation", "irrigate", "watering", "water system"],
    "local-food": ["local food", "local product", "locally sourced", "regional food"],
    "local-government": ["local government", "municipality", "county", "city"],
    "logistics": ["logistics", "supply chain", "distribution"],
    "marketing": ["marketing", "market", "promotion", "advertising", "brand"],
    "mixed-operations": ["mixed operation", "diversified"],
    "nonprofit": ["nonprofit", "non-profit", "NGO", "charity"],
    "nutrient-management": ["nutrient", "fertilizer", "nutrient management"],
    "operational": ["operational", "operations", "operating"],
    "organic-certification": ["organic certification", "certified organic"],
    "organic-transition": ["organic transition", "transitioning to organic"],
    "outreach": ["outreach", "awareness", "engagement", "communication"],
    "planning": ["planning", "plan", "strategy"],
    "pilot": ["pilot", "demonstration", "trial"],
    "producer-group": ["producer group", "cooperative", "association"],
    "procurement": ["procurement", "purchase", "purchasing", "buying"],
    "processing": ["processing", "process", "value-added", "manufacturing"],
    "research": ["research", "study", "investigation", "science"],
    "resilience": ["resilience", "resilient", "adaptation", "recovery"],
    "reimbursement": ["reimbursement", "reimburse", "repayment"],
    "rolling": ["rolling", "ongoing", "continuous"],
    "rural": ["rural", "countryside", "agricultural area"],
    "safety-net": ["safety net", "assistance", "support", "welfare"],
    "school": ["school", "educational institution", "K-12", "high school"],
    "seafood": ["seafood", "fish", "shellfish", "aquatic"],
    "seafood-harvester": ["seafood harvester", "fisherman", "fisher"],
    "soil": ["soil", "earth", "ground", "land"],
    "supply-chain": ["supply chain", "logistics", "distribution"],
    "technical-assistance": [
        "technical assistance",
        "consulting",
        "advisory",
        "support",
    ],
    "training": ["training", "education", "workshop", "instruction", "learning"],
    "value-added": ["value-added", "value added", "processing", "manufactured"],
    "water": ["water", "aquatic", "hydro"],
    "water-storage": ["water storage", "reservoir", "tank", "cistern"],
    "working-capital": ["working capital", "operational funds", "cash flow"],
    "row-crops": ["row crop", "grain", "corn", "soybean", "wheat"],
    "vegetables": ["vegetable", "produce", "veggie"],
    "fruit": ["fruit", "orchard", "berry", "berries"],
    "livestock": ["livestock", "cattle", "animal", "herd"],
    "competitive": ["competitive", "competition", "merit-based"],
    "match-required": ["match required", "matching", "cost-share"],
    "public-entity-eligible": ["public entity", "government", "municipality"],
    "individual-eligible": ["individual", "person", "farmer"],
    "cooperative": ["cooperative", "co-op", "association"],
    "for-profit": ["for-profit", "business", "commercial"],
    "university": ["university", "college", "academic"],
    "extension": ["extension", "outreach"],
    "tribal": ["tribal", "tribe", "indigenous", "native"],
    "veteran": ["veteran", "military", "armed forces"],
    "beginning-farmer": ["beginning farmer", "new farmer", "novice"],
    "underserved": ["underserved", "disadvantaged", "minority"],
    "youth": ["youth", "young", "children", "student", "students"],
    "food-access": ["food access", "food security", "hunger"],
    "nutrition": ["nutrition", "nutritional", "healthy eating"],
    "workforce": ["workforce", "employment", "labor", "worker"],
    "energy": ["energy", "power", "electricity"],
    "renewable-energy": ["renewable energy", "solar", "wind", "biomass"],
    "water-quality": ["water quality", "clean water", "pollution"],
    "soil-health": ["soil health", "soil quality", "soil conservation"],
    "wildlife-habitat": ["wildlife", "habitat", "ecosystem", "biodiversity"],
    "pasture": ["pasture", "grazing land", "grassland"],
    "grazing": ["grazing", "graze", "pasture"],
    "manure-management": ["manure", "waste management", "composting"],
    "disaster-relief": ["disaster", "emergency", "relief"],
    "flood": ["flood", "flooding", "inundation"],
}


class GrantTagger:
    def __init__(self, use_llm: bool = False):
        self.keyword_map = KEYWORD_MAP
        self.tags = PREDEFINED_TAGS
        self.use_llm = use_llm or os.getenv("USE_LLM", "false").lower() == "true"

    def normalize_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def simple_stem(self, word: str) -> str:
        if word.endswith("ies"):
            return word[:-3] + "y"
        if word.endswith("es"):
            return word[:-2]
        if word.endswith("s") and len(word) > 3:
            return word[:-1]
        return word

    def tag_grant(self, grant_name: str, grant_description: str) -> list[str]:
        combined_text = f"{grant_name} {grant_description}"
        normalized = self.normalize_text(combined_text)

        matched_tags: set[str] = set()

        for tag in self.tags:
            tag_normalized = tag.replace("-", " ")

            if tag_normalized in normalized or tag in normalized:
                matched_tags.add(tag)
                continue

            keywords = self.keyword_map.get(tag, [])
            for keyword in keywords:
                keyword_pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
                if re.search(keyword_pattern, normalized):
                    matched_tags.add(tag)
                    break

        words = normalized.split()
        stemmed_words = [self.simple_stem(w) for w in words]

        for tag in self.tags:
            if tag in matched_tags:
                continue

            tag_words = tag.replace("-", " ").split()
            for tag_word in tag_words:
                stemmed_tag = self.simple_stem(tag_word)
                if stemmed_tag in stemmed_words:
                    matched_tags.add(tag)
                    break

        initial_tags = sorted(list(matched_tags))

        if self.use_llm:
            try:
                from src.llm_refine import llm_refine

                refined_tags = llm_refine(grant_name, grant_description, initial_tags)
                return refined_tags
            except Exception:
                pass

        return initial_tags
