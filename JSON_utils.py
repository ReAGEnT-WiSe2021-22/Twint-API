import json, os, pandas

# utils class for historical tweets
# all tweets that were written by German representatives should be removed
# also for the MyTweet-Class a attribute "party" (="parteilos") will be added

# get List of user_ids from German representatives
def getUserIds():
    csv_file = pandas.read_csv("Bundestag_Namen_Usernamen_Fraktion.csv", delimiter=";", engine="python")
    id_list = csv_file["user_id"]
    return id_list.values.tolist()


# filter all tweets that are written from German representatives
# append party so we can use the tweets for the MyTweet.scala class
def prepareJSON(filename_in, filename_out, party):
    if not os.path.isfile(filename_in):
        print(f"File {filename_in} is empty!")
        return

    tweets_list = []

    with open(filename_in, encoding="utf") as rf:
        json_objects = rf.readlines()

    for obj in json_objects:
        tweet = json.loads(obj)
        tweet.update({'partei': party})
        tweets_list.append(tweet)

    id_list = getUserIds()
    for tweet in tweets_list:
        for user_id in id_list:
            if tweet["user_id"] == user_id:
                tweets_list.remove(tweet)
                print(f"{user_id} was removed")

    with open(filename_out, 'w', encoding='utf-8') as wf:
        for tweet in tweets_list:
            json.dump(tweet, wf, ensure_ascii=False, indent=4)



##### START PROGRAMM #####

parties = ["CDU", "SPD", "AfD", "FDP", "Die_Gruenen", "Die_Linke"]

for party in parties:
    prepareJSON("scraped_tweets\political_tweets_"+party+"_2021.json",
                "scraped_tweets\political_tweets_"+party+"_2021_cleaned.json", party)


