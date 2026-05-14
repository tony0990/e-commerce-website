import json
import re
from app.main import app

def generate_dummy_value(schema_def, schemas):
    if "$ref" in schema_def:
        ref_name = schema_def["$ref"].split("/")[-1]
        return generate_dummy_value(schemas[ref_name], schemas)
    
    if "anyOf" in schema_def:
        return generate_dummy_value(schema_def["anyOf"][0], schemas)
    
    type_ = schema_def.get("type", "string")
    if type_ == "string":
        format_ = schema_def.get("format")
        if format_ == "email":
            return "admin@ecommerce.com"
        if format_ == "password":
            return "Admin@123456"
        return "test_string"
    elif type_ == "integer":
        return 1
    elif type_ == "number":
        return 1.5
    elif type_ == "boolean":
        return True
    elif type_ == "array":
        items = schema_def.get("items", {})
        return [generate_dummy_value(items, schemas)]
    elif type_ == "object":
        properties = schema_def.get("properties", {})
        dummy_obj = {}
        for k, v in properties.items():
            dummy_obj[k] = generate_dummy_value(v, schemas)
        return dummy_obj
    return "test"

def main():
    schema = app.openapi()
    paths = schema.get("paths", {})
    schemas = schema.get("components", {}).get("schemas", {})
    
    bash_script = []
    bash_script.append("#!/bin/bash")
    bash_script.append("BASE_URL=\"http://localhost:8000\"")
    bash_script.append("ADMIN_EMAIL=\"admin@ecommerce.com\"")
    bash_script.append("ADMIN_PASSWORD=\"Admin@123456\"")
    bash_script.append("")
    bash_script.append("# 1. Login to get token")
    bash_script.append("echo \"Logging in...\"")
    bash_script.append("LOGIN_RESPONSE=$(curl -s -X POST \"$BASE_URL/api/v1/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"'\"$ADMIN_EMAIL\"'\", \"password\": \"'\"$ADMIN_PASSWORD\"'\"}')")
    bash_script.append("TOKEN=$(echo $LOGIN_RESPONSE | grep -o '\"access_token\":\"[^\"]*' | grep -o '[^\"]*$')")
    bash_script.append("echo \"Token: $TOKEN\"")
    bash_script.append("if [ -z \"$TOKEN\" ]; then echo \"Failed to get token\"; TOKEN=\"dummy_token\"; fi")
    bash_script.append("AUTH_HEADER=\"Authorization: Bearer $TOKEN\"")
    bash_script.append("")
    bash_script.append("echo \"Starting tests...\"")
    
    endpoints = []
    for path, methods in paths.items():
        # Replace path parameters with 999 to avoid mutating existing real data like user ID 1
        test_path = re.sub(r"\{.*?\}", "999", path)
        url = f"$BASE_URL{test_path}"
        
        for method, operation in methods.items():
            endpoints.append((method, test_path, url, operation))

    def get_sort_key(ep):
        method, test_path, _, _ = ep
        method_upper = method.upper()
        # Put dangerous/terminal operations at the very end
        if "toggle-status" in test_path:
            return 99
        if method_upper == "DELETE":
            return 5
        if method_upper == "GET":
            return 1
        if method_upper == "POST":
            return 2
        if method_upper == "PUT":
            return 3
        if method_upper == "PATCH":
            return 4
        return 10

    endpoints.sort(key=get_sort_key)

    for method, test_path, url, operation in endpoints:
        method_upper = method.upper()
        curl_cmd = f"echo \"\\n=== Testing {method_upper} {test_path} ===\"\n"
        curl_cmd += f"RESPONSE=$(curl -s -w \"\\nHTTP_STATUS:%{{http_code}}\" -X {method_upper} \"{url}\" \\\n"
        curl_cmd += "  -H \"Content-Type: application/json\" \\\n"
        curl_cmd += "  -H \"$AUTH_HEADER\""
        
        # Request body
        requestBody = operation.get("requestBody", {})
        if requestBody:
            content = requestBody.get("content", {})
            json_content = content.get("application/json", {})
            schema_ref = json_content.get("schema", {})
            if schema_ref:
                dummy_body = generate_dummy_value(schema_ref, schemas)
                # Convert dict to json string and escape single quotes
                body_str = json.dumps(dummy_body).replace("'", "'\\''")
                curl_cmd += f" \\\n  -d '{body_str}'"
        
        curl_cmd += ")\n"
        curl_cmd += "STATUS=$(echo \"$RESPONSE\" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)\n"
        curl_cmd += "BODY=$(echo \"$RESPONSE\" | sed 's/HTTP_STATUS:[0-9]*//g')\n"
        curl_cmd += "echo \"Status: $STATUS\"\n"
        curl_cmd += "echo \"Response: $BODY\"\n"
        curl_cmd += "if [ \"$STATUS\" -ge 500 ]; then\n"
        curl_cmd += f"  echo \"[FAILED] {method_upper} {test_path} returned 5xx error!\" >> failed_endpoints.txt\n"
        curl_cmd += "fi\n"
        
        bash_script.append(curl_cmd)

    bash_script.append("echo \"\\n=== TEST SUMMARY ===\"")
    bash_script.append("if [ -f failed_endpoints.txt ]; then")
    bash_script.append("  echo \"The following endpoints failed with 5xx errors:\"")
    bash_script.append("  cat failed_endpoints.txt")
    bash_script.append("else")
    bash_script.append("  echo \"All endpoints responded without 5xx errors.\"")
    bash_script.append("fi")
    bash_script.append("rm -f failed_endpoints.txt")
    
    with open("test_api.sh", "w") as f:
        f.write("\n".join(bash_script))
    print("test_api.sh created successfully.")

if __name__ == "__main__":
    main()
