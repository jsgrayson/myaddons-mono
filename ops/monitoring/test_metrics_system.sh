#!/bin/bash
set -e

BACKEND_METRICS_URL="http://localhost:8001/status/metrics"
BACKEND_PUSH_URL="http://localhost:8001/status/metrics/push"
PROMETHEUS_URL="http://localhost:9090/api/v1/query"

echo "======================================================"
echo "            Goblin Metrics System Test Tool           "
echo "======================================================"

# --------------------------------------------------------
# 1. Test BACKEND METRICS ENDPOINT
# --------------------------------------------------------
echo "➡ Testing backend metrics endpoint..."
if curl -s --fail ${BACKEND_METRICS_URL} >/dev/null; then
    echo "✔ Backend /status/metrics endpoint is responding"
else
    echo "❌ Backend /status/metrics endpoint is NOT responding"
    exit 1
fi

# --------------------------------------------------------
# 2. Push test metrics from a dummy agent
# --------------------------------------------------------
echo "➡ Pushing test metrics (dummy agent)..."

curl -s -X POST ${BACKEND_PUSH_URL} \
    -H "Content-Type: application/json" \
    -d '{"agent":"dummy","metric":"heartbeat","type":"heartbeat"}' >/dev/null

curl -s -X POST ${BACKEND_PUSH_URL} \
    -H "Content-Type: application/json" \
    -d '{"agent":"dummy","metric":"jobs_completed","type":"counter","value":3}' >/dev/null

curl -s -X POST ${BACKEND_PUSH_URL} \
    -H "Content-Type: application/json" \
    -d '{"agent":"dummy","metric":"latency_ms","type":"gauge","value":42}' >/dev/null

echo "✔ Dummy metrics pushed successfully"

# --------------------------------------------------------
# 3. Confirm backend exported those metrics
# --------------------------------------------------------
echo "➡ Validating metrics appear in /status/metrics..."

RESULT=$(curl -s ${BACKEND_METRICS_URL} | grep goblin_dummy_jobs_completed || true)

if [ -z "$RESULT" ]; then
    echo "❌ Test metrics did NOT appear in backend registry!"
    exit 1
fi

echo "✔ Backend registry contains custom metrics"

# --------------------------------------------------------
# 4. Test Prometheus scrape (if running)
# --------------------------------------------------------
echo "➡ Testing Prometheus scrape (optional)..."

QUERY_RESULT=$(curl -s "${PROMETHEUS_URL}?query=goblin_dummy_jobs_completed" | grep "success" || true)

if [ -z "$QUERY_RESULT" ]; then
    echo "⚠ Prometheus not running or not scraping yet."
    echo "   (This is safe to ignore if monitoring stack not started)"
else
    echo "✔ Prometheus can query Goblin metrics"
fi

echo "======================================================"
echo "   🎉 Goblin Metrics System Operational & Verified!   "
echo "======================================================"
