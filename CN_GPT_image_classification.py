import os
import shutil
import requests
import base64

# Created: 11/14/2023

def encode_image(image_path):
    """
    将图像编码为base64字符串。
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def classify_image(image_path, feature, api_key):
    """
    使用OpenAI的GPT-4 Vision API根据指定特征对图像进行分类。

    :param image_path: 图像文件的路径。
    :param feature: 要按照该特征对图像进行分类。
    :param api_key: 你的OpenAI API密钥。
    :return: 分类结果，字符串形式。
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

        # 确保返回的分类结果是有效的目录名
        if classification.startswith("Error:"):
            return None
        else:
            return classification
    else:
        return None


def get_folder_path():
    return input("请输入图片所在的文件夹路径：")

def get_classification_feature():
    return input("请输入您希望分类的图像特征（例如：'区分单色图和彩色图'）：")

def move_files(src_folder, dest_folder, files):
    os.makedirs(dest_folder, exist_ok=True)
    for file in files:
        shutil.move(os.path.join(src_folder, file), os.path.join(dest_folder, file))

def classify_images_in_folder(folder_path, feature, api_key):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            classification = classify_image(os.path.join(folder_path, file_name), feature, api_key)

            # 仅当分类成功时移动文件
            if classification:
                move_files(folder_path, os.path.join(folder_path, classification), [file_name])
            else:
                print(f"分类失败: {file_name}")

def main():
    api_key = "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"  # 将此替换为你的OpenAI API密钥
    folder_path = get_folder_path()
    feature = get_classification_feature(),'Please simplify your classification into one word.'
    classify_images_in_folder(folder_path, feature, api_key)

if __name__ == "__main__":
    main()
