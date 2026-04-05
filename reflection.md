# Detailed Reflection – Auto PPT Agent using MCP

## 1. Introduction

The objective of this assignment was to design and implement an Auto PPT Agent capable of generating presentation slides automatically from a user prompt. The agent was required to follow an agentic workflow using multiple MCP servers, instead of relying on a single LLM call. The system needed to demonstrate planning, decision-making, tool usage, and structured output generation.

---

## 2. Initial Approach

Initially, the system was implemented using a single LLM call where the model generated all slide content at once. This approach produced text output, but it did not resemble a real presentation workflow. There was no planning step, and slide generation logic was hardcoded in the script. As a result:

* The slides were inconsistent
* No structured workflow existed
* The system lacked modularity
* Debugging was difficult
* No intermediate outputs were available
* It did not satisfy the agentic architecture requirement

This approach did not align with the assignment requirement that the agent must make decisions and call tools iteratively.

---

## 3. Problems Observed

The major issues in the initial implementation were:

### 3.1 No Planning Phase

The agent directly generated slide content without creating an outline. This caused:

* Repetitive slides
* Missing sections
* Poor slide flow

### 3.2 Hardcoded Execution

Slides were generated using fixed loops without dynamic decision-making. This made the system less flexible and not truly agentic.

### 3.3 No Tool Separation

All logic was inside a single file. There was no separation between:

* Planning
* Content generation
* File creation

### 3.4 Lack of Observability

Since intermediate outputs were not stored, it was difficult to understand:

* What the agent planned
* How content was generated
* Where errors occurred

---

## 4. Introduction of MCP Architecture

To solve these issues, Model Context Protocol (MCP) servers were introduced. MCP allowed separation of responsibilities and enabled a modular architecture.

Two MCP servers were implemented:

### 4.1 Filesystem MCP Server

Responsibilities:

* Save outline.json
* Save slide_content.json
* Store intermediate planning data

Benefits:

* Provided transparency in agent planning
* Enabled debugging
* Showed explicit planning phase

### 4.2 PPT MCP Server

Responsibilities:

* Create presentation
* Add title slide
* Add content slides
* Apply themes
* Save presentation file

Benefits:

* Clean separation of slide creation
* Reusable tool interface
* Structured output generation

---

## 5. Final Agent Workflow

The final system followed a true agentic pipeline:

User Input
↓
LLM generates presentation title
↓
LLM generates structured outline
↓
Filesystem MCP saves outline.json
↓
Agent loops through each slide
↓
LLM generates bullet content
↓
Filesystem MCP saves slide_content.json
↓
PPT MCP creates slides
↓
PPT MCP saves final presentation

This workflow clearly demonstrates:

* Planning
* Decision making
* Tool usage
* Execution loop
* Final output generation

---

## 6. Agentic Decision Making

The agent performs multiple decisions:

* Determine presentation title
* Decide slide structure
* Generate slide content
* Choose theme styling
* Call appropriate MCP tools
* Save outputs

This satisfies the requirement of an agent making iterative decisions instead of executing a fixed script.

---

## 7. Robustness Improvements

The system was improved to handle:

* Long user prompts
* Vague prompts
* Missing structure
* JSON parsing failures
* Theme selection

Fallback logic ensures:

* Outline is always generated
* Slides always created
* Application does not crash

---

## 8. Output Quality Improvements

To improve presentation quality:

* Themes were added
* Title styling improved
* Bullet formatting standardized
* Accent bars added
* Consistent font sizes applied

These changes produced visually structured presentations.

---

## 9. Benefits of MCP-Based Agent

Using MCP provided multiple advantages:

* Modular architecture
* Separation of concerns
* Reusable tools
* Clear planning step
* Improved debugging
* Scalable design
* Better code organization
* Real agentic workflow

---

## 10. Comparison with Non-Agentic Approach

| Non-Agentic            | MCP Agentic           |
| ---------------------- | --------------------- |
| Single LLM call        | Multi-step planning   |
| Hardcoded logic        | Tool-based execution  |
| No intermediate output | Saved planning files  |
| Poor modularity        | Separated MCP servers |
| Difficult debugging    | Transparent workflow  |
| Limited scalability    | Easily extensible     |

---

## 11. Conclusion

The final implementation successfully transformed a simple script into a fully agentic Auto PPT system. The agent now plans the presentation, generates slide content, and uses MCP tools to construct the final output. The use of multiple MCP servers improved modularity, transparency, and robustness. The final solution meets all assignment requirements and demonstrates a clear agentic architecture.

The project highlights how MCP can be used to build structured, scalable, and tool-driven AI agents for real-world automation tasks.
