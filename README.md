# Twint-API
Inofficial API for Twitter Frontend for scraping tweets of german federal delegates

## Requirements

Python 3  
Twint (pip3 install twint)

## Usage of scraper

Execute `python3 twint_scraper.py` in the cloned git repository.  

Modify the date range in the `searchUserTweets()` function in `twint_scaper.py` or leave it commented out to get all tweets. It takes approximately 10 minutes for 7 days of tweets or 8 hours to get all existing tweets. 

To add or remove twitter accounts edit the `abgeordnete_usernamen_twitter.json` file.  

NOTE: It can only scrape the last 3200 tweets of an account. This is not a limitation of twint but of twitter. Checkout the twint project page to learn more: https://github.com/twintproject/twint

## Usage of scraper v2

There are several names of German representatives in the file `Bundestag_Namen_Username_Fraktion.csv` which are use as keywords in the method `searchPoliticalTweets()`

The tweets are stored separately according to the party of the German representatives

Like in the first scraper you can modify the data range.

With `JSON_utils.py` you can clean the data by removing all tweets written by German representatives.

Also the party of each tweet will be added to the json-object.

Caution: You may have to adjust the filepath in `JSON_utils.py`