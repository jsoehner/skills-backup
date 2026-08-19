---

name: content-research-writer

description: |

  Assists in researching, outlining, drafting, and refining high-quality, cited content while preserving the author's unique voice. Trigger when a user needs to: (1) Outline, draft, or edit long-form articles, newsletters, tutorials, or documentation, (2) Conduct web research and compile verified references, (3) Improve opening hooks, transitions, or structural flow, or (4) Format citations and cross-references. Keywords: draft, outline, edit, article, blog, newsletter, hook, citation, research, rewrite, proofread, bibliography, format.



---



# Content Research Writer



This is a self-contained skill. Do NOT load external files or reference external directories unless specifically instructed by the user.



---



## 1. Trigger Scenarios & Decision Trees



### Strategic Intent & Use Cases

Use this skill when:

- Designing content architecture (outlining complex narratives or technical guides).

- Performing deep research to extract statistics, expert quotes, or academic sources.

- Elevating hooks, introductions, or section flow.

- Analyzing and matching a specific writer's style/voice.

- Performing developmental editing, copyediting, or formatting bibliography.



### Workflow & Decision Tree

```mermaid

graph TD

    A[User Request] --> B{What is the primary objective?}

    B -->|Create Outline/Structure| C[Outlining Workflow]

    B -->|Find Evidence/Data| D[Research & Citation Workflow]

    B -->|Review/Refine Draft| E{Review Scope?}

    E -->|Intro Hook| F[Hook Optimization]

    E -->|Single Section| G[Section-by-Section Review]

    E -->|Full Draft| H[Comprehensive Edit & Polish]

    

    C --> C1[Analyze target audience, tone & core thesis]

    C1 --> C2[Identify logical progression & research gaps]

    

    D --> D1[Verify primary sources & extract metrics]

    D1 --> D2[Apply selected citation format]

    

    F --> F1[Select Hook Archetype based on audience]

    

    G --> G1[Analyze Flow, Evidence & Voice Alignment]

```



---



## 2. Constraints & Freedom Calibration



*   **Outline Architecture (Medium Freedom)**: Adjust layout formats to match content needs, but maintain logical hierarchy (Introduction -> Main Arguments -> Counterpoints/Nuance -> Actionable Takeaway/Conclusion).

*   **Voice & Tone Preservation (High Freedom)**: Adapt heavily to the user's style. Do not force generic "corporate friendly" or "AI-assistant" tones unless requested.

*   **Citations & Fact Verification (Low Freedom)**: Never invent statistics or extrapolate quotes. Cite only verified, credible sources. Use exact formats (APA, MLA, Chicago, or Inline/Numbered).



---



## 3. Expert-Level Knowledge Delta



### Voice Profile Modeling Framework

To accurately match the user's voice, analyze their writing samples across these dimensions:

1.  **Lexicon (Word Choice)**: Is it jargon-heavy, academic, colloquial, or simplified? (e.g., using "utilize" vs. "use", or "leverage" vs. "harness").

2.  **Syntax (Sentence Variety)**: Do they use short, punchy fragments, or long, complex clauses? Look for patterns in sentence length.

3.  **Perspective**: Is it first-person ("I", "we"), second-person ("you"), or objective third-person?

4.  **Tone**: Bold/provocative, analytical/empirical, warm/conversational, or authoritative.



### Hook Archetype Selection Matrix

Select the appropriate opening style depending on the audience and goals:



| Archetype | Best For | Mechanics | Example |

| :--- | :--- | :--- | :--- |

| **The Counter-Intuitive Truth** | Thought Leadership, Business | State a widely held belief, then explain why it's wrong. | "Every project manager is told to avoid scope creep. But trying to prevent it is actually killing your innovation." |

| **The Micro-Narrative** | Newsletters, Case Studies | Open with a brief, high-tension moment. | "Sarah stared at the error log. It was 3:00 AM, and the deployment script had just deleted their primary database." |

