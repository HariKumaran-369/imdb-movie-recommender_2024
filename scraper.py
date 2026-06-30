from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


def get_movie_links(driver, url):
    driver.get(url)
    time.sleep(3)

    movie_links = []
    movies = driver.find_elements(By.CSS_SELECTOR, ".ipc-title-link-wrapper")

    for movie in movies:
        link = movie.get_attribute("href")
        if link and "/title/tt" in link:
            full_link = link.split("?")[0]
            if full_link not in movie_links:
                movie_links.append(full_link)

    return movie_links


def get_movie_details(driver, movie_url):
    movie_name = None
    storyline = None

    try:
        driver.get(movie_url)
        time.sleep(2)

        wait = WebDriverWait(driver, 10)

        try:
            name_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h1[data-testid='hero__pageTitle']")
                )
            )
            movie_name = name_element.text.strip()
        except Exception:
            movie_name = "Unknown"

        try:
            story_element = driver.find_element(
                By.CSS_SELECTOR, "span[data-testid='plot-xl']"
            )
            storyline = story_element.text.strip()
        except Exception:
            try:
                story_element = driver.find_element(
                    By.CSS_SELECTOR, "span[data-testid='plot-l']"
                )
                storyline = story_element.text.strip()
            except Exception:
                storyline = ""

    except Exception as e:
        print(f"Error: {movie_url}-{e}")
        movie_name = None
        storyline = None

    return movie_name, storyline


def scrape_imdb():
    base_url = (
        "https://www.imdb.com/search/title/?"
        "title_type=feature"
        "&release_date=2024-09-01,2024-09-30"
        "&count=50"
        "&sort=num_votes,desc"
    )

    driver = setup_driver()
    all_movies = []
    start_values = [1, 51, 101]
    for start in start_values:
        url = base_url + f"&start={start}"

        movie_links = get_movie_links(driver, url)

        for i, link in enumerate(movie_links):
            result = get_movie_details(driver, link)
            if result is None:
                continue
            name, story = result

            if name and story and len(story) > 50:
                all_movies.append({"movie_name": name, "storyline": story, "url": link})
            time.sleep(1.5)

    driver.quit()
    df = pd.DataFrame(all_movies)
    df.drop_duplicates(subset=["movie_name"], inplace=True)
    df.to_csv("imdb_june_2024.csv", index=False, encoding="utf-8")
    return df


if __name__ == "__main__":
    df = scrape_imdb()
    print(df.head())
