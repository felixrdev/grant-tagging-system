import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from src.models import Grant
from src.search_index import get_search_index
from src.store import GrantStore
from src.synonyms import resolve_query
from src.tagging import GrantTagger
from src.tags import PREDEFINED_TAGS

load_dotenv()

app = Flask(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins == "*":
    CORS(app)
else:
    origins_list = [origin.strip() for origin in allowed_origins.split(",")]
    CORS(app, resources={r"/api/*": {"origins": origins_list}})

store = GrantStore()
tagger = GrantTagger()
search_index = get_search_index()


@app.before_request
def initialize_search_index():
    if not search_index.grant_id_to_grant:
        existing_grants = store.read_grants()
        if existing_grants:
            search_index.rebuild(existing_grants)


@app.route("/")
def index():
    return jsonify(
        {"message": "Grant Tagging API", "version": "1.0.0", "status": "running"}
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/health")
def api_health():
    return jsonify({"status": "healthy"})


@app.route("/api/grants", methods=["GET"])
def get_grants():
    grants = store.read_grants()
    return jsonify([g.to_dict() for g in grants])


@app.route("/api/grants/batch", methods=["POST"])
def batch_tag_grants():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected array of grants"}), 400

    tagged_grants = []
    for item in data:
        grant_name = item.get("grant_name", "")
        grant_description = item.get("grant_description", "")

        if not grant_name or not grant_description:
            return (
                jsonify({"error": "grant_name and grant_description are required"}),
                400,
            )

        tags = tagger.tag_grant(grant_name, grant_description)

        grant = Grant(
            grant_name=grant_name,
            grant_description=grant_description,
            tags=tags,
            website_urls=item.get("website_urls", []),
            document_urls=item.get("document_urls", []),
        )
        tagged_grants.append(grant)

    store.append_grants(tagged_grants)
    search_index.add_grants(tagged_grants)

    return jsonify([g.to_dict() for g in tagged_grants])


@app.route("/api/tags", methods=["GET"])
def get_tags():
    return jsonify(PREDEFINED_TAGS)


@app.route("/api/search", methods=["GET"])
def search_grants():
    tags_param = request.args.get("tags", "")

    if not tags_param:
        return jsonify([])

    requested_tags = [t.strip().lower() for t in tags_param.split(",")]

    all_grants = store.read_grants()

    matching_grants = []
    for grant in all_grants:
        grant_tags_lower = [t.lower() for t in grant.tags]
        if all(tag in grant_tags_lower for tag in requested_tags):
            matching_grants.append(grant.to_dict())

    return jsonify(matching_grants)


@app.route("/api/search/advanced", methods=["GET"])
def advanced_search():
    query = request.args.get("q", "").strip()
    tags_param = request.args.get("tags", "").strip()
    mode = request.args.get("mode", "all").lower()

    if mode not in ["all", "any"]:
        return jsonify({"error": "mode must be 'all' or 'any'"}), 400

    resolved_tags = set()

    if query:
        resolved_tags.update(resolve_query(query))

    if tags_param:
        explicit_tags = [t.strip().lower() for t in tags_param.split(",") if t.strip()]
        resolved_tags.update(explicit_tags)

    if not resolved_tags:
        return jsonify({"resolved_tags": [], "grants": []})

    matching_grants = search_index.search_by_tags(list(resolved_tags), mode=mode)

    return jsonify(
        {
            "resolved_tags": sorted(list(resolved_tags)),
            "grants": [g.to_dict() for g in matching_grants],
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        debug=os.getenv("FLASK_ENV") == "development",
    )
