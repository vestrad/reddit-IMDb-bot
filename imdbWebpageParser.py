import praw
from bs4 import BeautifulSoup
import requests
import winsound
import time
def findRating(PAGE_URL):
    response = requests.get(PAGE_URL)
    results_page = BeautifulSoup(response.content, 'lxml')
    try:
        results = results_page.find("span", {"itemprop":"ratingValue"})
        rating = results.getText()
        results = results_page.find("div",class_="summary_text")
        description = results.getText().lstrip()
        rating += "\n\nDescription: {0}".format(description)
        return rating
    except:
        return "Not available"
def findSearchPage(SEARCH_WORD):
    searchList = SEARCH_WORD.split()
    searchPhrase = "+".join(searchList)
    url = "https://www.imdb.com/find?s=tt&q=" + searchPhrase + "&ref_=nv_sr_sm"
    response = requests.get(url)
    results_page = BeautifulSoup(response.content, 'lxml')
    try:
        results = results_page.find("td", class_="result_text")
        results = results.find('a')
        phrase = results['href']
        url = "https://www.imdb.com" + phrase
        return findRating(url), url
    except:
        return "Rating not available", "imdb.com"
def eraseUpTo(comment, KEYPHRASE):
    index = comment.find(KEYPHRASE)
    return comment[index:]
def findSentence(text):
    list = text.split()
    list.pop(0)
    result = " "
    result = result.join(list)
    #print(result)
    return result
def runBot(SUBREDDIT, KEYPHRASE):
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(SUBREDDIT)
    for comment in subreddit.stream.comments(skip_existing=True):
        print("************************")
        print(comment.body)
        if KEYPHRASE in comment.body.lower():
            winsound.Beep(2500, 1000)
            text = eraseUpTo(comment.body.lower(), KEYPHRASE)
            text = findSentence(text)
            if text.isspace() or text == "":
                comment.reply("Invalid entry")
            else:
                rating , url= findSearchPage(text)
                link = "[" + text.title() + "](" + url + ")"
                reply = "The found rating of " + link + " is: " + rating
                comment.reply(reply)
                print("Replying " + reply)
                time.sleep(2)
def main():
    #SUBREDDIT = input("Enter the subreddit: ")
    #KEYPHRASE = input("Enter the keyphrase: ")
    SUBREDDIT = "testingground4bots"
    KEYPHRASE = "!imdb"
    runBot(SUBREDDIT, KEYPHRASE)
main()
#print(findRating("https://www.imdb.com/title/tt0343818/?ref_=fn_al_tt_1"))
