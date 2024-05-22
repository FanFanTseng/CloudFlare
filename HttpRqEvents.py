import requests
import json
from datetime import datetime, timedelta


# 你的Cloudflare账号信息

api_token = "DfBe95Uv9XIKEhy1kyprR39t7JllJTuxiRafdQSu"
zone_id = "05942fb4aaa61b4a50247dd9d07f83f8"

# 設置
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}

# 获取当前时间和五分钟前的时间，并格式化为ISO 8601字符串
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=60)
end_time_str = end_time.isoformat() + "Z"
start_time_str = start_time.isoformat() + "Z"

# GraphQL查询和变量
query = """
query LisRrqEvents($zoneTag: String!, $filter: ZoneHttpRequestsAdaptiveFilter_InputObject!) {
  viewer {
    zones(filter: { zoneTag: $zoneTag }) {
      httpRequests1hGroups(
        filter: $filter
        limit: 10
        orderBy: [datetime_DESC]
      ) {
        clientAsn
        clientCountryName
        clientIP
        datetime
        userAgent
      }
    }
  }
}
"""

variables = {
    "zoneTag": zone_id,
    "filter": {
        "datetime_geq": start_time_str,
        "datetime_leq": end_time_str
    }
}


# 请求URL
url = "https://api.cloudflare.com/client/v4/graphql"

# 发送请求
response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
data = response.json()

# 检查请求状态
if response.status_code == 200:
    if data.get("errors") is None:
        try:
            events = data["data"]["viewer"]["zones"][0]["firewallEventsAdaptive"]
            for event in events:
                print(f"Client ASN: {event['clientAsn']}")
                print(f"Client Country: {event['clientCountryName']}")
                print(f"Client IP: {event['clientIP']}")
                print(f"Datetime: {event['datetime']}")
                print(f"User Agent: {event['userAgent']}")
                print("\n")
        except (IndexError, KeyError, TypeError) as e:
            print(f"Failed to parse data for Zone ID {zone_id}: {e}")
            print(json.dumps(data, indent=2))
    else:
        print(f"GraphQL query errors for Zone ID {zone_id}: {data['errors']}")
else:
    print(f"HTTP error {response.status_code} for Zone ID {zone_id}: {response.text}")