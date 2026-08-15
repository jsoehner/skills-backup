import os

# List of built-in pi agents to "import" as skills
agents = [
    "advisor",
    "context-builder",
    "delegate",
    "oracle",
    "planner",
    "researcher",
    "reviewer",
    "scout",
    "worker"
]

base_path = r'C:/Users/jsoehner/.pi/agent/skills'

# Ensure the base path exists
if not os.path.exists(base_path):
    os.makedirs(base_path)

for agent in agents:
    agent_path = os.path.join(base_path, agent)
    
    # Create the directory
    if not os.path.exists(agent_path):
        os.makedirs(agent_path)
        print(f"Created directory: {agent_path}")
    
    # Create the SKILL.md file
    skill_file = os.path.join(agent_path, "SKILL.md")
    
    # Content for the SKILL.md
    # Since these are built-in agents, the skill describes the agent's role in the system.
    content = f"""# {agent.replace('-', ' ').title()}

## When to Use
Use the {agent} agent for tasks requiring its specific core functionality. This is a built-in pi agent.

## Procedure
1. Call the {agent} agent directly or via a chain/parallel task.
2. Provide the necessary requirements or context.
3. The {agent} will perform its specialized role (e.g., planning, research, review, or orchestration).

## Pitfalls
- Ensure you provide clear instructions; built-in agents are powerful but require well-defined goals.
- For multi-step tasks, consider using a chain to pass information between different agents.

## Verification
- The {agent} agent returns the expected output in the requested format.
- The logic follows the expected behavior for its specific role.
"""
    
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created SKILL.md for: {agent}")

print("\nAll built-in agents have been imported as skills.")
