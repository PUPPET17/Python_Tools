import requests
from PIL import Image,ImageChops
from io import BytesIO
import imagehash
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def resize_images_to_match(img1, img2):
    return img1, img2.resize(img1.size, Image.Resampling.LANCZOS)

def compare_images_with_pixel(img1_url, img2_url):
    img1 = download_image(img1_url)
    img2 = download_image(img2_url)
    img1, img2 = resize_images_to_match(img1, img2)
    return ImageChops.difference(img1, img2).getbbox() is None

def compare_images_with_hash(img1_url, img2_url):
    img1 = download_image(img1_url)
    img2 = download_image(img2_url)
    img1, img2 = resize_images_to_match(img1, img2)
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)
    return hash1 == hash2

def compare_images_with_ssim(img1_url, img2_url):
    img1 = download_image(img1_url).convert('L')  # 转换为灰度图
    img2 = download_image(img2_url).convert('L')
    img1, img2 = resize_images_to_match(img1, img2)
    img1 = np.array(img1)
    img2 = np.array(img2)
    score, _ = ssim(img1, img2, full=True)
    return score == 1.0

def compare_images_with_histogram(img1_url, img2_url):
    img1 = cv2.imdecode(np.asarray(bytearray(requests.get(img1_url).content), dtype="uint8"), cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(np.asarray(bytearray(requests.get(img2_url).content), dtype="uint8"), cv2.IMREAD_COLOR)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    comparison = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return comparison == 1.0

img1_url = "http://117.72.16.190:9000/8083images/1824125592304562176"
img2_url = "http://117.72.16.190:9000/8083images/1824155837325848576"

print("像素级比较:", compare_images_with_pixel(img1_url, img2_url))
print("哈希比较:", compare_images_with_hash(img1_url, img2_url))
print("SSIM 比较:", compare_images_with_ssim(img1_url, img2_url))
print("直方图比较:", compare_images_with_histogram(img1_url, img2_url))
