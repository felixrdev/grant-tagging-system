from collections import defaultdict

from src.models import Grant


class SearchIndex:
    def __init__(self):
        self.tag_to_grant_ids: dict[str, set[int]] = defaultdict(set)
        self.grant_id_to_grant: dict[int, Grant] = {}
        self._next_id = 0

    def clear(self):
        self.tag_to_grant_ids.clear()
        self.grant_id_to_grant.clear()
        self._next_id = 0

    def add_grants(self, grants: list[Grant]):
        for grant in grants:
            grant_id = self._next_id
            self._next_id += 1

            self.grant_id_to_grant[grant_id] = grant

            for tag in grant.tags:
                tag_normalized = tag.lower().strip()
                self.tag_to_grant_ids[tag_normalized].add(grant_id)

    def rebuild(self, grants: list[Grant]):
        self.clear()
        self.add_grants(grants)

    def search_by_tags(self, tags: list[str], mode: str = "all") -> list[Grant]:
        if not tags:
            return []

        normalized_tags = [tag.lower().strip() for tag in tags]

        grant_id_sets = [
            self.tag_to_grant_ids.get(tag, set()) for tag in normalized_tags
        ]

        if mode == "all":
            if not grant_id_sets:
                return []
            matching_ids = set.intersection(*grant_id_sets)
        else:
            matching_ids = set.union(*grant_id_sets) if grant_id_sets else set()

        return [self.grant_id_to_grant[gid] for gid in sorted(matching_ids)]


_global_index = SearchIndex()


def get_search_index() -> SearchIndex:
    return _global_index
