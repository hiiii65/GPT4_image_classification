import os
import shutil
import requests
import base64

# Created: 11/14/2023

def encode_image(image_path):
    """
    Encode the image as a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def classify_image(image_path, feature, api_key):
    """
    Classify an image using OpenAI's GPT-4 Vision API based on a specified feature.

    :param image_path: Path to the image file.
    :param feature: The feature to classify the image by.
    :param api_key: Your OpenAI API key.
    :return: The classification result as a string.
    """
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Classify this image based on the following feature: {feature}."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        classification = response_data["choices"][0]["message"]["content"]

        # Ensure the returned classification result is a valid directory name
        if classification.startswith("Error:"):
            return None
        else:
            return classification
    else:
        return None

def get_folder_path():
    return input("Please enter the path of the folder containing the images: ")

def get_classification_feature():
    return input("Please enter the image feature you wish to classify (e.g., 'Distinguish between monochrome and color images'): ")

def move_files(src_folder, dest_folder, files):
    os.makedirs(dest_folder, exist_ok=True)
    for file in files:
        shutil.move(os.path.join(src_folder, file), os.path.join(dest_folder, file))

def classify_images_in_folder(folder_path, feature, api_key):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            classification = classify_image(os.path.join(folder_path, file_name), feature, api_key)

            # Move files only if classification is successful
            if classification:
                move_files(folder_path, os.path.join(folder_path, classification), [file_name])
            else:
                print(f"Classification failed: {file_name}")

def main():
    api_key = "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"  # Replace this with your OpenAI API key
    folder_path = get_folder_path()
    feature = get_classification_feature()
    classify_images_in_folder(folder_path, feature, api_key)

if __name__ == "__main__":
    main()
