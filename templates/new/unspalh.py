import requests

# Your Unsplash API keys
access_key = 'eYzjJXqeLt5pA726eO1oJRTGYVzgruIhWJ8jfjroxRM'

# Unsplash API URL for a specific photo
photo_id = '30575eMzgr8'  # Replace with the Unsplash photo ID
url = f'https://api.unsplash.com/photos/{photo_id}?client_id={access_key}'
response = requests.get(url)
photo_details = response.json()

# Extracting metadata and Unsplash URL only
metadata = {
    'id': photo_details['id'],
    'created_at': photo_details['created_at'],
    'width': photo_details['width'],
    'height': photo_details['height'],
    'color': photo_details['color'],
    'likes': photo_details['likes'],
    'user': photo_details['user']['name'],
    'exif': photo_details['exif'],
    'location': photo_details['location'],
    'unsplash_url': f'https://unsplash.com/photos/{photo_id}'  
}

print(metadata)
