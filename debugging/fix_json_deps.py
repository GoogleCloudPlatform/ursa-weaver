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

def fix_dependencies(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if 'skills' in data:
        for skill in data['skills']:
            if 'dependencies' in skill:
                new_deps = []
                for dep in skill['dependencies']:
                    if isinstance(dep, str):
                        new_deps.append({'id': dep, 'type': 'hard'})
                    else:
                        new_deps.append(dep)
                skill['dependencies'] = new_deps
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    fix_dependencies('curricula/adk_go_curriculum_poc.json')
    print("Fixed dependencies in curricula/adk_go_curriculum_poc.json")
