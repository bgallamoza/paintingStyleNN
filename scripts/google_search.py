'''
@File   :   google_search.py
@Author :   Brennan Gallamoza
@Desc   :   Script for making search queries to google images and converting images to a 3D pixel array
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import requests as re
import io
from PIL import Image
import time
import numpy as np
import pandas as pd
import gzip, pickletools, pickle
import os

def generate_url(search_params: dict) -> str:
    """Takes dict of search parameters and returns a url"""

    url = "https://www.google.com/search?"
    for param, val in search_params.items():
        url += (param + "=" + val + "&")
    if url[-1] == "&": url = url[:-1]
    return url

def get_image_urls(wd: webdriver, delay: int, max_images: int, search_params: dict) -> set:
    """Returns a list of urls to images based on a Google search URL provided"""

    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = generate_url(search_params)
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        # gets list of thumbnails to click, defined by the html class "Q4LuWd"
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips : max_images]:

            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            
            try:
                # source image url identified by the html class "n3VNCb"
                images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                for image in images:
                    if len(image_urls) + skips >= max_images:
                        break

                    if image.get_attribute('src') in image_urls:
                        print("dupe")
                        max_images += 1
                        skips += 1
                        break
                    
                    # url contained in the 'src' attribute
                    if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                            image_urls.add(image.get_attribute('src'))
                            print(f"Found {len(image_urls)}")
            except Exception as e:
                print("Error:  ", e)
                continue

    return list(image_urls)

def url_to_img(url: str) -> Image:
    """Converts a url to an picture into an Image object"""
    try:
        content = re.get(url).content
        img = Image.open(io.BytesIO(content))
    except Exception as e:
        print("url_to_img() failed: ", e)
        img = None
    return img

def img_to_array(img: Image) -> np.array:
    """Converts an Image object into a 3D numpy array (pixel height * pixel width * pixel RGB)"""
    if img is None: return None
    else: return np.asarray(img)

def get_pixel_arrays(path: str) -> pd.DataFrame:
    df = pd.DataFrame(columns=['data', 'label'])

    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            try:
                for i, c in enumerate(filename):
                    if c.isdigit():
                        filename = filename[:i]
                        break
                img = Image.open(f)
                arr = img_to_array(img)
                df2 = pd.Series([arr, filename], index=df.columns)
                df = df.append(df2, ignore_index=True)
            except Exception as e:
                print("Error: ", f, e)

    return df

def download_img(path: str, img: Image):
    try:
        with open(path, "wb") as f:
            img.save(f, "JPEG")

        print(f"Image saved at {path}")
    except Exception as e:
        print(f"Download failed: ", e)

def get_images(wd: webdriver, delay: int, max_images: int, queries: list, path: str):
    for q in queries:
        search_params = {"q":q,"tbm":"isch"}
        url_list = get_image_urls(wd, delay, max_images, search_params)
        q = q.replace(" ", "_")
        for count, url in enumerate(url_list):
            img = url_to_img(url)
            download_img(path + q + str(count) + ".jpg", img)

def pickle_df(df: pd.DataFrame, path: str):
    # The output of a regular pickle.dump for our random forest is quite large,
    # we can compress it using gzip
    with gzip.open(path, "wb") as f:
        pickled = pickle.dumps(df)
        optimized_pickle = pickletools.optimize(pickled)
        f.write(optimized_pickle)
        f.close()
    print(f">>> DataFrame successfully saved to \"{path}\" directory. <<<")

if __name__ == "__main__":
    make_dataset = True

    if make_dataset:
        df = get_pixel_arrays(".\\data\\imgs")
        pickle_df(df, "./data/raw_img_arrays.pickle")
    else:
        PATH = ".\\scripts\\drivers\\chromedriver.exe"
        # op = webdriver.ChromeOptions()
        # op.add_argument("--headless")
        # op.add_argument("--disable-gpu")
        wd = webdriver.Chrome(
            PATH,
            # chrome_options=op
            )
        delay = 1
        max_images = 100
        search_params = {}
        queries = [
            "Impressionism Painting",
            "Romanticism Painting",
            "Expressionism Painting",
            "Post Impressionism Painting",
            "Surrealism Painting",
            "Baroque Painting",
            "Symbolism Painting",
            "Neoclassicism Painting",
            "Rococo Painting",
            "Cubism Painting",
            "Northern Renaissance Painting"
        ]
        get_images(wd, delay, max_images, queries, "./data/imgs/")
        wd.quit()