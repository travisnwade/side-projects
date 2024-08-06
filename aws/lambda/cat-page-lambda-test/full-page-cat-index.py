import os
import json
import requests
from github import Github

# Environment variables
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_FILE_PATH = os.getenv('GITHUB_FILE_PATH')

def get_random_cat_image():
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q=cat&image_type=photo&per_page=100"
    response = requests.get(url)
    data = response.json()
    if data['totalHits'] > 0:
        images = data['hits']
        random_image = random.choice(images)
        return random_image['largeImageURL']
    else:
        raise Exception("Failed to fetch image from Pixabay")

def generate_html(image_url):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Random Cat Image</title>
        <style>
            body, html {{
                height: 100%;
                margin: 0;
            }}
            .bg {{
                background-image: url("{image_url}");
                height: 100%;
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }}
        </style>
    </head>
    <body>
        <div class="bg"></div>
    </body>
    </html>
    """
    return html_content

def upload_to_github(html_content):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    try:
        contents = repo.get_contents(GITHUB_FILE_PATH)
        repo.update_file(contents.path, "Updating random cat image", html_content, contents.sha)
    except Exception as e:
        repo.create_file(GITHUB_FILE_PATH, "Adding random cat image", html_content)

def lambda_handler(event, context):
    try:
        image_url = get_random_cat_image()
        html_content = generate_html(image_url)
        upload_to_github(html_content)
        return {
            'statusCode': 200,
            'body': 'Successfully updated GitHub with random cat image.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
