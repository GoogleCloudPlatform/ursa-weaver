# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sys
from pathlib import Path

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def test_curricula_integrity():
    print("--- Testing Curricula Integrity ---")
    curricula_dir = Path("curricula")
    for curriculum_path in curricula_dir.glob("*.json"):
        print(f"Checking {curriculum_path.name}...")
        data = load_json(curriculum_path)
        
        # 1. Basic Structure
        assert "curriculum_id" in data
        assert "skills" in data
        
        skill_ids = {s["id"] for s in data["skills"]}
        
        # 2. Skill Dependencies
        for skill in data["skills"]:
            assert "id" in skill
            assert "title" in skill
            for dep in skill.get("dependencies", []):
                dep_id = dep["id"] if isinstance(dep, dict) else dep
                assert dep_id in skill_ids, f"Skill {skill['id']} has invalid dependency: {dep_id}"
    print("✅ Curricula Integrity Verified!")

def test_user_state_consistency():
    print("\n--- Testing User State Consistency ---")
    user_id = "sample_user"
    user_path = Path(f"users/{user_id}.json")
    assert user_path.exists(), f"User file {user_path} missing!"
    
    data = load_json(user_path)
    assert data["user_id"] == user_id
    assert "profile" in data
    assert "progress" in data
    assert "session" in data
    
    # Check if current_node_id exists in the default curriculum
    curr_id = data["session"]["current_curriculum_id"]
    curr_path = Path(f"curricula/{curr_id}.json")
    if curr_path.exists():
        curr_data = load_json(curr_path)
        skill_ids = {s["id"] for s in curr_data["skills"]}
        node_id = data["session"]["current_node_id"]
        assert node_id in skill_ids, f"Current node {node_id} not found in {curr_id}!"
    print("✅ User State Consistency Verified!")

def test_dependency_resolution():
    print("\n--- Testing Dependency Resolution Logic ---")
    # Simulation: What skills are available if 'install_tools' is mastered?
    data = load_json("curricula/adk_go_curriculum_poc.json")
    skills = data["skills"]
    mastered = {"install_tools"}
    
    available = []
    for skill in skills:
        if skill["id"] in mastered:
            continue
            
        deps_met = True
        for dep in skill.get("dependencies", []):
            dep_id = dep["id"] if isinstance(dep, dict) else dep
            # For simplicity, we only consider 'hard' dependencies as blocking
            dep_type = dep.get("type", "hard") if isinstance(dep, dict) else "hard"
            
            if dep_type == "hard" and dep_id not in mastered:
                deps_met = False
                break
        
        if deps_met:
            available.append(skill["id"])
            
    print(f"Mastered: {mastered}")
    print(f"Available: {available}")
    assert len(available) > 0, "No skills available after mastering a root node!"
    print("✅ Dependency Resolution Verified!")

def test_persona_loading():
    print("\n--- Testing Personas ---")
    data = load_json("personas.json")
    assert "user_personas" in data, "Missing 'user_personas' key in personas.json"
    personas = data["user_personas"]
    assert isinstance(personas, list)
    for persona in personas:
        assert "id" in persona
        assert "description" in persona
    print("✅ Personas Verified!")

if __name__ == "__main__":
    try:
        test_curricula_integrity()
        test_user_state_consistency()
        test_dependency_resolution()
        test_persona_loading()
        print("\n✨ ALL TESTS PASSED! Coverage is good for core OSS use cases.")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
