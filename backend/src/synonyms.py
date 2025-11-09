SYNONYM_MAP = {
    "learning": "education",
    "teach": "education",
    "teaching": "education",
    "school": "education",
    "classroom": "education",
    "curricula": "education",
    "curriculum": "education",
    "training": "education",
    "workshop": "education",
    "soil health": "soil",
    "soil-health": "soil",
    "ground": "soil",
    "earth": "soil",
    "local food": "local-food",
    "local-food": "local-food",
    "locally sourced": "local-food",
    "regional food": "local-food",
    "irrigation": "water",
    "watering": "water",
    "water system": "water",
    "water-system": "water",
    "farm": "agriculture",
    "farming": "agriculture",
    "agricultural": "agriculture",
    "crop": "agriculture",
    "crops": "agriculture",
    "grower": "agriculture",
    "producer": "agriculture",
    "organic": "organic-transition",
    "sustainable": "sustainability",
    "sustain": "sustainability",
    "environment": "sustainability",
    "environmental": "sustainability",
    "climate": "climate-change",
    "climate-change": "climate-change",
    "global warming": "climate-change",
    "student": "youth",
    "students": "youth",
    "children": "youth",
    "kids": "youth",
    "young people": "youth",
    "equine": "equine",
    "horse": "equine",
    "horses": "equine",
    "drought": "drought",
    "dry": "drought",
    "water shortage": "drought",
    "nutrient": "nutrient-management",
    "nutrients": "nutrient-management",
    "nutrient-management": "nutrient-management",
    "fertilizer": "nutrient-management",
    "business": "business-development",
    "entrepreneur": "business-development",
    "startup": "business-development",
    "market": "marketing",
    "markets": "marketing",
    "marketing": "marketing",
    "promotion": "marketing",
    "community": "community",
    "local": "community",
    "neighborhood": "community",
    "research": "research",
    "study": "research",
    "investigation": "research",
    "equipment": "equipment",
    "machinery": "equipment",
    "tool": "equipment",
    "tools": "equipment",
    "implement": "equipment",
    "cost-share": "cost-share",
    "cost share": "cost-share",
    "financial assistance": "grant",
    "funding": "grant",
}


def resolve_synonym(term: str) -> str:
    normalized = term.lower().strip()
    return SYNONYM_MAP.get(normalized, normalized)


def resolve_query(query: str) -> set[str]:
    tokens = query.lower().replace("-", " ").split()
    resolved_tags = set()

    for token in tokens:
        canonical = resolve_synonym(token)
        resolved_tags.add(canonical)

    multi_word = query.lower().strip()
    canonical = resolve_synonym(multi_word)
    if canonical != multi_word:
        resolved_tags.add(canonical)

    return resolved_tags
