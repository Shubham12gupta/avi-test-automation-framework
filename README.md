# Avi Load Balancer – Python Test Automation Framework

## Overview
This project is a Python-based modular test automation framework designed to interact with a mock VMware Avi Load Balancer API.  
It demonstrates configuration-driven automation, REST API interaction, validation gates, and safe state-changing operations.

The framework follows a structured test lifecycle:
1. Pre-Fetch
2. Pre-Validation
3. Task / Trigger
4. Post-Validation

---

## Folder Structure
avi_test_framework/
├── config/
│ ├── env.yaml
│ └── testcases.yaml
│
├── core/
│ ├── api_client.py
│ ├── prefetch.py
│ ├── validation.py
│ └── task.py
│
├── mocks/
│ ├── ssh.py
│ └── rdp.py
│
├── runner.py
├── requirements.txt
└── README.md


---

---

## Configuration

### env.yaml
Contains environment and authentication details:
```yaml
base_url: https://semantic-brandea-banao-dc049ed0.koyeb.app
auth:
  username: <your_username>
  password: <your_password>
testcases.yaml
Defines test cases dynamically:

yaml
Copy code
tests:
  - name: disable_virtual_service_test
    target_vs_name: backend-vs-t1r_1000-1
Test Workflow
1. Pre-Fetch
Fetches tenants, virtual services, and service engines

Logs resource counts

Read-only operation

2. Pre-Validation
Identifies the target Virtual Service

Ensures it is enabled before modification

3. Task / Trigger
Sends a PUT request using the Virtual Service UUID

Disables the Virtual Service

Operation is idempotent (safe for retries)

4. Post-Validation
Confirms the Virtual Service is disabled using a GET request

Mock Components
The framework includes stubbed methods for:

SSH

RDP

These are placeholders to demonstrate extensibility and do not establish real connections.

How to Run
1. Create virtual environment
bash
Copy code
python -m venv venv
venv\Scripts\activate
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Execute the test
bash
Copy code
python runner.py
Key Design Decisions
YAML-driven configuration for flexibility

Centralized API client for authentication and HTTP handling

Validation gates to prevent unsafe state changes

Idempotent operations for reliability

Conclusion
This framework demonstrates safe, modular, and configurable automation practices aligned with real-world DevOps and SRE workflows.

yaml
Copy code

This README is **interview-grade**.  
Don’t over-edit it.

---

#PART 2 — PARALLEL EXECUTION (OPTIONAL BUT STRONG)

You already support **multiple test cases**.  
Now we’ll add **parallel execution** cleanly.

### 🔹 Update `runner.py` (ONLY this small change)

At the top, add:
```python
from concurrent.futures import ThreadPoolExecutor
Replace this part:

python
Copy code
for test in tests:
    ...
With this:

python
Copy code
def run_test(test):
    print("\n--- PRE-VALIDATION STAGE ---")
    vs = find_vs_by_name(virtual_services, test["target_vs_name"])
    validate_vs_enabled(vs)

    disable_virtual_service(client, vs)

    print("\n--- POST-VALIDATION STAGE ---")
    vs_after = client.get(f"/api/virtualservice/{vs['uuid']}")
    if vs_after.get("enabled") is False:
        print(f"Post-validation passed: {vs_after['name']} disabled")
    else:
        raise Exception("Post-validation failed")


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(run_test, tests)
