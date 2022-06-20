import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


IMDB_BUTTON_PATH = "/html//a[@id='home_img_holder']"
SEARCH_PATH = '//*[@id="suggestion-search"]'
MENU_BUTTON_PATH = '//*[@id="imdbHeader-navDrawerOpen--desktop"]'
SEARCH_BAR_FIRST_MOVIE_PATH = "/html/body/div[2]/nav/div[2]/div[1]/form/div[2]/div/div/div/ul/li[1]"
OSCAR_BUTTON_PATH = '//*[@id="imdbHeader"]/div[2]/aside/div/div[2]/div/div[3]/span/div/div/ul/a[1]/span'
SELECT_YEAR_PATH = '/html/body/div[2]/div/div[2]/div[3]/div/div[2]/div[3]/span/div/div/div[2]/div[16]/span[4]/a'
DIRECTOR_NAME_PATH = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div'
WRITER_NAME_PATH = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[2]/div'
STARS_NAME_PATH = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div'
ALL_PHOTOS_PATH = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[2]/div[1]/a/h3'
BROKEN_LINK_CHECKER_PATH = "//div[@id='media_index_thumbnail_grid']/a[@href]"


def movie_checker(movie_name, movie_path):
    def save(text):
        with open("save.txt", mode="a+", encoding="utf-8") as log:
            log.write(text + movie_name + "\n")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.imdb.com/")
    menuButton = driver.find_element(By.XPATH, MENU_BUTTON_PATH)
    menuButton.click()
    time.sleep(1)

    oscarButton = driver.find_element(By.XPATH, OSCAR_BUTTON_PATH)
    oscarButton.click()
    time.sleep(1)

    selectYear = driver.find_element(By.XPATH, SELECT_YEAR_PATH)
    selectYear.click()
    time.sleep(1)

    selectMovie = driver.find_element(By.XPATH, movie_path)
    selectMovie.click()
    time.sleep(1)

    directorName = driver.find_element(By.XPATH, DIRECTOR_NAME_PATH)
    saveDirector = directorName.text
    writerName = driver.find_element(By.XPATH, WRITER_NAME_PATH)
    saveWriter = writerName.text
    starsName = driver.find_element(By.XPATH, STARS_NAME_PATH)
    saveStars = starsName.text
    time.sleep(1)

    homePage = driver.find_element(By.XPATH, IMDB_BUTTON_PATH)
    homePage.click()

    searchMovie = driver.find_element(By.XPATH, SEARCH_PATH)
    searchMovie.send_keys(movie_name)
    time.sleep(2)

    firstMovieSelect = driver.find_element(
        By.XPATH, SEARCH_BAR_FIRST_MOVIE_PATH)
    firstMovieSelect.click()

    otherDirectorName = driver.find_element(By.XPATH, DIRECTOR_NAME_PATH)
    if otherDirectorName.text == saveDirector:
        save("Director name match successful. ")
    else:
        save("Director name match failed! ")

    otherWriterName = driver.find_element(By.XPATH, WRITER_NAME_PATH)
    if otherWriterName.text == saveWriter:
        save("Writer name match successful. ")
    else:
        save("Writer name match failed! ")

    otherStarsName = driver.find_element(By.XPATH, STARS_NAME_PATH)
    if otherStarsName.text == saveStars:
        save("Stars name match successful. ")
    else:
        save("Stars name match failed! ")

    allPhoto = driver.find_element(By.XPATH, ALL_PHOTOS_PATH)
    allPhoto.click()

    photos = driver.find_elements_by_xpath(
        "//div[@id='media_index_thumbnail_grid']/a[@href]")
    print("BROKEN LINK CHECKER WORKING...")
    for photo in photos:
        photoLink = photo.get_attribute("href")
        res = requests.request("GET", photoLink)
        if res.status_code != 200:
            with open("save.txt", mode="a+", encoding="utf-8") as log:
                log.write("BROKEN LINK! " + photo.text + "\n")

    driver.close()


SELECT_CIRCUS_PATH = '//*[@id="center-3-react"]/div/div/div[2]/h3/div/div/div/div[2]/div[2]/div[2]/div[2]/a'
movie_checker("The Circus", SELECT_CIRCUS_PATH)

SELECT_JAZZ_SINGER_PATH = '//*[@id="center-3-react"]/div/div/div[1]/h3/div[10]/div[2]/div[1]/div[2]/div[2]/div/div[2]/a'
movie_checker("The Jazz Singer", SELECT_JAZZ_SINGER_PATH)
