import requests
import pandas as pd


# 你的Cloudflare账号信息
api_key = "d9aaca86dc14d87ee47ab94ae744177f8f9a1"
email = "artenis159.tr@gmail.com"

# 設置
headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": api_key,
    "Content-Type": "application/json"
}

# 定義 GraphQL 查詢
query = """
{
  __schema {
    types {
      ...FullType
    }
  }
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
"""

# 请求URL
url = "https://api.cloudflare.com/client/v4/graphql"

# 发送请求
response = requests.post(url, headers=headers, json={"query": query})
data = response.json()

# 確認請求成功
if response.status_code == 200:
    data = response.json()

    all_fields_data = []

    # 收集所有類型的欄位信息
    for type_info in data['data']['__schema']['types']:
        type_name = type_info['name']
        if type_info['fields']:
            for field in type_info['fields']:
                field_name = field['name']
                field_type = field['type']['name'] if field['type']['name'] else field['type']['ofType']['name']
                all_fields_data.append(f"Type: {type_name}, Field: {field_name}, Field Type: {field_type}")

    # 將所有欄位信息寫入TXT文件
    with open("all_table_fields.txt", "w") as file:
        file.write("\n".join(all_fields_data))

    print("All table fields information has been exported to all_table_fields.txt")
else:
    print(f"Query failed with status code {response.status_code} and message: {response.text}")