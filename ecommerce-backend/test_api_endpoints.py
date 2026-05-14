import requests
import json
import re

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@ecommerce.com"
ADMIN_PASSWORD = "Admin@123456"

def test_all_endpoints():
    print(f"Fetching OpenAPI schema from {BASE_URL}/openapi.json...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        response.raise_for_status()
        openapi_schema = response.json()
    except Exception as e:
        print(f"Failed to fetch OpenAPI schema: {e}")
        return

    paths = openapi_schema.get("paths", {})
    if not paths:
        print("No paths found in OpenAPI schema.")
        return

    print(f"Found {len(paths)} unique paths.")
    
    # 1. Login to get a token
    print("Attempting to login as admin...")
    token = None
    login_res = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if login_res.status_code == 200:
        res_json = login_res.json()
        token = res_json.get("data", {}).get("tokens", {}).get("access_token")
        if token:
            print("Successfully logged in and acquired token.")
        else:
            print("Logged in, but failed to extract token from response.")
    else:
        print(f"Login failed! Status: {login_res.status_code}, Response: {login_res.text}")
        print("Will proceed without token (expecting 401s).")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    total = 0
    failed = 0
    working = 0
    
    failures = []

    for path, methods in paths.items():
        # Replace path parameters with dummy values
        test_path = re.sub(r"\{.*?\}", "999", path)
        url = f"{BASE_URL}{test_path}"

        for method, operation in methods.items():
            method_upper = method.upper()
            total += 1
            
            try:
                req_method = getattr(requests, method.lower())
                
                # Send empty body. It might result in 422 which means it reached the endpoint correctly.
                res = req_method(url, headers=headers, json={}, timeout=5)
                
                if res.status_code >= 500:
                    status = "FAILED"
                    failed += 1
                    failures.append(f"{method_upper} {path} -> {res.status_code} {res.reason} {res.text}")
                elif res.status_code == 404:
                    if "Not Found" in res.text or "not found" in res.text.lower():
                        status = "WORKING (404 Data Not Found)"
                        working += 1
                    else:
                        status = f"WORKING ({res.status_code})"
                        working += 1
                elif res.status_code == 401:
                    status = f"WORKING (401: {res.text})"
                    working += 1
                else:
                    status = f"WORKING ({res.status_code})"
                    working += 1
                    
                print(f"[{status}] {method_upper} {url}")
                
            except Exception as e:
                print(f"[ERROR] {method_upper} {url} -> {str(e)}")
                failed += 1
                failures.append(f"{method_upper} {path} -> {str(e)}")

    print("\n" + "="*40)
    print("TEST SUMMARY")
    print("="*40)
    print(f"Total Endpoints Tested : {total}")
    print(f"Working / Responding   : {working}")
    print(f"Failed / 500 Errors    : {failed}")
    
    if failures:
        print("\nNOT WORKING (5xx Errors):")
        for f in failures:
            print(f" - {f}")
    else:
        print("\nAll endpoints are responding correctly (no 5xx errors)!")

if __name__ == "__main__":
    test_all_endpoints()
