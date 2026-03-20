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
from collections import deque

def verify(json_path=None):
    if not json_path:
        json_path = 'curricula/adk_go_curriculum_poc.json'
    with open(json_path, 'r') as f:
        data = json.load(f)

    skill_ids = {s['id'] for s in data.get('skills', [])}
    errors = []

    # Undirected connectivity check (islands)
    adj = {sid: set() for sid in skill_ids}
    for skill in data.get('skills', []):
        for dep_obj in skill.get('dependencies', []):
            dep = dep_obj['id'] if isinstance(dep_obj, dict) else dep_obj
            if dep in adj:
                adj[skill['id']].add(dep)
                adj[dep].add(skill['id'])
    
    components = []
    visited = set()
    for sid in skill_ids:
        if sid not in visited:
            component = set()
            q = deque([sid])
            while q:
                curr = q.popleft()
                if curr not in visited:
                    visited.add(curr)
                    component.add(curr)
                    for neighbor in adj[curr]:
                        q.append(neighbor)
            components.append(component)

    if len(components) > 1:
        errors.append(f"Error: The graph is split into {len(components)} disconnected islands.")
        for i, comp in enumerate(components):
            print(f"Island {i+1} ({len(comp)} nodes): {list(comp)[:3]}...")
    else:
        print("Success: All nodes are connected in a single graph structures.")

    if not errors:
        print("Verification successful: No integrity or connectivity issues found.")
    else:
        for err in errors:
            print(err)

if __name__ == "__main__":
    verify()
