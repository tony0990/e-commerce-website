#!/bin/bash
BASE_URL="http://localhost:8000"
ADMIN_EMAIL="admin@ecommerce.com"
ADMIN_PASSWORD="Admin@123456"

# 1. Login to get token
echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" -H "Content-Type: application/json" -d '{"email": "'"$ADMIN_EMAIL"'", "password": "'"$ADMIN_PASSWORD"'"}')
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | grep -o '[^"]*$')
echo "Token: $TOKEN"
if [ -z "$TOKEN" ]; then echo "Failed to get token"; TOKEN="dummy_token"; fi
AUTH_HEADER="Authorization: Bearer $TOKEN"

echo "Starting tests..."
echo "\n=== Testing GET /api/v1/auth/me ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/auth/me" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/auth/me returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/users/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/users/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/users/count ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/users/count" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/users/count returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/users/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/users/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/users/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/users/me/profile ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/users/me/profile" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/users/me/profile returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/products/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/products/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/products/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/products/categories ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/products/categories" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/products/categories returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/products/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/products/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/products/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/orders/me ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/orders/me" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/orders/me returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/orders/all ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/orders/all" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/orders/all returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/orders/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/orders/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/orders/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/orders/999/track ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/orders/999/track" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/orders/999/track returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/wishlist/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/wishlist/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/wishlist/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/dashboard/stats ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/stats" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/dashboard/stats returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/dashboard/metrics ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/metrics" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/dashboard/metrics returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/dashboard/health/extended ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/health/extended" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/dashboard/health/extended returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/dashboard/logs ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/logs" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/dashboard/logs returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/dashboard/logs/stats ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/logs/stats" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/dashboard/logs/stats returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /api/v1/cart/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/api/v1/cart/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /api/v1/cart/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET / ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET / returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing GET /health ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X GET "$BASE_URL/health" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] GET /health returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/auth/register ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"email": "admin@ecommerce.com", "password": "test_string", "confirm_password": "test_string", "first_name": "test_string", "last_name": "test_string", "phone": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/auth/register returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/auth/login ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"email": "admin@ecommerce.com", "password": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/auth/login returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/auth/refresh ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"refresh_token": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/auth/refresh returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/auth/change-password ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/auth/change-password" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"current_password": "test_string", "new_password": "test_string", "confirm_new_password": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/auth/change-password returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/users/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"email": "admin@ecommerce.com", "first_name": "test_string", "last_name": "test_string", "phone": "test_string", "password": "test_string", "role": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/users/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/products/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/products/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"name": "test_string", "description": "test_string", "price": 1.5, "original_price": 1.5, "stock": 1, "image_url": "test_string", "is_active": true, "is_offer": true, "offer_price": 1.5, "is_sold_out": true, "category_id": 1}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/products/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/products/categories ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/products/categories" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"name": "test_string", "description": "test_string", "image_url": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/products/categories returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/orders ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/orders" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"shipping_address": "test_string", "shipping_city": "test_string", "shipping_state": "test_string", "shipping_zip": "test_string", "shipping_country": "test_string", "payment_method": "test_string", "notes": "test_string", "items": [{"product_id": 1, "quantity": 1}]}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/orders returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/wishlist/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/wishlist/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"product_id": 1}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/wishlist/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/cart/items ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/cart/items" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"product_id": 1, "quantity": 1}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/cart/items returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing POST /api/v1/cart/sync ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$BASE_URL/api/v1/cart/sync" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"items": [{"product_id": 1, "quantity": 1}]}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] POST /api/v1/cart/sync returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PUT /api/v1/users/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "$BASE_URL/api/v1/users/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"first_name": "test_string", "last_name": "test_string", "phone": "test_string", "address": "test_string", "city": "test_string", "state": "test_string", "zip_code": "test_string", "country": "test_string", "avatar_url": "test_string", "email": "admin@ecommerce.com", "role": "test_string", "is_active": true}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PUT /api/v1/users/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PUT /api/v1/users/me/profile ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "$BASE_URL/api/v1/users/me/profile" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"first_name": "test_string", "last_name": "test_string", "phone": "test_string", "address": "test_string", "city": "test_string", "state": "test_string", "zip_code": "test_string", "country": "test_string", "avatar_url": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PUT /api/v1/users/me/profile returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PUT /api/v1/products/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "$BASE_URL/api/v1/products/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"name": "test_string", "description": "test_string", "price": 1.5, "original_price": 1.5, "stock": 1, "image_url": "test_string", "is_active": true, "is_offer": true, "offer_price": 1.5, "is_sold_out": true, "category_id": 1}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PUT /api/v1/products/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PUT /api/v1/cart/items/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "$BASE_URL/api/v1/cart/items/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"quantity": 1}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PUT /api/v1/cart/items/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PATCH /api/v1/orders/999/status ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PATCH "$BASE_URL/api/v1/orders/999/status" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d '{"status": "test_string"}')
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PATCH /api/v1/orders/999/status returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing DELETE /api/v1/users/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$BASE_URL/api/v1/users/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] DELETE /api/v1/users/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing DELETE /api/v1/products/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$BASE_URL/api/v1/products/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] DELETE /api/v1/products/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing DELETE /api/v1/wishlist/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$BASE_URL/api/v1/wishlist/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] DELETE /api/v1/wishlist/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing DELETE /api/v1/cart/ ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$BASE_URL/api/v1/cart/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] DELETE /api/v1/cart/ returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing DELETE /api/v1/cart/items/999 ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE "$BASE_URL/api/v1/cart/items/999" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] DELETE /api/v1/cart/items/999 returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== Testing PATCH /api/v1/users/999/toggle-status ==="
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PATCH "$BASE_URL/api/v1/users/999/toggle-status" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER")
STATUS=$(echo "$RESPONSE" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*//g')
echo "Status: $STATUS"
echo "Response: $BODY"
if [ "$STATUS" -ge 500 ]; then
  echo "[FAILED] PATCH /api/v1/users/999/toggle-status returned 5xx error!" >> failed_endpoints.txt
fi

echo "\n=== TEST SUMMARY ==="
if [ -f failed_endpoints.txt ]; then
  echo "The following endpoints failed with 5xx errors:"
  cat failed_endpoints.txt
else
  echo "All endpoints responded without 5xx errors."
fi
rm -f failed_endpoints.txt