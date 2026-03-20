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

# Pathweaver System Architecture

This document defines the data structures for the Pathweaver curriculum and the flat, unified user state model.

---

## 1. Curriculum Schema
Located in `curricula/*.json`. Defines the learning path and mastery requirements.

### Root Fields
- `curriculum_id`: Unique identifier for the learning path.
- `version`: Version string (e.g., '1.0').
- `description`: High-level summary of the track.
- `skills`: An array of Skill Nodes.

### Skill Node Structure
- `id`: Unique identifier (e.g., `install_go`).
- `title`: Human-readable name.
- `category`: Grouping for UI/discovery (e.g., `go_development`).
- `dependencies`: List of objects:
  - `id`: The dependent skill ID.
  - `type`: `hard` (required) or `recommended`.
- `description`: The educational summary of the skill.
- `fast_track_assessment`: A concise prompt used to skip the lesson if the user already knows the topic.
- `verification`: A block defining how mastery is proven.

### Verification Types
- `multiple_choice`: `question`, `options` (list of `id`, `text`), `correct_answer_id`.
- `command_check`: `command`, `expected_output` (supports `regex:` prefix).
- `mcp_check`: `mcp_server`, `mcp_tool`, `arguments`, `expected_result_field`, `expected_value`.
- `code_test`: `validation_script` or `test_command`.
- `llm_rubric`: `instructions_to_user`.

---

## 2. Unified User State Model

Pathweaver stores all user-specific data in a single JSON file per user.

### User State Structure
**Path**: `users/<user_id>.json`
- **Purpose**: A single source of truth for who the user is, what they know, and where they are in the curriculum.
- **Git Status**: 🔒 **Ignored** (via `.gitignore`).
- **Key Sections**:
  - `profile`:
    - `display_name`: How the tutor addresses the user.
    - `background`: Prior experience and technical context.
    - `interests`: Topics the user cares about.
  - `progress`:
    - `skills_mastered`: List of IDs verified via assessment.
    - `skills_fast_tracked`: List of IDs skipped via fast-track assessment.
  - `session`:
    - `current_curriculum_id`: The active curriculum track.
    - `current_node_id`: The current skill the tutor is teaching.
    - `today_goal`: The user's specific objective for the current session.
    - `last_interaction`: Timestamp of the last interaction.
