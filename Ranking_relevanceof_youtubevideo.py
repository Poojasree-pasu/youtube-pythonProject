###################  Ranking relevance of youtube video results ##############
#Name: Poojasree Pasupuleti
#
#Purpose: Ranking relevance of YouTube video results with the help of review data from previous viewers
#
#Algorithm:
#
#Start
#from selenium import webdriver
#Import pandas
#Import numpy
#from textblob import TextBlob
#Import seaborn as sns
#Import matplotlib.pyplot as plt
#Define launchapp function to Launch Google chrome and open YouTube
#    Prompt user for input
#    Pass the input as argument and search for videos in youtube
#    List of videos are displayed based on the customer search
#Define scraping_analysingdata function
#    Prompt user for input number(n) that n number of videos are to be considered for analysis
#    Take Top ‘n’ search results
#    For details in search results(performs the below steps for all ‘n’considered videos)
#         Collect the customer review data of each video from comments, viewcount, likecount, dislikecount
#    Create a CSV file and save video comments in the file
#    Define sentiment Function
#          Perform sentimental analysis on the comments provided by the customers
#          Validate positive, negative, and neutral comments with the help of testblob library and save it in CSV file
#     Count the number of positive comments for each video
#     Define barplot_likes Function
#           Visualize the likes data using the bar graph
#     Define barplot_comments Function
#           Visualize comments of the videos using the bar graph
#Programs returns the highest-ranking video
# Stop
#########################################################################

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.support.ui import WebDriverWait

likesdict = {"videolikes":[],"likes":[], "comments":[]};
commentspolarityCount = []
videotitle = []
videolinks = []

# Chromedriver path
s = Service("/Users/poojasreepasupuleti/Downloads/chromedriver")
# Invoking chrome
driver = webdriver.Chrome(service=s)


# Launching YouTube and query search
def launchapp(url, user_input):
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(20)
    driver.find_element(By.XPATH, '//input[@id="search"]').send_keys(user_input)
    driver.find_element(By.XPATH, '//input[@id="search"]').send_keys(Keys.RETURN)
    driver.implicitly_wait(100)

# Checking polarity
# Performing sentimental analysis
def sentiment(polarity):
    if polarity < 0:
        p = "Negative"
    elif polarity > 0:
        p = 'Positive'
    else:
        p = 'Neutral'
    return p

# Plotting bargraph for likes
def barplot_likes(dict):
    # print(dict)
    df = pd.DataFrame(data=dict)
    plt.figure(figsize=(8, 5))
    sns.barplot(x = "videolikes", y = "likes", data = df, palette="Blues")
    plt.xlabel('Analysis of video likes', fontsize=20)
    plt.ylabel('likes', fontsize=20)
    plt.show()

# Plotting bargraph for comments
def barplot_comments(dict):
    # print(dict)
    df = pd.DataFrame(data=dict)
    plt.figure(figsize=(8, 5))
    sns.barplot(x = "videolikes", y = "comments", data = df, palette="Blues")
    plt.xlabel('Analysis of video comments', fontsize=20)
    plt.ylabel('comments', fontsize=20)
    plt.show()

