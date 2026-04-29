<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Ursa Weaver: Agentic AI Tutoring System

Ursa Weaver is a framework for building highly personalized, graph-based AI tutoring sessions. Unlike linear "next lesson" systems, Ursa Weaver treats technical skills as nodes in a directed graph, allowing a tutor to navigate unlocked paths based on a learner's mastered dependencies.

---

## 🚀 Key Features

- **Graph-Based Roadmaps**: Skills are defined as nodes with explicit dependencies, enabling non-linear learning paths.
- **Unified User State**: Persistent identity, progress, and session context are stored in a single, portable JSON file.
- **Dynamic Pedagogy**: The tutor uses the learner's background, interests, and personas to generate tailored metaphors and explanations.
- **Extensible Verifications**: Integrated support for Multiple Choice, CLI command checks, MCP tool results, and LLM-based rubrics.
- **Agentic Logic**: Designed to run as an autonomous "Skill" for AI agents (e.g., in a development environment or IDE).

---

## 📂 Repository Structure

- `curricula/`: The "knowledge base" containing JSON-based skill graphs (e.g., Go ADK).
- `users/`: Unified JSON files for individual learners. (Git-ignored to protect privacy).
- `debugging/`: Verification scripts and a comprehensive test suite for graph integrity.
- `.agents/skills/llm_tutor/`: The implementation protocol for the AI tutor.
- `docs/`: Technical deep-dives into the architecture and schemas.

---

## 🛠️ Getting Started

### 1. Prerequisites
- An AI Agent capable of interpreting the `llm_tutor` skill (e.g., Gemini-powered coding assistant).
- Python 3.10+ (for verification scripts).

### 2. How to Run
Invoke the `llm_tutor` skill within your agent's environment:
1. Provide the path to a curriculum file: `curricula/adk_go_curriculum_poc.json`.
2. Provide your `user_id` (this will load or create your unified state file in `users/`).
3. Follow the tutor's guidance as it identifies unlocked skills and presents choices.

---

## 📊 Data Model Overview

### Curriculum (Graph)
Defined in `curricula/*.json`. 
- **Skill Nodes**: Contain title, category, description, and dependencies.
- **Verifications**: Define how mastery is proven (e.g., `command_check` to see if a CLI was installed).

### Unified User State
Defined in `users/<user_id>.json`.
- **Profile**: Identity and technical background.
- **Progress**: A persistent list of mastered and fast-tracked skill IDs.
- **Session**: Temporary context including `current_node_id` and today's learning goal.

---

## 🧪 Verification & Reliability

Ensuring the integrity of the curriculum graph is critical for a smooth user experience.

- **Integrity Check**: Verifies that all dependencies point to valid nodes and the graph is fully connected.
  ```bash
  python3 debugging/verify_json.py
  ```
- **Functional Test Suite**: Exercises the unified state logic and dependency resolution.
  ```bash
  python3 debugging/test_suite.py
  ```

## ⚖️ License
This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

---

This is not an officially supported Google product. This project is not eligible for the [Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security).
