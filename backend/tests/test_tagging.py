from src.tagging import GrantTagger


def test_tagger_basic():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Sustainable Agriculture Research Grant",
        (
            "Funding for projects that promote organic farming practices "
            "and soil conservation."
        ),
    )

    assert "agriculture" in tags
    assert "research" in tags
    assert "soil" in tags


def test_tagger_education():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "STEM Education Initiative",
        (
            "Support for programs that encourage high school students to pursue "
            "careers in science, technology, engineering, and mathematics."
        ),
    )

    assert "education" in tags
    assert "school" in tags
    assert "youth" in tags


def test_tagger_nutrient_management():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Nutrient Management Farmer Education Grants",
        (
            "The Nutrient Management Farmer Education Grant Program supports "
            "nutrient management planning in Wisconsin by funding entities to educate farmers."
        ),
    )

    assert "nutrient-management" in tags
    assert "education" in tags
    assert "farmer" in tags


def test_tagger_organic_transition():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Minnesota Transition to Organic Cost-Share Program",
        (
            "This program supports Minnesota farmers transitioning to organic farming "
            "by reimbursing costs associated with working with an organic certifying "
            "agency during the transition period."
        ),
    )

    assert "organic-transition" in tags
    assert "farmer" in tags
    assert "cost-share" in tags


def test_tagger_drought_relief():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Farmers Drought Relief Fund",
        (
            "The Farmers Drought Relief Fund aims to assist Maine farmers in overcoming "
            "the adverse effects of drought by providing grants for developing agricultural "
            "water management plans and installing agricultural water sources."
        ),
    )

    assert "drought" in tags
    assert "farmer" in tags
    assert "water" in tags


def test_tagger_equine_welfare():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Equine Welfare Assistance",
        (
            "The Equine Welfare Assistance Grant aims to enhance the well-being of Colorado's "
            "domestic equines by funding projects and programs that support safety net initiatives, "
            "adoption programs, education, and awareness related to equine welfare."
        ),
    )

    assert "equine" in tags
    assert "education" in tags
    assert "safety-net" in tags


def test_tagger_no_hallucination():
    tagger = GrantTagger()

    tags = tagger.tag_grant(
        "Random Grant Program",
        (
            "This is a grant for something completely unrelated to agriculture "
            "or any predefined tags."
        ),
    )

    for tag in tags:
        assert tag in tagger.tags


def test_tagger_case_insensitive():
    tagger = GrantTagger()

    tags = tagger.tag_grant("AGRICULTURE GRANT", "FARMING AND EDUCATION")

    assert "agriculture" in tags
    assert "education" in tags


def test_normalize_text():
    tagger = GrantTagger()

    text = "Hello, World! This is a TEST."
    normalized = tagger.normalize_text(text)

    assert normalized == "hello world this is a test"


def test_simple_stem():
    tagger = GrantTagger()

    assert tagger.simple_stem("farmers") == "farmer"
    assert tagger.simple_stem("farms") == "farm"
    assert tagger.simple_stem("berries") == "berry"