# Scraping Youtube comments, likes, dislikes and views data
def scraping_analysingdata(url, user_input, num_videos):
    launchapp(url, user_input)
    searchresults_links = []
    find_href = []
    # Fetching links of youtube videos(search results)
    for i in range(1, num_videos):
        val = str(i)
        find_href = driver.find_elements(By.XPATH, '(//a[@id="video-title"])[' + val + ']')
        for my_href in find_href:
            searchresults_links.append(my_href.get_attribute("href"))
    print(searchresults_links)
    for index, i in enumerate(searchresults_links):
        val1 = str(index)
        driver.get(i)
        driver.implicitly_wait(70000)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/h1/yt-formatted-string'))
        )
        # Fetching titles of video
        video_title = driver.find_element(By.XPATH, '//*[@id="container"]/h1/yt-formatted-string').text
        print("Title of the video: ", index, ":", video_title)
        driver.implicitly_wait(20)
        videotitle.append(video_title)
        # Scraping views data of videos
        views = driver.find_element(By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text
        print("Views of the video: ", index, ":", views)
        # Scraping likes data of videos
        #Likes
        vallikes1 = driver.find_element(By.XPATH, '(//yt-formatted-string[@class="style-scope ytd-toggle-button-renderer style-text"])[1]').get_attribute("aria-label")
        print("Likes of the video: ", index, ":", vallikes1)
        likessplit = vallikes1.split(' ')
        likessplit1 = likessplit[0]
        if ',' in likessplit1:
            likessplit2 = likessplit1.split(',')
            likessplit3 = likessplit2[0] + likessplit2[1]
            likescount = int(likessplit3)
            print(likescount)
        else:
            likescount = int(likessplit1)
            print(likescount)
        likesdict["videolikes"].append('Video'+val1)
        likesdict["likes"].append(likescount)
        # Scraping dislikes data of videos
        #Dislikes
        val_dislikes = driver.find_element(By.XPATH,'(//yt-formatted-string[@class="style-scope ytd-toggle-button-renderer style-text"])[2]').get_attribute("aria-label")
        print("Dislikes of the video: ", index, ":", val_dislikes)
        driver.implicitly_wait(50)
        driver.execute_script('window.scrollTo(0,600);')
        driver.implicitly_wait(50)
        # print('scrolled')
        sort = driver.find_element(By.XPATH, '//*[@id="icon-label"]')
        sort.click()
        time.sleep(10)
        # Fetching first 20 comments data of videos
        topcomments = driver.find_element(By.XPATH,'//a[@class="yt-simple-endpoint style-scope yt-dropdown-menu iron-selected"]')
        topcomments.click()
        time.sleep(10)
        for j in range(0,2):
            driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));")
            time.sleep(10)
        totalcomments = len(driver.find_elements(By.XPATH, '//*[@id="content-text"]'))
        if totalcomments < 20:
            index = totalcomments
        else:
            index = 20

        count = 0
        comments = []
        while count < index:
            try:
                comment = driver.find_elements(By.XPATH, '//*[@id="content-text"]')[count].text
                count = count + 1
                # print(comment)
                comments.append(comment)
            except:
                comment = ""
        # Performing sentimnetal analysis
        polarity = []
        subjectivity = []
        sentiment_type = []
        for word in comments:
            p = TextBlob(word)
            polarity.append(p.sentiment.polarity)
            subjectivity.append(p.sentiment.subjectivity)
            s = sentiment(p.sentiment.polarity)
            sentiment_type.append(s)
        # Saving the data into CSV sheets
        dataframe = {"comment": comments, "sentiment_type": sentiment_type, "polarity": polarity , "subjectivity": subjectivity}
        df = pd.DataFrame.from_dict(dataframe, orient='index')
        df1 = df.transpose()
        df1.columns = ['comment','polarity','sentiment_type','subjectivity']
        df1.to_csv(r"/Users/poojasreepasupuleti/Documents/Python/python_Project/Commentsdata_CSV/"+video_title+".csv", header = True, encoding='utf-8', index=False)
        train_data = pd.read_csv("/Users/poojasreepasupuleti/Documents/Python/python_Project/Commentsdata_CSV/"+video_title+".csv")
        col_one_list = train_data['polarity'].tolist()
        count = 0
        for posval in col_one_list:
            if posval == 'Positive':
                count = count + 1
        commentspolarityCount.append(count)
        likesdict["comments"].append(count)

# Calling the objects
url = 'https://www.youtube.com/'
user_input = input("Enter the input to search for: ")
num_videos = int(input("Enter number of videos: "))
scraping_analysingdata(url, user_input, num_videos)
maxcommentcount = max(commentspolarityCount)
index = commentspolarityCount.index(maxcommentcount)
# Printing the Highest ranking video
print('The Highest ranking video with more positive comments is : video', index, 'with title name: ', videotitle[index])
barplot_likes(likesdict)
barplot_comments(likesdict)


# Libraries :
# Selenium: Selenium is a Python library and tool used for automating web browsers and also used for web-scraping to extract useful data and information. In this project, I am using selenium for automating the Google chrome, YouTube and extracting the data like Comments, Views, Likes and dislikes of the YouTube videos.
# Pandas: Pandas is an open-source Python library used for data manipulation and analysis. And allows the handling of tabular data
# NumPy: NumPy is a library in python. It is used for performing mathematical and logical operations on Arrays.
# Text blob: Text blob is an open-source python library for processing textual data. It is used for performing sentiment analysis
# Seaborn and Matplotlib: Seaborn and Matplotlib are open-source Python libraries that are used for data visualization and exploratory data analysis. Seaborn works easily with dataframes. Matplotlib provides various methods to Visualize data in more effective way.
