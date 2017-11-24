import time
import datetime
import random
import os
import sys
import movies
import tv_series
import sel_utils
import proxy
from decimal import Decimal 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Setup Django project to work in other modules
proj_path = "/home/sainjusajan/professional/googleplay"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "googleplay.settings")
sys.path.append(proj_path)
# This is so my local_settings.py gets loaded.
os.chdir(proj_path)
# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from playmovies.models import *



def movieWorks():
    main_url = 'https://play.google.com/store/search?q=HBO&c=movies'
    # Ping the browser until a workable ip is found
    while True:
        driver = sel_utils.initWebdriver()
        try:
            driver.get(main_url)
            time.sleep(random.randint(4,9))
            print(driver.title)
            assert 'hbo' in driver.title.lower()
            today = str(datetime.date.today())
            name = os.path.dirname(os.path.realpath(__file__)) + "/screenshots/homepage/homepageFor" + today + ".png"
            print(name)
            driver.get_screenshot_as_file(name)
            sel_utils.scrollToBottom(driver)
            time.sleep(random.randint(3,5))
            
            if sel_utils.isPresent(driver, By.XPATH, "//a[@aria-label=' Check out more content from Movies ']"):
                more_button = driver.find_element(By.XPATH, "//a[@aria-label=' Check out more content from Movies ']")
                more_button.click()
                print("Clicked 'more movies'...")
                time.sleep(random.randint(3,4))
                break
            else:
                print("Page fully not loaded...Retrying..")
                raise AssertionError
        except Exception as e:
            print(e)
            print("Proxy IP not working. Trying new one..")
            driver.quit()

    allMovies = movies.getMoviesList(driver)
    driver.quit()

    time.sleep(random.randint(3,5))
    test_movies = allMovies[3:5]

    # Start a new webdriver session for movie details
    # Restart in between
    # Ping the browser until a workable ip is found
    # today = datetime.date.today()
    # day_db, day_created = Day.objects.get_or_create(date=today)
    for movie in test_movies:
        time.sleep(random.randint(20,30))
        while True:
            driver = sel_utils.initWebdriver()
            try:
                driver.get(movie['url'])
                time.sleep(random.randint(4,6))
                print(driver.title)
                assert 'movies & tv' in driver.title.lower()
                break
            except Exception as e:
                print(e)
                print("Proxy IP not working. Trying new one..")
                time.sleep(random.randint(2,3))
                driver.quit()
        
        # driver.get(movie['url'])
        sel_utils.scrollToBottom(driver)
        time.sleep(random.randint(3,4))
        # look for 'Read more' if present in description
        if sel_utils.isPresent(driver, By.XPATH, "//span[contains(text(), '{0}')]".format("Read more")):
            read_more = driver.find_element_by_xpath("//span[contains(text(), '{0}')]".format("Read more"))
            action_read = ActionChains(driver)
            action_read.move_to_element(read_more).click().perform()
            time.sleep(random.randint(2,3))
        
        # Now get the data
        title = movies.getTitle(driver)
        releaseDate = movies.getReleaseDate(driver)
        runtime = movies.getRuntime(driver)
        genre = movies.getGenre(driver)
        starRatings = movies.getStarRatings(driver)
        nRatings = movies.getNRatings(driver)
        # rentContent = getRentButton(driver) 
        buyContent = movies.getBuyButton(driver)
        
        descript = movie['details']
        actors = movies.getActors(driver)
        producers = movies.getProducers(driver)
        directors = movies.getDirectors(driver)
        writers = movies.getWriters(driver)
        coverImage = movies.getCoverImage(driver)
        trailerVideo = movies.getTrailerVideo(driver)

        print("All movie data scraped successfully..")
        driver.quit()

        time.sleep(random.randint(2,3))
        print("Now, heading towards the database..")

        # Now populate the database tables
        # Save the actors 
        # actors = {'a':'url1', 'b':'url2',...}
        actors_movie = []
        for i in actors:
            actor_db, created = Actor.objects.get_or_create(name=i, url=actors[i])
            print(actor_db, created)
            actors_movie.append(actor_db)
        print("Actors added to db..")

        # Save the producers
        # producers = {'a':'url1', 'b':'url2',...}
        producers_movie = []
        for j in producers:
            producer_db, created = Producer.objects.get_or_create(name=j, url=producers[j])
            print(producer_db, created)
            producers_movie.append(producer_db)
        print("Producers added to db..")

        # Save the directors
        # directors = {'a':'url1', 'b':'url2',...}        
        directors_movie = []
        for k in directors:
            director_db, created = Director.objects.get_or_create(name=k, url=directors[k])
            print(director_db, created)
            directors_movie.append(director_db)
        print("Directors added to db..")

        # Save the writers
        # writers = {'a':'url1', 'b':'url2',...}
        writers_movie = []
        for l in writers:
            writer_db, created = Writer.objects.get_or_create(name=l, url=writers[l])
            print(writer_db, created)
            writers_movie.append(writer_db)
        print("Writers added to db..")

        # Save the genre/s
        genres_movie = []
        for m in genre:
            genre_db, created = Genre.objects.get_or_create(name=m, url=genre[m])
            print(genre_db, created)
            genres_movie.append(genre_db)
        print("Genres added to db..")

        # Now save the movie data
        # Important thing to note: "date: today", save the movie for today
        movie_db, created = Movie.objects.get_or_create(date = today, name=title)
        print(movie_db, created)
        # Save movie item only if the movie is not already saved to database today
        if created == True:
            movie_db.poster       = coverImage
            movie_db.length       = runtime
            movie_db.rating       = starRatings
            movie_db.n_raters     = nRatings
            movie_db.trailer      = trailerVideo
            movie_db.url          = movie['url']
            movie_db.description  = descript

            # Add all the crew information
            for actor in actors_movie:
                movie_db.actors.add(actor)
            for producer in producers_movie:
                movie_db.producers.add(producer)
            for director in directors_movie:
                movie_db.directors.add(director)
            for writer in writers_movie:
                movie_db.writers.add(writer)
            for genre in genres_movie:
                movie_db.genre.add(genre)
            movie_db.save()
        print("Movie data successfully added to the database..")
    #     day_db.movies.add(movie_db)
    # day_db.save()
        
        
    print("All movies data added to database..")
    # print("All movies added to today...")
    


