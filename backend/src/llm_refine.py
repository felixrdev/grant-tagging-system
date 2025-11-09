import os

from src.tags import PREDEFINED_TAGS


def llm_refine(
    grant_name: str, grant_description: str, initial_tags: list[str]
) -> list[str]:
    """
    Optional LLM-based tag refinement.

    Takes the initial keyword-matched tags and uses an LLM to:
    1. Re-rank tags by relevance
    2. Suggest additional tags from PREDEFINED_TAGS only
    3. Remove any clearly mismatched tags

    This function is ONLY called when USE_LLM=true.

    Args:
        grant_name: The grant name
        grant_description: The grant description
        initial_tags: Tags from keyword matching

    Returns:
        Refined list of tags (only from PREDEFINED_TAGS)
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return initial_tags

    predefined_set = set(PREDEFINED_TAGS)
    initial_tags_str = ", ".join(initial_tags)
    available_tags_str = ", ".join(sorted(PREDEFINED_TAGS))

    prompt = f"""You are a grant categorization assistant. Given a grant and some \
initial tags from keyword matching, your job is to:
1. Re-rank the initial tags by relevance
2. Add any missing relevant tags from the available tags list
3. Remove any clearly incorrect tags

IMPORTANT: You may ONLY use tags from the "Available tags" list. Do not invent \
new tags.

Grant Name: {grant_name}
Grant Description: {grant_description}

Initial tags (from keyword matching): {initial_tags_str}

Available tags: {available_tags_str}

Return ONLY a comma-separated list of tags, ordered by relevance. No explanations.
Example: agriculture, education, youth, sustainability"""

    try:
        import openai

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise grant categorization assistant. "
                        "Only return comma-separated tags from the provided list."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=200,
        )

        refined_tags_str = response.choices[0].message.content.strip()
        refined_tags = [tag.strip().lower() for tag in refined_tags_str.split(",")]

        valid_tags = [tag for tag in refined_tags if tag in predefined_set]

        return valid_tags if valid_tags else initial_tags

    except ImportError:
        return initial_tags
    except Exception:
        return initial_tags