| **The Raw Data Punch** | Technical Reports, Research | Lead with a shocking, verified statistic. | "73% of product launches fail not because of technology, but because of poor user distribution planning." |

| **The Relatable Problem** | Tutorials, How-To Guides | Start with a direct question addressing a common pain point. | "If you've ever spent three hours troubleshooting a Webpack configuration only to find a missing comma, this guide is for you." |



---



## 4. Mindset & Actionable Procedures



### Self-Inquiry Framework (Think Before You Write)

Before drafting or proposing changes, ask yourself:

*   *Who is reading this, and what is their current level of expertise on the subject?*

*   *Does this draft present a unique angle, or is it repeating generic search-engine-optimized content?*

*   *Are the transitions between paragraphs logical, or are we jumping abruptly between ideas?*

*   *Did I preserve the writer's style, or did I homogenize it into a generic style?*



### Step-by-Step Writing & Editing Sequence

1.  **Intake & Profiling**:

    *   Review instructions and samples. Extract vocabulary patterns, length preferences, and target audience expectations.

2.  **Structural Mapping (Outlining)**:

    *   Construct an outline map detailing the purpose of each section.

    *   Tag sections requiring empirical evidence: `[Research needed: Topic]`.

3.  **Drafting/Refinement (Iterative)**:

    *   Work section-by-section. Do not dump the entire draft in one turn unless the file is short.

    *   For edits, provide: (1) Strengths, (2) Specific line-by-line comparison, (3) Rationale for changes.

4.  **Verification**:

    *   Cross-check assertions against research sources. Ensure citation mapping matches user format.

5.  **Voice Tuning**:

    *   Scan output for generic AI phrases ("delve", "testament", "tapestry", "in summary", "moreover"). Replace with natural transitions matching the writer's voice.



---



## 5. Anti-Patterns & Never-Lists



| Action | Why Avoid It | Correction/Alternative |

| :--- | :--- | :--- |

| **NEVER** invent, estimate, or hallucinate citations or statistics. | Destroys credibility and introduces falsehoods. | Use placeholders like `[Source Needed]` or run web searches to find real, verified statistics. |

| **NEVER** overwrite the writer's style with standard "AI voice". | Makes the content sound robotic and identical to typical AI output. | Match vocabulary, sentence lengths, and structure of user's samples. |

| **NEVER** edit a full draft without first aligning on the outline/thesis. | Leads to misaligned drafts, wasted effort, and massive rewrites. | Confirm outline, goals, and section-by-section focus before editing. |

| **NEVER** use clichés or generic transition words ("furthermore", "lastly"). | Weakens prose and lowers the overall authority of the writing. | Use logical context transitions instead of mechanical signposts. |

| **NEVER** accept assertions without supporting evidence. | Weakens the author's argument and compromises content quality. | Flag assertions that lack proof and prompt the user to add data or search for it. |



---



## 6. Error Scenarios & Fallbacks



### Mismatched Voice

*   *Scenario*: User states: "This doesn't sound like me. It's too formal/corporate."

*   *Fallback*: Ask for a short paragraph they wrote themselves. Break it down using the *Voice Profile Modeling Framework* (lexicon, syntax, perspective) and revise the section using those constraints.



### Source Contradiction

*   *Scenario*: Web search reveals that the statistic the user wants to cite is outdated or refuted by a more credible study.

*   *Fallback*: Alert the user to the conflict. Show them both sources (old vs. new) and suggest updated phrasing. E.g., *"The 80% statistic from 2021 was updated in a 2025 study to 45%. I suggest using the newer figure to maintain credibility."*



### Flow Breakdown

*   *Scenario*: The transition between two major sections feels jarring or disconnected.

*   *Fallback*: Identify the logical gap. Create a "bridge" sentence or short paragraph at the end of the first section or the beginning of the second that explicitly links the two concepts together.


