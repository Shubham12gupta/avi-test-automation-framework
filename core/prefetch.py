def prefetch_resources(api_client):
    print("\n--- PRE-FETCH STAGE ---")

    tenants = api_client.get("/api/tenant")
    virtual_services = api_client.get("/api/virtualservice")
    service_engines = api_client.get("/api/serviceengine")

    tenant_count = len(tenants.get("results", []))
    vs_count = len(virtual_services.get("results", []))
    se_count = len(service_engines.get("results", []))

    print(f"Tenants found        : {tenant_count}")
    print(f"Virtual Services found: {vs_count}")
    print(f"Service Engines found : {se_count}")

    return virtual_services.get("results", [])
    