import requests
from neword_image_url_data import get_image_url, image_ids


folder = 'neword_images'

for image_id in image_ids:
    filename, url = get_image_url(image_id)
    path = folder + '/' + filename

    with open(path, 'wb') as f:
        try:
            req = requests.get(url)
            image = req.content
            f.write(image)
        except Exception:
            print(url)
