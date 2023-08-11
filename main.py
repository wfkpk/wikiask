from fastapi import FastAPI
import weaviate

app = FastAPI()

# Connect to the Weaviate demo database
auth_config = weaviate.auth.AuthApiKey(api_key="76320a90-53d8-42bc-b41d-678647c6672e")
client = weaviate.Client(
    url="https://cohere-demo.weaviate.network/",
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": "API KEY",
    }
)

client.is_ready()  # check if True

@app.get("/semantic_search/")
async def semantic_search(query: str, results_lang: str = ""):
    nearText = {"concepts": [query]}
    properties = ["text", "title", "url", "views", "lang", "_additional {distance}"]

    if results_lang:
        where_filter = {
            "path": ["lang"],
            "operator": "Equal",
            "valueString": results_lang
        }
        response = (
            client.query
            .get("Articles", properties)
            .with_where(where_filter)
            .with_near_text(nearText)
            .with_limit(5)
            .do()
        )
    else:
        response = (
            client.query
            .get("Articles", properties)
            .with_near_text(nearText)
            .with_limit(5)
            .do()
        )

    result = response['data']['Get']['Articles']
    # print(result)
    return result

# def print_result(result):
#     for item in result:
#         print(f"\033[95m{item['title']} ({item['views']}) {item['_additional']['distance']}\033[0m")
#         print(f"\033[4m{item['url']}\033[0m")
#         print(item['text'])
        # print()

# @app.get("/search/")
# async def search(query: str, lang: str = ""):
#     query_result = semantic_search(query, lang)
#     return query_result
