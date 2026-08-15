import os
import re
import yaml

repo_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(repo_dir, "README.md")

# Categories mapping mapping folder name patterns to category keys
USER_CATEGORIES = {
    "design_film_video": {
        "title": "🎨 Design, Film & Video",
        "patterns": ["yuv-pilot", "yuv-decks", "yuv-design-system", "yuv-viral-video", "video-edit", 
                     "video-to-landing-page", "parallax-landing-page", "director", "hyperframes", 
                     "hyperframes-cli", "hyperframes-registry", "canvas-design", "algorithmic-art", 
                     "image-enhancer", "theme-factory", "slack-gif-creator", "excalidraw", "draw-io", 
                     "marp-slide"]
    },
    "document_media_processing": {
        "title": "📄 Document & Media Processing",
        "patterns": ["document-skills/docx", "document-skills/pdf", "document-skills/pptx", 
                     "document-skills/xlsx", "web-to-markdown", "video-downloader", "resemble-detect", "document-skills"]
    },
    "notion_integration": {
        "title": "📓 Notion Integration",
        "patterns": ["notion-knowledge-capture", "notion-meeting-intelligence", 
                     "notion-research-documentation", "notion-spec-to-implementation"]
    },
    "development_testing": {
        "title": "🛠️ Development & Testing Tools",
        "patterns": ["artifacts-builder", "mcp-builder", "skill-creator", "webapp-testing", 
                     "template-skill", "skill-judge", "dependency-updater", "openapi-to-typescript", 
                     "changelog-generator", "commit-work", "reducing-entropy"]
    },
    "research_analysis": {
        "title": "🔍 Research & Analysis",
        "patterns": ["competitive-ads-extractor", "content-research-writer", "lead-research-assistant", 
                     "meeting-insights-analyzer", "daily-meeting-update", "session-handoff", "lesson-learned", 
                     "naming-analyzer", "domain-name-brainstormer", "gemini", "codex", "perplexity"]
    },
    "productivity_comms": {
        "title": "💬 Productivity & Communication",
        "patterns": ["internal-comms", "professional-communication", "difficult-workplace-conversations", 
                     "feedback-mastery", "raffle-winner-picker"]
    }
}

CONFIG_CATEGORIES = {
    "databases_data": {
        "title": "🗄️ Databases & Data Engineering",
        "patterns": ["alloydb-omni", "alloydb-postgres", "cloud-sql", "firestore-data", "spanner-data", 
                     "postgresql", "bigquery", "dbt", "spark-optimization", "airflow-dag-patterns", 
                     "database-migrations", "data-engineering"]
    },
    "security_compliance": {
        "title": "🔒 Security, Compliance & Hardening",
        "patterns": ["security", "secrets-management", "sast-configuration", "pci-compliance", "threat", 
                     "attack-tree", "stride-analysis", "anti-reversing", "binary-analysis", 
                     "malware-analyst", "solidity-security"]
    },
    "devops_infra": {
        "title": "☁️ DevOps & Infrastructure",
        "patterns": ["gcloud", "k8s", "kubernetes", "helm", "istio", "linkerd", "service-mesh", 
                     "turborepo", "nx-workspace", "bazel", "github_actions", "gitlab-ci", 
                     "deployment", "observability", "prometheus", "grafana", "datadog-cli", 
                     "incident", "postmortem", "slo-implementation"]
    },
    "agent_orchestration": {
        "title": "🤖 Agent Orchestration & Workflow",
        "patterns": ["agent-orchestration", "context", "conductor", "workflow-patterns", 
                     "git-pr-workflows", "tdd-", "team-collaboration"]
    },
    "software_languages": {
        "title": "💻 Software Engineering (Languages & APIs)",
        "patterns": ["python", "cpp", "c-pro", "java-pro", "javascript", "typescript", "golang", 
                     "rust", "elixir", "php-pro", "ruby-pro", "scala-pro", "haskell-pro", 
                     "angular-migration", "react", "nextjs", "django-pro", "fastapi", "api-design", 
                     "api-testing", "openapi-spec", "graphql", "mui", "tailwind-"]
    },
    "business_finance": {
        "title": "📈 Business & Financial Analysis",
        "patterns": ["startup", "quant-analyst", "risk", "billing", "sales-automator", 
                     "stripe-integration", "paypal-integration", "payment-integration", "cost-optimization"]
    }
}

def determine_category(relative_path, is_config=False):
    path_str = relative_path.replace("\\", "/")
    if path_str.startswith("config-skills/"):
        path_str = path_str[len("config-skills/"):]
        
    categories = CONFIG_CATEGORIES if is_config else USER_CATEGORIES
    
    for cat_key, cat_info in categories.items():
        for pattern in cat_info["patterns"]:
            if pattern in path_str:
                return cat_key
                
    return "other"

def extract_frontmatter(skill_md_path):
    if not os.path.exists(skill_md_path):
        return None
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Match YAML frontmatter
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            group_val = None
            try:
                parsed = yaml.safe_load(yaml_content)
                name = parsed.get("name")
                desc = parsed.get("description")
                group_val = parsed.get("group")
            except Exception:
                # Regex fallback if safe_load fails
                name_match = re.search(r"^name:\s*(.+)$", yaml_content, re.MULTILINE)
                desc_match = re.search(r"^description:\s*(.+)$", yaml_content, re.MULTILINE)
                group_match = re.search(r"^group:\s*(.+)$", yaml_content, re.MULTILINE)
                name = name_match.group(1).strip() if name_match else None
                desc = desc_match.group(1).strip() if desc_match else None
                group_val = group_match.group(1).strip() if group_match else None
            
            if not name:
                name = os.path.basename(os.path.dirname(skill_md_path))
            if not desc:
                desc = ""
            
            # Strip quotes from descriptions if present
            desc = desc.strip().strip('"').strip("'")
            desc = re.sub(r"\s+", " ", desc)
            return {"name": name, "description": desc, "group": group_val}
    except Exception as e:
        print(f"Error parsing {skill_md_path}: {e}")
    return None

