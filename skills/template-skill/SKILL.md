---

name: template-skill

description: |

  Template blueprint and structural guide for creating Grade-A compliant Claude skills. Trigger when initializing a new skill directory, writing a skeleton SKILL.md file, or reviewing a skill file template for standard formatting. Keywords: template-skill, skeleton, placeholder, blueprint, frontmatter schema, design guidelines.



  Template blueprint and structural guide for creating Grade-A compliant Claude skills. Trigger when initializing a new skill directory, writing a skeleton SKILL.md file, or reviewing a skill file template for standard formatting. Keywords: template-skill, skeleton, placeholder, blueprint, frontmatter schema, design guidelines.



---



# [Skill Name] - [Short Catchy Title]



[Provide a high-level summary of the skill's purpose, what operations it simplifies, and the benefits of using it.]



## Progressive Disclosure & External Resources



[Explicitly state here if this skill is self-contained, or if it relies on external files (e.g., scripts, references, assets). Detail the commands or imports required to run or trigger them without reading the source code.]



- **External Resources**: [List resources, e.g. "This is a self-contained skill. Do NOT load external files or reference directories." OR list specific scripts and how to execute/import them.]



## Freedom Calibration & Constraints

- **Constraint Level: [High / Medium / Low]**

  - **High Rigidity**: [Specify exactly what must be followed without exception (e.g., schemas, CLI flags, output formats).]

  - **High Freedom**: [Specify where the agent has creative/implementation flexibility (e.g., code design, style choices, troubleshooting paths).]



## Decision Tree: Choosing the Right Approach



[Include an ASCII diagram or text-based decision tree that helps the agent select the right sub-procedure or tool based on the user's input/scenario.]



```

User Input/Scenario

 ├─ [Condition A] → [Use Procedure A]

 ├─ [Condition B] → [Use Procedure B]

 └─ [Condition C] → [Fallback/Alternative]

```



## Professional Mindset & Design Principles

1. **[Principle 1]**: [Describe a mental framework or domain-specific lens to look through.]

2. **[Principle 2]**: [Describe another key optimization or strategy.]

3. **[Principle 3]**: [Describe error prevention or sanity-checking strategies.]



---



## Step-by-Step Execution Procedure

### Step 1: Pre-Flight Context, Memory Recall & Fork Guardrail
- Run pre-flight memory retrieval to load applicable policies and prior lessons learned:
  ```bash
  python3 ~/memory_system/inspect_memory.py --preflight .
  ```
- If operating on a git repository, verify origin and upstream maintenance status:
  ```bash
  python3 ~/memory_system/check_fork_guardrail.py .
  ```
  *If target is an active fork, HALT direct updates. Propose upstream PR or sync with `gh repo sync`.*

### Step 2: [Phase Name]
- [Instruction in imperative form, e.g., "Analyze the input specifications..."]
- [Instruction, e.g., "Execute the primary utility script..."]

### Step 3: [Phase Name]
- [Instruction, e.g., "Generate the initial output representation..."]
- [Instruction, e.g., "Perform verification and quality assurance checks..."]

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** unilaterally update an active forked repository | Diverges from upstream source of truth, creating conflicts and breaking sync | Refresh fork with `gh repo sync` or submit PR to upstream |
| **NEVER** bypass local memory pre-flight recall | Causes amnesia and repeats previously solved mistakes or violates OKF policies | Run `inspect_memory.py --preflight .` prior to formulating plan |
| **NEVER** deploy code changes without test validation | Introduces regressions into default branches | Run test harness before committing |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: [Error Trigger / Symptom]
- **Root Cause**: [Explain why this happens.]
- **Fallback**:
  1. [Step-by-step fallback action 1]
  2. [Step-by-step fallback action 2]

### Scenario 2: Active Fork Detected During Guardrail Check
- **Root Cause**: Target repository is a fork of an active open-source project.
- **Fallback**:
  1. Refresh the fork from upstream: `gh repo sync <owner>/<repo>`.
  2. If contributing changes, create a feature branch targeting the upstream parent.

## Two-Phase Memory Lifecycle

Every skill must participate in the bi-directional memory protocol:

### Phase 1: Pre-Flight Memory Recall
Before executing code, modifying files, or planning architecture, retrieve local context and lessons learned:
```bash
python3 ~/memory_system/inspect_memory.py --preflight .
# Or domain search:
python3 ~/memory_system/inspect_memory.py -q "<domain_keyword>"
```

### Phase 2: Post-Execution Memory Capture
After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger local memory capture:
1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).

