def disable_virtual_service(api_client, vs):
    print("\n--- TASK / TRIGGER STAGE ---")

    if not vs.get("enabled"):
        print(
            f"Virtual Service '{vs['name']}' is already disabled. Skipping PUT."
        )
        return vs

    payload = {"enabled": False}
    response = api_client.put(
        f"/api/virtualservice/{vs['uuid']}",
        payload
    )

    print(
        f"Virtual Service '{vs['name']}' disable request sent"
    )
    return response
    