import yaml
from core.api_client import APIClient
from core.prefetch import prefetch_resources
from core.validation import find_vs_by_name, validate_vs_enabled
from core.task import disable_virtual_service

with open("config/env.yaml") as f:
    env = yaml.safe_load(f)

with open("config/testcases.yaml") as f:
    tests = yaml.safe_load(f)["tests"]

client = APIClient(env["base_url"])
client.register(env["auth"]["username"], env["auth"]["password"])
client.login(env["auth"]["username"], env["auth"]["password"])

virtual_services = prefetch_resources(client)

for test in tests:
    print("\n--- PRE-VALIDATION STAGE ---")
    vs = find_vs_by_name(virtual_services, test["target_vs_name"])
    validate_vs_enabled(vs)

    updated_vs = disable_virtual_service(client, vs)

    print("\n--- POST-VALIDATION STAGE ---")
    vs_after = client.get(f"/api/virtualservice/{vs['uuid']}")

    if vs_after.get("enabled") is False:
        print(
            f"Post-validation passed: Virtual Service '{vs_after['name']}' is disabled"
        )
    else:
        raise Exception("Post-validation failed: VS is still enabled")

print("\n✅ TEST WORKFLOW COMPLETED SUCCESSFULLY")
