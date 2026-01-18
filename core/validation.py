def find_vs_by_name(virtual_services, target_name):
    for vs in virtual_services:
        if vs.get("name") == target_name:
            return vs
    return None


def validate_vs_enabled(vs):
    if not vs:
        raise Exception("Target Virtual Service not found")

    if vs.get("enabled") is not True:
        raise Exception(
            f"Validation failed: Virtual Service '{vs['name']}' is already disabled"
        )

    print(
        f"Pre-validation passed: Virtual Service '{vs['name']}' is enabled"
    )
    