from dataclasses import dataclass, field


@dataclass
class Grant:
    grant_name: str
    grant_description: str
    tags: list[str] = field(default_factory=list)
    website_urls: list[str] | None = field(default_factory=list)
    document_urls: list[str] | None = field(default_factory=list)

    def to_dict(self):
        return {
            "grant_name": self.grant_name,
            "grant_description": self.grant_description,
            "tags": self.tags,
            "website_urls": self.website_urls,
            "document_urls": self.document_urls,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            grant_name=data.get("grant_name", ""),
            grant_description=data.get("grant_description", ""),
            tags=data.get("tags", []),
            website_urls=data.get("website_urls", []),
            document_urls=data.get("document_urls", []),
        )
