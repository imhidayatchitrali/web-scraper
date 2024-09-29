# # # from fastapi import FastAPI, Request
# # # import requests
# # # from bs4 import BeautifulSoup

# # # app = FastAPI()

# # # def get_page_title(url: str) -> str:
# # #     try:
# # #         response = requests.get(url)
# # #         if response.status_code == 200:
# # #             soup = BeautifulSoup(response.text, 'html.parser')
# # #             title = soup.title.string if soup.title else 'No title found'
# # #             return title
# # #         else:
# # #             return f"Failed to retrieve page. Status code: {response.status_code}"
# # #     except Exception as e:
# # #         return f"An error occurred: {str(e)}"

# # # # Example route
# # # @app.get("/")
# # # def read_root():
# # #     return {"message": "Hello World"}

# # # @app.post("/get-title")
# # # async def fetch_title(request: Request):
# # #     data = await request.json()
# # #     url = data.get('url')
# # #     if url:
# # #         title = get_page_title(url)
# # #         return {"title": title}
# # #     return {"error": "URL not provided"}

# # # # To run the server, use the command: uvicorn app:app --reload


# # from fastapi import FastAPI, Request
# # import requests
# # from bs4 import BeautifulSoup
# # import re
# # import json

# # app = FastAPI()

# # def get_product_v2_json(url: str) -> dict:
# #     try:
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             soup = BeautifulSoup(response.text, 'html.parser')
# #             # Find all script tags
# #             script_tags = soup.find_all('script')

# #             # Search for the ProductV2Json object within script tags
# #             for script in script_tags:
# #                 if script.string:
# #                     # Use regex to find the ProductV2Json object
# #                     match = re.search(r'productV2JsonData\s*=\s*(\{.*?\});', script.string, re.DOTALL)
# #                     if match:
# #                         # Parse the JSON object
# #                         product_data = json.loads(match.group(1))
# #                         return product_data
# #             return {"error": "ProductV2Json not found"}
# #         else:
# #             return {"error": f"Failed to retrieve page. Status code: {response.status_code}"}
# #     except Exception as e:
# #         return {"error": f"An error occurred: {str(e)}"}


# # def get_page_title(url: str) -> str:
# #     try:
# #         response = requests.get(url)
# #         if response.status_code == 200:
# #             soup = BeautifulSoup(response.text, 'html.parser')
# #             title = soup.title.string if soup.title else 'No title found'
# #             return title
# #         else:
# #             return f"Failed to retrieve page. Status code: {response.status_code}"
# #     except Exception as e:
# #         return f"An error occurred: {str(e)}"
    
# # @app.get("/")
# # def read_root():
# #     return {"message": "Hello World"}

# # @app.post("/get-title")
# # async def fetch_title(request: Request):
# #     data = await request.json()
# #     url = data.get('url')
# #     if url:
# #         title = get_page_title(url)
# #         return {"title": title}
# #     return {"error": "URL not provided"}


# # @app.post("/get-product-v2")
# # async def fetch_product_v2(request: Request):
# #     data = await request.json()
# #     url = data.get('url')
# #     if url:
# #         product_data = get_product_v2_json(url)
# #         return product_data
# #     return {"error": "URL not provided"}


# from fastapi import FastAPI, Request
# import requests
# from bs4 import BeautifulSoup

# app = FastAPI()

# def get_page_title(url: str) -> str:
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             title = soup.title.string if soup.title else 'No title found'
#             return title
#         else:
#             return f"Failed to retrieve page. Status code: {response.status_code}"
#     except requests.exceptions.RequestException as e:
#         return f"Request error: {str(e)}"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"


# @app.post("/get-title")
# async def fetch_title(request: Request):
#     data = await request.json()
#     url = data.get('url')
#     if url:
#         title = get_page_title(url)
#         return {"title": title}
#     return {"error": "URL not provided"}


#     # @app.post("/get-product-v2")
# # async def fetch_product_v2(request: Request):
# #     data = await request.json()
# #     url = data.get('url')
# #     if url:
# #         product_data = get_product_v2_json(url)
# #         return product_data
# #     return {"error": "URL not provided"}




from fastapi import FastAPI, Request
import requests
from bs4 import BeautifulSoup
import json
import re

app = FastAPI()

def clean_html(html: str) -> str:
    # Use BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=" ", strip=True)

def get_product_v2_json(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all script tags
            script_tags = soup.find_all('script')

            # Search for the ProductV2Json object within script tags
            for script in script_tags:
                if script.string:
                    # Use regex to find the ProductV2Json object
                    match = re.search(r'productV2JsonData\s*=\s*(\{.*?\});', script.string, re.DOTALL)
                    if match:
                        # Parse the JSON object
                        cleaned_data ={}
                        product_data = json.loads(match.group(1))
                        short_description = product_data.get('description', {}).get('shortDescription', '')
                        cleaned_data['shortDescription'] = clean_html(short_description)

                        long_description = product_data.get('description', {}).get('longDescription', '')
                        cleaned_data['longDescription'] = clean_html(long_description)
                    
                        return product_data, cleaned_data
            return {"error": "ProductV2Json not found"}
        else:
            return {"error": f"Failed to retrieve page. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.post("/get-product-v2")
async def fetch_product_v2(request: Request):
    data = await request.json()
    url = data.get('url')
    if url:
        product_data = get_product_v2_json(url)
        return product_data
    return {"error": "URL not provided"}

@app.post("/get-title")
async def fetch_title(request: Request):
    data = await request.json()
    url = data.get('url')
    if url:
        title = get_page_title(url)
        return {"title": title}
    return {"error": "URL not provided"}

def get_page_title(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else 'No title found'
            return title
        else:
            return f"Failed to retrieve page. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
