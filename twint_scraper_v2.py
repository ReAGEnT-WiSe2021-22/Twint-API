import twint, json, os, time, pandas
from pprint import pprint

TWEETS_DUMP_FILENAME = "abgeordnete_tweets.json"
META_DUMP_FILENAME = "abgeordnete_meta.json"


# The CSV contains the following parties:
# "CDU", "AfD", "B90/Die Grünen", "SPD", "FDP", "Die Linke"
def getNamesFromCSV(csv, party):
	rowsOfParty = csv[csv['party'] == party]
	names = rowsOfParty[["screen_name", "full_name"]].values.flatten().tolist()
	names.insert(0, party)
	return names


def searchPoliticalTweets(csv, mentionedParty):
	out_filename = "political_tweets_" + mentionedParty + ".csv"
	names = getNamesFromCSV(csv, mentionedParty)[1:3]
	print("List of names: ", names)

	for name in names:

		print("Searching tweets with keyword: ", name)
		c = twint.Config()

		c.Search = name
		c.Limit = 100
		c.Store_csv = True
		c.Hide_output = True
		c.Retweets = False
		c.Count = True
		c.Since = '2021-06-01'
		c.Until = '2021-11-01'
		c.Output = out_filename

		try:
			twint.run.Search(c)
		except Exception as e:
			print(f"\n Skipped {name} because of:")
			print(f"\n\t {e}")

	return out_filename


def searchUserTweets(username):
	out_filename = "abgeordnete_tweets_" + username + ".json"

	c = twint.Config()

	c.Username = username
	c.Store_json = True
	c.Hide_output = True
	c.Retweets = True
	#c.Since = '2021-05-24'
	#c.Until = '2021-05-31'
	c.Output = out_filename

	try:
		twint.run.Search(c)
	except Exception as e:
		print(f"\n Skipped {username} because of:")
		print(f"\n\t {e}")
	
	return out_filename

def searchUserMeta(username):
	out_filename = "abgeordnete_meta_" + username + ".json"

	c = twint.Config()

	c.Username = username
	c.Store_json = True
	c.Hide_output = True
	c.Output = out_filename

	
	try:
		twint.run.Lookup(c)
	except Exception as e:
		print(f"\n Skipped {username} because of:")
		print(f"\n\t {e}")

	return out_filename


def appendPartyToJson(filename, party):
	if not os.path.isfile(filename):
		print(f"File {filename} is empty!")
		return

	final_json = {}
	tweets_list = []

	with open(filename) as rf:
		jsonObjects = rf.readlines()

	for obj in jsonObjects:
		tweet = json.loads(obj)
		#pprint(tweet)
		tweet.update({'partei' : party})
		tweets_list.append(tweet)

	with open(TWEETS_DUMP_FILENAME, 'a', encoding='utf-8') as wf:
		for tweet in tweets_list:
			json.dump(tweet, wf, ensure_ascii=False, indent=4)

	os.remove(filename)


##### START PROGRAMM #####

csv_file = pandas.read_csv("Bundestag_Namen_Usernamen_Fraktion.csv", delimiter=';', engine='python')
print("Start")
searchPoliticalTweets(csv_file, "CDU")

#with open('abgeordnete_usernamen_twitter.json') as rf:
#	partymemebers = json.load(rf)

#for party in partymemebers.keys():
#	print(f"Processing party: {party} ...")
#	members = partymemebers[party]
	
#	for member in members:
#		print(f"Current account: {member}")
#		result_filename = searchUserTweets(member)
#		appendPartyToJson(result_filename, party)