from notion_client import Client
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

# 初始化Notion客户端
notion = Client(auth=os.environ.get("NOTION_INTEGRATION_TOKEN"))

# 指定数据库ID
database_id = os.getenv("NOTION_DATABASE_ID")


# 获取数据库中的数据
def get_database_entries():
    results = notion.databases.query(database_id=database_id).get("results")
    return results


# 更新数据库条目
def update_notion_database_entry(page_id, properties):
    notion.pages.update(page_id=page_id, properties=properties)


# 主函数
def main():

    response = requests.get("https://api.exchangerate-api.com/v4/latest/CNY")
    exchangerate_json = response.json()
    print(exchangerate_json)

    # 获取数据
    entries = get_database_entries()

    # 处理和更新数据
    for entry in entries:
        page_id = entry["id"]
        current_properties = entry["properties"]

        curr_type = current_properties["币种"]["title"][0]["plain_text"]
        if curr_type in exchangerate_json["rates"]:
            curr_value = exchangerate_json["rates"][curr_type]
            price = round(1 / curr_value, 2)

            # 这里可以添加您的逻辑来决定如何更新数据
            # 例如，我们可以更新一个名为"Status"的属性
            updated_properties = {"汇率": {"number": price}}

            # 更新数据
            update_notion_database_entry(page_id, updated_properties)
            print(
                f"Updated entry: {page_id}, CNY:{curr_type}=1:{price}, {updated_properties}"
            )


if __name__ == "__main__":
    main()
