import requests
import json
from datetime import datetime, timedelta

# 你的Cloudflare账号信息
api_key = "d9aaca86dc14d87ee47ab94ae744177f8f9a1"
email = "artenis159.tr@gmail.com"

# 設置
headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": api_key,
    "Content-Type": "application/json"
}

# 获取所有Zone的ID
def get_zone_ids():
    url = "https://api.cloudflare.com/client/v4/zones"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data["success"]:
        zones = data["result"]
        zone_ids = [(zone["id"], zone["name"]) for zone in zones]
        return zone_ids
    else:
        print("Failed to retrieve zones:", data["errors"])
        return []


# 使用GraphQL API查询每个Zone的总请求数
def get_total_requests(zone_id, zone_name):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=2)
    end_time = end_time.isoformat() + "Z"
    start_time = start_time.isoformat() + "Z"

    query = """
    query {
      viewer {
        zones(filter: {zoneTag: "%s"}) {
          httpRequests1hGroups(limit: 1, filter: {datetime_geq: "%s", datetime_leq: "%s"}) {
            sum {
              requests
            }
          }
        }
      }
    }
    """ % (zone_id, start_time, end_time)

    url = "https://api.cloudflare.com/client/v4/graphql"
    response = requests.post(url, headers=headers, json={'query': query})
    data = response.json()

    if response.status_code == 200:
        if data.get("errors") is None:
            try:
                total_requests = data["data"]["viewer"]["zones"][0]["httpRequests1hGroups"][0]["sum"]["requests"]
                print(
                    f"Zone Name: {zone_name}, Zone ID: {zone_id} - Total Requests in the last 2 hours: {total_requests}")
            except (IndexError, KeyError, TypeError) as e:
                print(f"Failed to parse data for Zone ID {zone_id}: {e}")
                print(json.dumps(data, indent=2))
        else:
            print(f"GraphQL query errors for Zone ID {zone_id}: {data['errors']}")
    else:
        print(f"HTTP error {response.status_code} for Zone ID {zone_id}: {response.text}")


# 主程序
zone_ids = get_zone_ids()
for zone_id, zone_name in zone_ids:
    get_total_requests(zone_id, zone_name)