def tvWorks():
    main_url = 'https://play.google.com/store/search?q=HBO&c=movies'

    # Ping the browser until a workable ip is found
    # Check for the more shows button
    # Check for the title of the page
    while True:
        driver = sel_utils.initWebdriver()
        try:
            driver.get(main_url)
            time.sleep(random.randint(4,9))
            print(driver.title)
            assert 'hbo' in driver.title.lower()
            time.sleep(random.randint(3,5))
            if sel_utils.isPresent(driver, By.XPATH, "//a[@aria-label=' Check out more content from TV Shows ']"):
                more_button = driver.find_element(By.XPATH, "//a[@aria-label=' Check out more content from TV Shows ']")
                more_button.click()
                print("Clicked 'more tv series'...")
                time.sleep(random.randint(4,7))
                break
            else:
                print("Page not loaded fully.. trying again...")
                raise AssertionError
        except Exception as e:
            print(e)
            print("Proxy IP not working. Trying new one..")
            driver.quit()    
    time.sleep(random.randint(3,4))

    # Now get all the tv series list
    allSeries = tv_series.getSeriesList(driver)
    driver.quit()
    print("Series list data extracted...")
    print(allSeries)

    # Scrape the tv series details page one by one 
    test_series = allSeries[3:5]
    for series in test_series:
        time.sleep(random.randint(20,30))
        while True:
            driver = sel_utils.initWebdriver()
            try:
                driver.get(series['url'])
                time.sleep(random.randint(2,4))
                WebDriverWait(driver,10).until(EC.title_contains('Movies & TV'))
                print(driver.title)
                break
            except Exception as e:
                print(e)
                print("Proxy IP not working. Trying new one..")
                time.sleep(2)
                driver.quit()
        # driver.get(movie['url'])
        sel_utils.scrollToBottom(driver)
        time.sleep(random.randint(4,7))
        
        # Now get the series info
        description = series['details']
        url = series['url']
        poster, title, rating, n_raters, genres, release_date = tv_series.getSeriesInfo(driver)
        series_dict = {
            'title'        : title,
            'description'  : description,
            'url'          : url,
            'poster'       : poster,
            'rating'       : rating,
            'n_raters'     : n_raters,
            'genres'       : genres,
            'release_date' : release_date,
        }
        print("Series full info initiating >>>")
        # Now pass this dict to append season and episode details
        fullSeriesDetails = tv_series.getSeriesFullDict(driver, series_dict)

        # Now start the db works
        print("Adding series to database >>>")
        SaveSeriesToDB(fullSeriesDetails)       
        print("\n")


