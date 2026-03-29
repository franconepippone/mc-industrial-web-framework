import os
from dotenv import load_dotenv
import yaml
import github

load_dotenv()

REPO_NAME = "franconepippone/mc-industrial-web-framework"
BRANCH = "master"

token = os.getenv("GITHUB_TOKEN")

if not token:
    raise RuntimeError("GITHUB_TOKEN environment variable not set")

auth = github.Auth.Token(token)
g = github.Github(auth=auth)

repo = g.get_repo(REPO_NAME)

print(repo)

# -----------------------------
# Find specs.yaml files
# -----------------------------

branch = repo.get_branch(BRANCH)
tree = repo.get_git_tree(branch.commit.sha, recursive=True)

spec_paths = []

for element in tree.tree:
    path = element.path
    if path.startswith("designs/") and path.endswith("specs.yaml"):
        spec_paths.append(path)

# -----------------------------
# Download YAML files
# -----------------------------

design_specs = []

for path in spec_paths:
    content = repo.get_contents(path, ref=BRANCH)

    yaml_data = yaml.safe_load(content.decoded_content)

    design_specs.append({
        "path": path,
        "spec": yaml_data
    })

# -----------------------------
# Result
# -----------------------------

print(f"Loaded {len(design_specs)} design specs")

for spec in design_specs:
    print(spec["path"])