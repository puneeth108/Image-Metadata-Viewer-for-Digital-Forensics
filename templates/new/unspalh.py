import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from fractions import Fraction

# Your Unsplash API key
access_key = 'eYzjJXqeLt5pA726eO1oJRTGYVzgruIhWJ8jfjroxRM'

# Prompt the user to enter the Unsplash photo ID
photo_id = input("Enter the Unsplash photo ID: ")

# Unsplash API URL for a specific photo
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
    'exif': photo_details.get('exif', {}),
    'location': photo_details.get('location', {}),
    'unsplash_url': f'https://unsplash.com/photos/{photo_id}'  
}

# Print metadata one by one
for key, value in metadata.items():
    print(f"{key}: {value}")

# Extract exposure time and aperture values from EXIF data
exposure_time = metadata['exif'].get('exposure_time', 'N/A')
aperture_value = metadata['exif'].get('aperture', 'N/A')

# Convert exposure time from fraction to float
if exposure_time != 'N/A':
    try:
        exposure_time = float(Fraction(exposure_time))
    except Exception as e:
        print(f"Error converting exposure time: {e}")
        exposure_time = 'N/A'

# Prepare data for histograms
exposure_times = [exposure_time] if exposure_time != 'N/A' else []
aperture_values = [float(aperture_value)] if aperture_value != 'N/A' else []

# Create a DataFrame for scatter plots and bar graphs
df = pd.DataFrame([metadata])

# Extract the color for Seaborn plotting
dominant_color = metadata['color']

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Scatter Plot: Resolution vs. Likes
df['resolution'] = df['width'] * df['height']
sns.scatterplot(x=df['resolution'], y=df['likes'], ax=axs[0, 0])
axs[0, 0].set_title('Resolution vs. Likes')
axs[0, 0].set_xlabel('Resolution (Width x Height)')
axs[0, 0].set_ylabel('Likes')

# Bar Graph: Dimensions
df[['width', 'height']].plot(kind='bar', ax=axs[0, 1])
axs[0, 1].set_title('Image Dimensions')
axs[0, 1].set_xlabel('Image Index')
axs[0, 1].set_ylabel('Pixels')

# Bar Graph: Likes
df['likes'].plot(kind='bar', color='skyblue', ax=axs[1, 0])
axs[1, 0].set_title('Number of Likes')
axs[1, 0].set_xlabel('Image Index')
axs[1, 0].set_ylabel('Likes')

# Bar Graph: Dominant Color
sns.barplot(x=[0], y=[1], hue=[dominant_color], dodge=False, ax=axs[1, 1], palette=[dominant_color])
axs[1, 1].set_title('Dominant Color')
axs[1, 1].set_xlabel('Image Index')
axs[1, 1].set_ylabel('Color')
axs[1, 1].legend([dominant_color], title='Color')

# Add custom text in the middle of the graph output
# You can adjust the coordinates (x, y) and text as needed
plt.text(0.5, 0.5,     'Custom Text in the Middle', fontsize=14, ha='center', va='center', transform=plt.gcf().transFigure)

plt.tight_layout()
plt.show()
