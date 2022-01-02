'''
@File   :   google_search.py
@Author :   Brennan Gallamoza
@Desc   :   Script for making search queries to google images and converting images to a 3D pixel array
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests as re
import io
from PIL import Image
import time
import numpy as np
import pandas as pd
import gzip, pickletools, pickle

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

            # source image url identified by the html class "n3VNCb"
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if len(image_urls) + skips >= max_images:
                    break

                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                
                # url contained in the 'src' attribute
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

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

def get_pixel_arrays(wd: webdriver, delay: int, max_images: int, queries: list) -> pd.DataFrame:
    df = pd.DataFrame(columns=['data', 'label'])

    for q in queries:
        search_params = {"q":q,"tbm":"isch"}
        url_list = get_image_urls(wd, delay, max_images, search_params)
        for url in url_list:
            img = url_to_img(url)
            arr = img_to_array(img)
            df2 = pd.Series([arr, q], index=df.columns)
            df = df.append(df2, ignore_index=True)

    return df

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
    PATH = ".\\scripts\\drivers\\chromedriver.exe"
    wd = webdriver.Chrome(PATH)
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

    df = get_pixel_arrays(wd, delay, max_images, queries)
    pickle_df(df, "../data/raw_img_arrays.pickle")

    wd.quit()