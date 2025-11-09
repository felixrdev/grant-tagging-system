#!/usr/bin/env python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import Grant
from src.store import GrantStore
from src.tagging import GrantTagger


def seed_grants():
    seed_file = Path(__file__).parent.parent.parent / "data" / "grants_seed.json"

    if not seed_file.exists():
        print(f"Seed file not found: {seed_file}")
        return

    print(f"Loading seed data from {seed_file}")
    with open(seed_file) as f:
        grants_data = json.load(f)

    print(f"Loaded {len(grants_data)} grants from seed file")

    tagger = GrantTagger()
    store = GrantStore()

    print("Tagging grants...")
    tagged_grants = []
    for data in grants_data:
        tags = tagger.tag_grant(data["grant_name"], data["grant_description"])
        grant = Grant(
            grant_name=data["grant_name"],
            grant_description=data["grant_description"],
            tags=tags,
            website_urls=data.get("website_urls", []),
            document_urls=data.get("document_urls", []),
        )
        tagged_grants.append(grant)
        print(f"   • {grant.grant_name[:50]}... → {len(tags)} tags")

    print(f"\nSaving {len(tagged_grants)} grants to storage...")
    store.clear_grants()
    store.write_grants(tagged_grants)

    print("Seeding complete!")
    print("\nSummary:")
    print(f"   • Total grants: {len(tagged_grants)}")
    all_tags = set()
    for g in tagged_grants:
        all_tags.update(g.tags)
    print(f"   • Unique tags used: {len(all_tags)}")
    print(
        f"   • Average tags per grant: {sum(len(g.tags) for g in tagged_grants) / len(tagged_grants):.1f}"
    )


if __name__ == "__main__":
    seed_grants()
