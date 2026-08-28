import os
import re
try:
    import yaml
except ImportError:
    yaml = None

repo_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(repo_dir, "README.md")

# Categories mapping mapping folder name patterns to category keys
USER_CATEGORIES = {
    "design_film_video": {
        "title": "🎨 Design, Film & Video",
        "patterns": [r"yuv-", r"video", r"film", r"director", r"hyperframes", r"canvas-design", r"algorithmic-art", r"image-enhancer", r"theme-factory", r"slack-gif-creator", r"excalidraw", r"draw-io", r"marp-slide", r"art", r"brand", r"decks", r"meme-factory"]
    },
    "document_media_processing": {
        "title": "📄 Document & Media Processing",
        "patterns": [r"document", r"docx", r"pdf", r"pptx", r"xlsx", r"web-to-markdown", r"video-downloader", r"resemble-detect", r"html", r"invoice"]
    },
    "notion_integration": {
        "title": "📓 Notion Integration",
        "patterns": [r"notion-"]
    },
    "ai_llm_engineering": {
        "title": "🤖 AI, RAG & LLM Engineering",
        "patterns": [r"ai-", r"llm", r"agent", r"langchain", r"rag", r"embedding", r"vector", r"prompt", r"openai", r"claude", r"gemini", r"copilot", r"semantic", r"similarity-search", r"hybrid-search", r"ml-", r"mlops", r"gepetto"]
    },
    "databases_data": {
        "title": "🗄️ Databases & Data Engineering",
        "patterns": [r"alloydb", r"cloud-sql", r"postgres", r"mysql", r"sqlserver", r"spanner", r"firestore", r"bigquery", r"dbt", r"spark", r"airflow", r"database", r"migration", r"sql", r"data-", r"lakehouse", r"gcs-"]
    },
    "security_compliance": {
        "title": "🔒 Security, Compliance & Hardening",
        "patterns": [r"security", r"secrets", r"sast", r"pci", r"threat", r"attack", r"stride", r"reversing", r"binary", r"malware", r"solidity", r"xss", r"wcag", r"audit", r"hardening", r"auth", r"mtls", r"gdpr"]
    },
    "devops_cloud": {
        "title": "☁️ DevOps, Cloud & Infrastructure",
        "patterns": [r"gcloud", r"gcp", r"k8s", r"kubernetes", r"helm", r"istio", r"linkerd", r"service-mesh", r"turborepo", r"nx-workspace", r"bazel", r"github", r"gitlab", r"deployment", r"observability", r"prometheus", r"grafana", r"datadog", r"incident", r"postmortem", r"slo", r"cost-optimization", r"ci-cd", r"monorepo", r"docker", r"container", r"devops", r"tracing", r"on-call", r"gitops", r"terraform", r"network"]
    },
    "software_architecture": {
        "title": "🏗️ Architecture & Engineering Practices",
        "patterns": [r"architect", r"c4-", r"feature", r"design-pattern", r"clean-code", r"governance", r"requirements", r"onboard", r"microservices", r"saga", r"cqrs", r"event-", r"systems-programming"]
    },
    "software_languages": {
        "title": "💻 Software Engineering & Frameworks",
        "patterns": [r"python", r"cpp", r"c-pro", r"java", r"javascript", r"typescript", r"golang", r"go-", r"rust", r"elixir", r"php", r"ruby", r"scala", r"haskell", r"angular", r"react", r"nextjs", r"django", r"fastapi", r"api-", r"openapi", r"graphql", r"mui", r"tailwind", r"godot", r"unity", r"flutter", r"ios-", r"dotnet", r"csharp", r"bash", r"shell", r"bats", r"posix", r"frontend", r"backend", r"full-stack", r"mobile", r"web", r"arm-cortex", r"firmware", r"blockchain", r"web3", r"defi", r"nft", r"uv-package"]
    },
    "business_finance": {
        "title": "📈 Business, Finance & Strategy",
        "patterns": [r"startup", r"quant", r"risk", r"billing", r"sales", r"stripe", r"paypal", r"payment", r"seo-", r"hr-", r"employment", r"legal", r"business", r"market", r"customer-support"]
    },
    "development_testing": {
        "title": "🛠️ Development, Debugging & QA Workflows",
        "patterns": [r"artifacts", r"mcp", r"skill", r"webapp", r"template", r"dependency", r"changelog", r"commit", r"entropy", r"tdd", r"conductor", r"adr", r"context", r"codebase", r"refactor", r"debug", r"test", r"error", r"diagnostics", r"review", r"qa", r"issue", r"pr-", r"patch", r"performance", r"dx-optimizer", r"memory-"]
    },
    "productivity_comms": {
        "title": "💬 Productivity, Research & Communication",
        "patterns": [r"internal-comms", r"communication", r"conversation", r"feedback", r"raffle", r"research", r"meeting", r"handoff", r"lesson", r"naming", r"domain", r"standup", r"humanizer", r"writing", r"tutorial", r"docs-", r"file-organizer"]
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
            if re.search(pattern, path_str, re.IGNORECASE):
                return cat_key
                
    return "other"

def parse_yaml_frontmatter_fallback(yaml_text):
    data = {}
    lines = yaml_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match key: ...
        key_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if key_match:
            key = key_match.group(1).strip()
            rest = key_match.group(2).strip()
            if rest in ("|", "|-", "|+", ">", ">-", ">+"):
                # Multiline block scalar
                block_lines = []
                i += 1
                while i < len(lines):
                    subline = lines[i]
                    if subline.strip() == "":
                        block_lines.append("")
                        i += 1
                        continue
                    # Check if indented
                    indent_match = re.match(r"^(\s+)(.*)$", subline)
                    if indent_match:
                        block_lines.append(indent_match.group(2))
                        i += 1
                    else:
                        break
                data[key] = "\n".join(block_lines).strip()
                continue
            elif rest == "":
                # Could be multiline without pipe or empty
                block_lines = []
                i += 1
                while i < len(lines):
                    subline = lines[i]
                    if subline.strip() == "":
                        block_lines.append("")
                        i += 1
                        continue
                    indent_match = re.match(r"^(\s+)(.*)$", subline)
                    if indent_match:
                        block_lines.append(indent_match.group(2))
                        i += 1
                    else:
                        break
                if block_lines:
                    data[key] = "\n".join(block_lines).strip()
                else:
                    data[key] = ""
                continue
            else:
                # Value on same line, handle possible continuation lines
                val = rest
                i += 1
                while i < len(lines):
                    subline = lines[i]
                    if subline.strip() == "":
                        break
                    # If line starts with non-space key: break
                    if re.match(r"^[a-zA-Z0-9_-]+:\s*", subline):
                        break
                    indent_match = re.match(r"^\s+(.*)$", subline)
                    if indent_match:
                        val += " " + indent_match.group(1)
                        i += 1
                    else:
                        break
                data[key] = val.strip()
                continue
        i += 1
    return data

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
            name = None
            desc = None
            group_val = None
            if yaml is not None:
                try:
                    parsed = yaml.safe_load(yaml_content)
                    if isinstance(parsed, dict):
                        name = parsed.get("name")
                        desc = parsed.get("description")
                        group_val = parsed.get("group")
                except Exception:
                    pass
            
            if not name or not desc:
                fallback_data = parse_yaml_frontmatter_fallback(yaml_content)
                if not name:
                    name = fallback_data.get("name")
                if not desc:
                    desc = fallback_data.get("description")
                if not group_val:
                    group_val = fallback_data.get("group")
            
            if name:
                name = str(name).strip().strip('"').strip("'")
            else:
                name = os.path.basename(os.path.dirname(skill_md_path))

            if desc:
                desc = str(desc).strip().strip('"').strip("'")
                desc = re.sub(r"\s+", " ", desc)
            else:
                desc = ""
            
            if group_val:
                group_val = str(group_val).strip().strip('"').strip("'")
            
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
            # relative link goes up one level to categories' parent and points to SKILL.md
            skill_link = f"[`{skill['name']}`](../{skill['path']}/SKILL.md)"
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
readme_addition = "\n\n## 🧠 Local Memory RAG Architecture & Token Flow\n\n"
readme_addition += "The repository integrates a local Memory RAG framework (`~/memory_system`) using [`memory-capture`](tools/memory-capture). This system intercepts requests locally, retrieves policy/vector context, and injects it **before** tokens are transmitted to frontier LLMs.\n\n"

readme_addition += "### System Architecture & Data Flow\n\n"
readme_addition += "```mermaid\n"
readme_addition += "flowchart TD\n"
readme_addition += "    subgraph LocalMachine[\"💻 Local Machine (Zero Cloud Tokens Spent)\"]\n"
readme_addition += "        UserReq[\"👤 User Request\"] --> PrePrompt[\"⚡ Pre-Prompt Interceptor\"]\n"
readme_addition += "        PrePrompt --> OKFSearch[\"📄 OKF File Search<br/>~/memory_system/knowledge/okf\"]\n"
readme_addition += "        PrePrompt --> ChromaSearch[\"🔍 ChromaDB Vector Search<br/>~/memory_system/db\"]\n"
readme_addition += "        OKFSearch --> ContextFormat[\"📦 Context Formatter\"]\n"
readme_addition += "        ChromaSearch --> ContextFormat\n"
readme_addition += "        ContextFormat --> AugmentedPayload[\"📝 Augmented Prompt Payload<br/>(System Prompt + RAG + User Query)\"]\n"
readme_addition += "    end\n\n"
readme_addition += "    subgraph CloudModel[\"☁️ Frontier LLM Cloud\"]\n"
readme_addition += "        AugmentedPayload -->|\"Encrypted HTTP / Token Stream\"| FrontierLLM[\"🤖 Gemini / Claude / OpenAI\"]\n"
readme_addition += "        FrontierLLM -->|\"Response Stream\"| AgentResponse[\"✨ Synthesized Response\"]\n"
readme_addition += "    end\n"
readme_addition += "```\n\n"

readme_addition += "### Why & How This Functionality Is Organized\n\n"
readme_addition += "- **Deterministic Policy Routing (OKF)**: High-level architectural rules and security standards are stored as plain Markdown under `~/memory_system/knowledge/okf/` for exact, zero-hallucination regex matching.\n"
readme_addition += "- **Semantic Memory Indexing (ChromaDB)**: Troubleshooting notes, error logs, and code snippets are embedded locally into ChromaDB at `~/memory_system/db/` using local ONNX embeddings.\n"
readme_addition += "- **Automated Inbox Daemon**: Background service `memory-inbox.service` monitors `~/memory_system/inbox/` for new `.md` files and automatically indexes them.\n"
readme_addition += "- **Architectural Decision Record**: See [ADR 0005: Local Memory RAG Architecture](tools/adr/0005-local-memory-rag-architecture.md) for rationale.\n"
readme_addition += "- **Detailed Documentation**: See the complete [Memory RAG FAQ](memory_rag_faq.md) for step-by-step technical details.\n\n"

readme_addition += "### ⚠️ Gotchas & Operational Caveats\n\n"
readme_addition += "> [!WARNING]\n"
readme_addition += "> **Pre-Prompt Token Payload Overflow**: Ingesting raw logs or unchunked files directly into ChromaDB can inflate the injected context payload. Ensure log files are pre-filtered or split into 500–1000 token chunks before dropping into `~/memory_system/inbox/`.\n\n"
readme_addition += "> [!IMPORTANT]\n"
readme_addition += "> **Systemd User Daemon Required**: The inbox background watcher relies on `memory-inbox.service` running under `systemctl --user`. If the service is stopped or disabled, files dropped into `inbox/` will sit unprocessed until `python3 ~/memory_system/capture_knowledge.py <file>` is run manually.\n\n"
readme_addition += "> [!CAUTION]\n"
readme_addition += "> **OKF vs Chroma Routing Triggers**: Files intended for OKF (deterministic policies) **must** contain `# OKF Decision`, `Type: Policy`, or `Type: Architecture Standard` in their header. Without these exact header strings, `capture_knowledge.py` defaults to embedding the content into ChromaDB vector storage.\n\n"
readme_addition += "> [!NOTE]\n"
readme_addition += "> **Directory Tree Initializer**: If `~/memory_system` is missing or cleared, running `python3 ~/memory_system/init_storage.py` must be executed before ingestion to recreate required SQLite tables and collection schemas.\n\n"

readme_addition += "## 📚 Skill Catalog & Navigation\n"
readme_addition += f"\nThis repository manages **{len(user_skills) + len(config_skills)}** modular AI skills across 12 primary domains.\n\n"

# Overview Table
readme_addition += "### Overview\n\n"
readme_addition += "| Category | Skills | Quick Link |\n"
readme_addition += "|---|---|---|\n"

for cat_key, cat_info in USER_CATEGORIES.items():
    skills_in_cat = user_by_cat.get(cat_key, [])
    if skills_in_cat:
        link = f"[{cat_info['title']}](#-{cat_key.replace('_', '-')})"
        count = f"**{len(skills_in_cat)}**"
        doc_link = f"[Full Doc ↗](categories/{cat_key}.md)"
        readme_addition += f"| {link} | {count} | {doc_link} |\n"

if other_user:
    readme_addition += f"| [📦 Other User Skills](#-other-user-skills) | **{len(other_user)}** | [Full Doc ↗](categories/other_user.md) |\n"

readme_addition += "\n---\n\n"

# Detailed Category Sections with direct skill links
for cat_key, cat_info in USER_CATEGORIES.items():
    skills_in_cat = user_by_cat.get(cat_key, [])
    if skills_in_cat:
        readme_addition += f"### {cat_info['title']}\n"
        readme_addition += f"📁 *Full Documentation: [{cat_info['title']} Document](categories/{cat_key}.md) ({len(skills_in_cat)} skills)*\n\n"
        
        # Deduplicate skills by name for display list
        unique_skills = {}
        for s in skills_in_cat:
            if s["name"] not in unique_skills:
                unique_skills[s["name"]] = s
        
        skill_links = []
        for s_name, s_info in sorted(unique_skills.items()):
            skill_links.append(f"[`{s_name}`]({s_info['path']}/SKILL.md)")
        
        readme_addition += " • ".join(skill_links) + "\n\n"

if other_user:
    readme_addition += "### 📦 Other User Skills\n"
    readme_addition += f"📁 *Full Documentation: [Other User Skills Document](categories/other_user.md) ({len(other_user)} skills)*\n\n"
    unique_skills = {}
    for s in other_user:
        if s["name"] not in unique_skills:
            unique_skills[s["name"]] = s
    skill_links = [f"[`{s_name}`]({s_info['path']}/SKILL.md)" for s_name, s_info in sorted(unique_skills.items())]
    readme_addition += " • ".join(skill_links) + "\n\n"

# Read original README up to the separator
original_content = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        original_content = f.read()

# Cut off any existing generated sections (Memory RAG or Skill Catalog)
cutoff_marker = "## 🧠 Local Memory RAG Architecture"
if cutoff_marker in original_content:
    original_content = original_content.split(cutoff_marker)[0].strip()
elif "## 📚 Skill Catalog" in original_content:
    original_content = original_content.split("## 📚 Skill Catalog")[0].strip()

new_content = original_content.strip() + "\n" + readme_addition

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"README.md and category documents updated successfully with {len(user_skills)} user skills and {len(config_skills)} config skills.")
