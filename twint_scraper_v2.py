import twint, json, os, time, pandas


# The CSV contains the following parties:
# "CDU", "AfD", "Die_Gruenen", "SPD", "FDP", "Die Linke"
def getKeywordsFromCSV(csv, party):
	rowsOfParty = csv[csv['party'] == party]
	names = rowsOfParty[["screen_name", "full_name"]].values.flatten().tolist()
	names.insert(0, party)  # also look for tweets with "party" as keyword, for example "CDU"
	return names

# Search all tweets that write about a representative or the party itself
# For example: "Christian Lindner" or "c_lindner" or "FDP"
def searchPoliticalTweets(csv, mentionedParty):
	out_filename = "political_tweets_" + mentionedParty + ".json"
	names = getKeywordsFromCSV(csv, mentionedParty)
	print("List of keywords: ", names)

	for name in names:

		print("Searching tweets with keyword: ", name)
		c = twint.Config()

		c.Search = name
		# adjust limit as you like
		#c.Limit = 2000
		c.Retweets = False
		# adjust timespace as you like
		c.Since = '2021-01-01'
		c.Until = '2021-02-28'
		c.Store_json = True
		c.Hide_output = True
		c.Count = True
		c.Output = out_filename

		try:
			twint.run.Search(c)
		except Exception as e:
			print(f"\n Skipped {name} because of:")
			print(f"\n\t {e}")

	return out_filename


##### START PROGRAMM #####

csv_file = pandas.read_csv("Bundestag_Namen_Usernamen_Fraktion.csv", delimiter=";", engine="python")
parties = ["CDU", "SPD", "AfD", "FDP", "Die_Gruenen", "Die Linke"]


print("Tweet extraction started")

for party in parties:
	searchPoliticalTweets(csv_file, party)
	print(f"################################## {party} completed ##################################")

print("Tweet extraction finished")


