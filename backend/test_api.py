import urllib.request, json

# Login
login_req = urllib.request.Request(
    'http://localhost:8000/api/v1/auth/login',
    data=json.dumps({'email':'admin@retailpulse.com','password':'admin123'}).encode(),
    headers={'Content-Type':'application/json'}
)
token = json.loads(urllib.request.urlopen(login_req).read())['access_token']

# Test Dashboard KPIs
kpi_req = urllib.request.Request(
    'http://localhost:8000/api/v1/dashboard/kpis',
    headers={'Authorization': f'Bearer {token}'}
)
kpis = json.loads(urllib.request.urlopen(kpi_req).read())
print("DASHBOARD KPIs:")
print(f"  Revenue: {kpis['total_revenue']:,.2f}")
print(f"  Orders: {kpis['total_orders']:,}")
print(f"  Customers: {kpis['total_customers']:,}")
print(f"  AOV: {kpis['avg_order_value']:,.2f}")