def scan_skills_dir(directory, is_config=False):
    catalog = []
    if not os.path.exists(directory):
        return catalog
        
    for root, dirs, files in os.walk(directory):
        if ".git" in root.split(os.sep):
            continue
        if "SKILL.md" in files:
            skill_md_path = os.path.join(root, "SKILL.md")
            
            rel_path = os.path.relpath(root, repo_dir)
            if rel_path == "." or rel_path == "":
                continue
                
            if not is_config and (rel_path.startswith("config-skills") or "config-skills" in rel_path.split(os.sep)):
                continue
                
            info = extract_frontmatter(skill_md_path)
            if info:
                group_key = info.get("group")
                if not group_key:
                    group_key = determine_category(rel_path, is_config)
                
                info["group_key"] = group_key
                info["path"] = rel_path
                catalog.append(info)
    
    catalog.sort(key=lambda x: x["name"])
    return catalog

# Scan
user_skills = scan_skills_dir(repo_dir, is_config=False)
config_skills = scan_skills_dir(os.path.join(repo_dir, "config-skills"), is_config=True)

# Ensure categories directory exists
categories_dir = os.path.join(repo_dir, "categories")
os.makedirs(categories_dir, exist_ok=True)

# Clear existing category files to avoid orphaned configurations
if os.path.exists(categories_dir):
    for f_name in os.listdir(categories_dir):
        if f_name.endswith(".md"):
            try:
                os.remove(os.path.join(categories_dir, f_name))
            except Exception as e:
                print(f"Error removing old category file {f_name}: {e}")

# Group user skills
user_by_cat = {}
for skill in user_skills:
    group = skill["group_key"]
    if group not in user_by_cat:
        user_by_cat[group] = []
    user_by_cat[group].append(skill)

# Group config skills
config_by_cat = {}
for skill in config_skills:
    group = skill["group_key"]
    if group not in config_by_cat:
        config_by_cat[group] = []
    config_by_cat[group].append(skill)

# Helper function to write a category markdown document
def write_category_file(cat_key, title, skills, is_config):
    filename = f"{cat_key}.md"
    file_path = os.path.join(categories_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"This document catalogs the {'system configuration' if is_config else 'custom user'} skills belonging to the **{title}** category.\n\n")
        f.write("| Skill Name | Description | Path |\n")
        f.write("|---|---|---|\n")
        for skill in skills:
            # relative link goes up one level to categories' parent
            skill_link = f"[`{skill['name']}`](../{skill['path']})"
            f.write(f"| {skill_link} | {skill['description']} | `{skill['path']}` |\n")

# Write user category documents
for cat_key, cat_info in USER_CATEGORIES.items():
    skills_in_cat = user_by_cat.get(cat_key, [])
    if skills_in_cat:
        write_category_file(cat_key, cat_info["title"], skills_in_cat, is_config=False)

other_user = user_by_cat.get("other", [])
if other_user:
    write_category_file("other_user", "📦 Other User Skills", other_user, is_config=False)

# Write config category documents
for cat_key, cat_info in CONFIG_CATEGORIES.items():
    skills_in_cat = config_by_cat.get(cat_key, [])
    if skills_in_cat:
        write_category_file(cat_key, cat_info["title"], skills_in_cat, is_config=True)

other_config = config_by_cat.get("other", [])
if other_config:
    write_category_file("other_config", "⚙️ Other Config Skills", other_config, is_config=True)

# Build master README links
readme_addition = "\n\n## 📚 Skill Catalog\n"
readme_addition += f"\nThis repository manages a total of **{len(user_skills) + len(config_skills)}** skills.\n"

readme_addition += "\n### 👤 Custom User Skills\n"
readme_addition += "Click on a category to view the list of user-installed skills and their detailed descriptions:\n\n"
for cat_key, cat_info in USER_CATEGORIES.items():
    skills_in_cat = user_by_cat.get(cat_key, [])
    if skills_in_cat:
        readme_addition += f"- [{cat_info['title']}](categories/{cat_key}.md) ({len(skills_in_cat)} skills)\n"
if other_user:
    readme_addition += f"- [📦 Other User Skills](categories/other_user.md) ({len(other_user)} skills)\n"

readme_addition += "\n### ⚙️ System Config Skills\n"
readme_addition += "Click on a category to view the list of system-installed configuration skills and their detailed descriptions:\n\n"
for cat_key, cat_info in CONFIG_CATEGORIES.items():
    skills_in_cat = config_by_cat.get(cat_key, [])
    if skills_in_cat:
        readme_addition += f"- [{cat_info['title']}](categories/{cat_key}.md) ({len(skills_in_cat)} skills)\n"
if other_config:
    readme_addition += f"- [⚙️ Other Config Skills](categories/other_config.md) ({len(other_config)} skills)\n"

# Read original README up to the separator
original_content = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        original_content = f.read()

# Cut off any existing catalog section
cutoff_marker = "## 📚 Skill Catalog"
if cutoff_marker in original_content:
    original_content = original_content.split(cutoff_marker)[0].strip()

new_content = original_content.strip() + "\n" + readme_addition

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"README.md and category documents updated successfully with {len(user_skills)} user skills and {len(config_skills)} config skills.")
