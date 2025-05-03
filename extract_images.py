import docker
import json
from datetime import datetime

def get_image_data():
    client = docker.from_env()
    images = client.images.list()

    image_data_list = []
    for image in images:
        tags = image.tags if image.tags else ["<none>:<none>"]
        for tag in tags:
            image_info = {
                "id": image.id,
                "tag": tag,
                "short_id": image.short_id,
                "created": datetime.fromisoformat(image.attrs['Created'].replace("Z", "")),
                "size_bytes": image.attrs['Size'],
                "virtual_size_bytes": image.attrs.get('VirtualSize', image.attrs['Size']),
                "labels": image.labels
            }
            image_data_list.append(image_info)

    return image_data_list

def save_to_json(data, filename='docker_images.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, default=str)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    data = get_image_data()
    save_to_json(data)
