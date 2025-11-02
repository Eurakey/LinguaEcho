#!/bin/bash
# Phase 2 Authentication & Database Test Script

echo "=========================================="
echo "Phase 2 功能测试脚本"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
TOTAL_TESTS=0
PASSED_TESTS=0

test_endpoint() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    local name=$1
    local command=$2

    echo -n "测试 $name ... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ 失败${NC}"
    fi
}

echo "1. 测试基础端点"
echo "----------------------------------------"
test_endpoint "Health Check" "curl -sf $BASE_URL/health | grep -q 'healthy'"
test_endpoint "Root Endpoint" "curl -sf $BASE_URL/ | grep -q 'Welcome to LinguaEcho'"
test_endpoint "API Docs" "curl -sf $BASE_URL/docs | grep -q 'swagger'"
echo ""

echo "2. 测试用户注册"
echo "----------------------------------------"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="test123456"

echo "注册邮箱: $TEST_EMAIL"
REGISTER_RESPONSE=$(curl -sf -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\"}")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✓ 用户注册成功${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "  Token: ${ACCESS_TOKEN:0:20}..."
else
    echo -e "${RED}✗ 用户注册失败${NC}"
    echo "  响应: $REGISTER_RESPONSE"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "3. 测试用户登录"
echo "----------------------------------------"
LOGIN_RESPONSE=$(curl -sf -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$TEST_EMAIL\", \"password\": \"$TEST_PASSWORD\"}")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✓ 用户登录成功${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
else
    echo -e "${RED}✗ 用户登录失败${NC}"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "4. 测试获取当前用户信息"
echo "----------------------------------------"
USER_RESPONSE=$(curl -sf -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$USER_RESPONSE" | grep -q "$TEST_EMAIL"; then
    echo -e "${GREEN}✓ 获取用户信息成功${NC}"
    echo "  Email: $TEST_EMAIL"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ 获取用户信息失败${NC}"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "5. 测试访客模式对话（无认证）"
echo "----------------------------------------"
SESSION_ID=$(uuidgen)
CHAT_RESPONSE=$(curl -sf -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"language\": \"japanese\",
    \"scenario\": \"restaurant\",
    \"message\": \"こんにちは\",
    \"history\": []
  }")

if echo "$CHAT_RESPONSE" | grep -q "reply"; then
    echo -e "${GREEN}✓ 访客模式对话成功${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ 访客模式对话失败${NC}"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "6. 测试认证模式对话（自动保存到数据库）"
echo "----------------------------------------"
AUTH_SESSION_ID=$(uuidgen)
AUTH_CHAT_RESPONSE=$(curl -sf -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"session_id\": \"$AUTH_SESSION_ID\",
    \"language\": \"english\",
    \"scenario\": \"casual_chat\",
    \"message\": \"Hello!\",
    \"history\": []
  }")

if echo "$AUTH_CHAT_RESPONSE" | grep -q "reply"; then
    echo -e "${GREEN}✓ 认证模式对话成功${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ 认证模式对话失败${NC}"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "7. 测试获取用户对话历史"
echo "----------------------------------------"
CONVERSATIONS_RESPONSE=$(curl -sf -X GET "$BASE_URL/api/conversations" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$CONVERSATIONS_RESPONSE" | grep -q "session_id"; then
    echo -e "${GREEN}✓ 获取对话历史成功${NC}"
    COUNT=$(echo "$CONVERSATIONS_RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
    echo "  找到 $COUNT 个对话"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ 获取对话历史失败${NC}"
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo ""

echo "8. 验证数据库表"
echo "----------------------------------------"
echo "数据库表结构:"
psql linguaecho -c "\dt" 2>/dev/null || echo "  无法连接到数据库"
echo ""
echo "用户数据:"
psql linguaecho -c "SELECT email, created_at FROM users ORDER BY created_at DESC LIMIT 3;" 2>/dev/null || echo "  无法查询用户表"
echo ""

echo "=========================================="
echo "测试总结"
echo "=========================================="
echo -e "总测试数: $TOTAL_TESTS"
echo -e "通过: ${GREEN}$PASSED_TESTS${NC}"
echo -e "失败: ${RED}$((TOTAL_TESTS - PASSED_TESTS))${NC}"
echo ""

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}🎉 所有测试通过！${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  部分测试失败${NC}"
    exit 1
fi
