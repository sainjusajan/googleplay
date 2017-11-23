# -*- coding: utf-8 -*-
# Import selenium reqs

from playmovies import sel_utils


# Setup Django to use models



# Once after entering the movies list page, run the function below
# Expected to work for tv series as well
def getMoviesList(driver):
    sel_utils.scrollToBottom(driver)
    movies = []
    movies_elements = driver.find_elements_by_xpath("//div[@class='id-card-list card-list two-cards']/div")
    # print(movies_elements)
    try:
        for i in movies_elements:
            movie = {}
            content = i.find_element_by_xpath(".//div")
            url = content.find_element_by_tag_name('a').get_attribute('href')
            details = content.find_element_by_xpath(".//div[@class='description']").text
            movie['url'] = url
            movie['details'] = details
            movies.append(movie)

    except Exception as e:
        print(e)
    else:
        print(str(len(movies)) + " movies found")
        return movies
        

        

# Get actors
def getActors(driver):
    actor_elements = driver.find_elements_by_xpath("//span[@itemprop='actor']")
    actors = {}
    for i in actor_elements:
        actor_url = i.find_element_by_tag_name('a').get_attribute('href')
        actor = i.text
        actors[actor] = actor_url
    print(actors)
    return actors

# Get producers
def getProducers(driver):
    producer_elements = driver.find_elements_by_xpath("//span[@itemprop='producer']")
    producers = {}
    for i in producer_elements:
        producer_url = i.find_element_by_tag_name('a').get_attribute('href')
        producer = i.text
        producers[producer] = producer_url
    print(producers)
    return producers

# Get directors
def getDirectors(driver):
    director_elements = driver.find_elements_by_xpath("//span[@itemprop='director']")
    directors = {}
    for i in director_elements:
        director_url = i.find_element_by_tag_name('a').get_attribute('href')
        director = i.text
        directors[director] = director_url
    print(directors)
    return directors

# Get writers
def getWriters(driver):
    writer_elements = driver.find_elements_by_xpath("//span[@itemprop='writer']")
    writers = {}
    for i in writer_elements:
        writer_url = i.find_element_by_tag_name('a').get_attribute('href')
        writer = i.text
        writers[writer] = writer_url
    print(writers)
    return writers

# Get cover image
def getCoverImage(driver):
    image_element = driver.find_element_by_xpath("//img[@alt='Cover art' and @itemprop='image']")
    image_url = image_element.get_attribute('src')
    print(image_url)
    return image_url

# Get trailer video
def getTrailerVideo(driver):
    trailer_element = driver.find_element_by_xpath("//body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz/div/div/button")
    trailer_url = trailer_element.get_attribute('data-trailer-url')
    print(trailer_url)
    return trailer_url

# Get movie title
def getTitle(driver):
    title_element = driver.find_element_by_xpath("//body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/h1")
    title = title_element.text
    print(title)
    return title

# Get Release date
def getReleaseDate(driver):
    date_element = driver.find_element_by_xpath("//body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/div/div[1]/span[1]")
    date = date_element.text
    print(date)
    return date

# get runtime
def getRuntime(driver):
    runtime_element = driver.find_element_by_xpath("//meta[@itemprop='duration']")
    runtime = runtime_element.get_attribute('content')
    print(runtime)
    return runtime

# get Genre
def getGenre(driver):
    genreElement = driver.find_element_by_xpath("//a[@itemprop='genre']")
    genre = genreElement.text
    genre_url = genreElement.get_attribute('href')
    print({genre:genre_url})
    return {genre: genre_url}

# get star ratings
def getStarRatings(driver):
    ratings_element = driver.find_element_by_xpath("//body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div")
    ratings = ratings_element.get_attribute('aria-label')
    print(ratings[6:9])
    return ratings[6:9]

# get n_ratings
def getNRatings(driver):
    nrating_element = driver.find_element_by_xpath("//body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/div/div[2]/span/span[1]")
    nratings = nrating_element.text
    print(nratings)
    return nratings

# Rent button
def getRentButton(driver):
    rentBElement = driver.find_element_by_xpath("//button[contains(@aria-label,'Rent')]")
    rentcontent = rentBElement.text
    print(rentcontent)
    return rentcontent

# Buy button
def getBuyButton(driver):
    buyBElement = driver.find_element_by_xpath("//button[contains(@aria-label,'Buy')]")
    buycontent = buyBElement.text
    print(buycontent)
    return buycontent


# Get Screenshot
def getScreenshot(driver, filename):
    driver.save_screenshot(filename)