def SaveSeriesToDB(series_dict):
    '''
    Use the full series dictionary to save it to db
    dict = {
			'title'        : 'GOT',
			'poster'       : 'abc.com',
			'rating'       : '4.9',
			'n_raters'     : '10000',
			'genres'       : ['Drama'], 
			'release_date' : '2010',
			'description'  : 'GOT is awesome',
			'url'          : 'abc.com',
			'genres'       : ['Drama',],
			'seasons':{
				'season 1': {
					'cost': '30$',
					'url': 'abc.com',
					'episodes': 
						{
						'episode1':{
							'name'         : 'Dragonstone', 
                            'cost'         : '1.99$',
							'description'  : 'alksjfdsd ldsfj',
							'poster'       : 'jsdlfjlks',
							'release_date' : '12 Jan 2013',
							'url'          : 'alsdjkf.dslfjk',
						},...
					}
				},...
			}
	}
    '''
    today = datetime.date.today()
    SeriesDict = series_dict
    seasons = SeriesDict['seasons']
    genres = SeriesDict['genres']
    genres_series = []
    for m in genres:
        genre_db, created = Genre.objects.get_or_create(name=m, url=genres[m])
        print(genre_db, created)
        genres_series.append(genre_db)
    print("Genres added to db..")
    for season in seasons:
        season_db, created_season = TVSeason.objects.get_or_create(name=season, url=seasons[season]['url'])        
        print(season_db, created_season)
        if created_season == True:
            season_db.cost = seasons[season]['cost']
            episodes = seasons[season]['episodes']
            for episode in episodes:
                episode_db, created_episode = TVEpisode.objects.get_or_create(name=episodes[episode]['title'], number=episode)
                print(episode_db, created_episode)
                if created_episode == True:
                    episode_db.cost            =  episodes[episode]['cost']
                    episode_db.description     =  episodes[episode]['description']
                    episode_db.poster          =  episodes[episode]['cover_image']
                    episode_db.releaseDate     =  episodes[episode]['release_date']
                    episode_db.url             =  episodes[episode]['url']
                    episode_db.save()
                    season_db.episodes.add(episode_db)
            season_db.save()
            print("{} saved to db..".format(season_db))
            series_db, created_series = TVSeries.objects.get_or_create(date=today, season=season_db)
            print(series_db, created_series)
            if created_series == True:
                series_db.name          =  SeriesDict['title']
                series_db.poster        =   SeriesDict['poster']
                series_db.rating        =   SeriesDict['rating']
                series_db.n_raters      =   SeriesDict['n_raters']
                series_db.url           =   SeriesDict['url']
                series_db.releaseDate   =   SeriesDict['release_date']
                series_db.description   =   SeriesDict['description']
                for i in genres_series:
                    series_db.category.add(i)
                series_db.save()
                print("{} saved to db..".format(series_db))
    #             if not series_db in day_db.tvseries.all():
    #                 day_db.add(series_db)
    
    # day_db.save()
    # print("All tv series added for today db...")
    # website_db = Website.objects.create(day=day_db)
    # print("\n\nWebsite for today added successfully...\n\n")


def dayWiseWorks():
    day = datetime.date.today()
    day_db, created = Day.objects.get_or_create(day=day)
    # run movieWorks
    movieWorks()
    time.sleep(random.randint(5,10))
    print("Initializing tv works ...")
    tvWorks()
    allMovies = Movie.objects.filter(date=day)
    for i in allMovies:
        day_db.movies.add(i)
    print("All movies saved to today db..")
    allSeries = TVSeries.objects.filter(date=day)
    for j in allSeries:
        day_db.tvseries.add(j)
    day_db.save()
    print("Today's db works done..")
    website_db, web_created = Website.objects.get_or_create(day=day_db)
    print("website for {} created ...".format(website_db.day))
