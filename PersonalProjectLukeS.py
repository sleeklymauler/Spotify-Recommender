import spotipy 
import pprint 
from spotipy.oauth2 import SpotifyClientCredentials
import os 
from dotenv import dotenv_values

# logging in to spotify, using token and secret
credentials = dotenv_values("tokens.env")
clientID = credentials["CLIENT_ID"]
clientSecret = credentials["CLIENT_SECRET"]
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID,
                                                           client_secret=clientSecret))

# make sure to clear format.txt and recommendation.txt at start of program in case they already exist
if os.path.exists("format.txt"):
    os.remove("format.txt")

# this function searches for the user inputted song and formats it so that it looks good
def searchSong(search_term, search_result_offset):
    result = sp.search(q = search_term, offset = search_result_offset, limit = 1, type = 'track', market = 'US')

    # writing data from search into file called format.txt
    with open('format.txt', 'w') as out: 
        pprint.pprint(result, stream=out)

    # create list, fill list with lines from format.txt
    search_list = []
    with open ('format.txt', 'rt') as in_file:
        for line in in_file:
            search_list.append(line.rstrip('\n'))

    # getting line numbers and indexes from search_list[]
    linenumberperm = None
    for linenum, line in enumerate(search_list):  # For every line in lines, enumerated by linenum,
        index = 0               # Set the search index to the first character,
        str = search_list[linenum]	# and store the line in a string variable, str.
        while index < len(str): # While search index is less than the length of the string:
            index = str.find("spotify:track:", index)# If substring is located, set search index to that location.
            if index == -1:         # If nothing is found,
                break                   # break out of the while loop. Otherwise,
            # print("Line: ", linenum, "Index: ", index) # Print the linenum and index of the located substr.
            linenumberperm = linenum; # we now know location of track id
            indexperm = index; # final location of index
            index += len("spotify:track:")    # Before repeating search, increment index by length of substr.

    # printing track id with linenumber from above
    global track_id
    with open ('format.txt') as format: # auto open and close format.txt
        alt=format.readlines()
        if (linenumberperm == None):
            track_id = "Error: Unable to find id, double check spelling"
        else:
            track_id = alt[linenumberperm] # get line that has id
            track_id = track_id.split("spotify:track:",1)[1] # remove front part of id
            track_id = track_id[:-5] # remove end of id

    # get song title
    song_title = ''
    with open ('format.txt') as format: # auto open and close format.txt
        alt = format.readlines()
        if (linenumberperm == None):
            song_title = "Error: Unable to find song_title, double check spelling"
        else:
            try:
                song_title = alt[linenumberperm - 5] # get line that has song_title
                song_title = song_title.split("'name': ",1)[1] # remove front part of song_title
                song_title = song_title[:-2] # remove end of song_title
            except:
                song_title = None

    # get artist title
    artist_title = ''
    with open ('format.txt') as format: # auto open and close format.txt
        alt = format.readlines()
        if (linenumberperm == None):
            artist_title = "Error: Unable to find artist_title, double check spelling"
        else:
            try:
                artist_title = alt[linenumberperm - 17] # get line that has artist_title og is 17
                artist_title = artist_title.split("'name': ",1)[1] # remove front part of artist_title
                artist_title = artist_title[:-2] # remove end of artist_title
                # print("The song artist_title of " + search_term + " is: " + artist_title)
            except:
                artist_title = None
    print("\nSearching for song...\n")
    if song_title == None or artist_title == None:
        print("An error has occurred with that search")
    else:
        print("Search results:\n" + "Song name: " + song_title + "\nArtist name: " + artist_title + "\n")

# this function searches for the user inputted artist and formats it so that it looks good
def searchArtist(search_term, search_result_offset):
    # actually searches
    result = sp.search(q = search_term, offset = search_result_offset, limit = 1, type = 'artist', market = 'US')

    # writing data from search into file called format.txt
    with open('format.txt', 'w') as out: # auto open and close format.txt
        pprint.pprint(result, stream=out)

    # create list, fill list with lines from format.txt
    search_list = []
    with open ('format.txt', 'rt') as in_file: # auto open and close format.txt
        for line in in_file:
            search_list.append(line.rstrip('\n'))

    # getting line numbers and indexes from search_list[]
    linenumberperm = None
    for linenum, line in enumerate(search_list):  # For every line in lines, enumerated by linenum,
        index = 0               # Set the search index to the first character,
        str = search_list[linenum]	# and store the line in a string variable, str.
        while index < len(str): # While search index is less than the length of the string:
            index = str.find("spotify:artist:", index)# If substring is located, set search index to that location.
            if index == -1:         # If nothing is found,
                break                   # break out of the while loop. Otherwise,
            linenumberperm = linenum; # we now know location of track id
            indexperm = index; # final location of index
            index += len("spotify:artist:")    # Before repeating search, increment index by length of substr.

    # printing artist id with linenumber from above
    global artist_id
    with open ('format.txt') as format: # auto open and close format.txt
        alt=format.readlines()
        if (linenumberperm == None):
            artist_id = "Error: Unable to find id, double check spelling"
        else:
            artist_id = alt[linenumberperm] # get line that has id
            artist_id = artist_id.split("spotify:artist:",1)[1] # remove front part of id
            artist_id = artist_id[:-5] # remove end of id

    # get artist title
    artist_title = ''
    with open ('format.txt') as format: # auto open and close format.txt
        alt=format.readlines()
        if (linenumberperm == None):
            artist_title = "Error: Unable to find artist_title, double check spelling"
        else:
            artist_title = alt[linenumberperm - 3] # get line that has artist_title og is 17
            artist_title = artist_title.split("'name': ",1)[1] # remove front part of artist_title
            artist_title = artist_title[:-2] # remove end of artist_title

    print("\nSearching for artist...\n")
    print("Search results:\n" + "Artist name: " + artist_title + "\n")

# this function uses a list of songs and artists gotten from the functions above to get recommendations
def getRecommendations(tracklist, artistlist, genrelist):
    if os.path.exists("recommendation.txt"):
        os.remove("recommendation.txt")

    final_recommendations = sp.recommendations(seed_artists = artistlist, seed_tracks = tracklist, seed_genres = genrelist, limit = 1, country = "US")

    with open ('recommendation.txt', 'w') as out:
        pprint.pprint(final_recommendations, stream=out)

    recommendation_list = []
    with open ('recommendation.txt', 'r') as in_file:
        for line in in_file:
            recommendation_list.append(line.rstrip('\n'))

    permline = None
    for linenum, line in enumerate(recommendation_list):
        index = 0
        str = recommendation_list[linenum]
        while index < len(str):
            index = str.find("'type': 'track'", index)
            if index == -1:
                break
            permline = linenum
            index += len("'type': 'track'")

    global rsong_title
    with open ('recommendation.txt', 'r') as format:
        yeet = format.readlines()
        if (permline == None):
            rsong_title = "Error!"
        else:
            try:
                rsong_title = yeet[permline - 4] # get line that has song_title
                rsong_title = rsong_title.split("'name': ",1)[1] # remove front part of song_title
                rsong_title = rsong_title[:-2] # remove end of song_title
            except:
                rsong_title = None


    permline = None
    for linenum, line in enumerate(recommendation_list):
        index = 0
        str = recommendation_list[linenum]
        while index < len(str):
            index = str.find("'type': 'artist'", index)
            if index == -1:
                break
            permline = linenum
            index += len("'type': 'artist'")

    global rartist_title
    with open ('recommendation.txt') as format: # auto open and close format.txt
        yeet=format.readlines()
        if (permline == None):
            rartist_title = "Error: Unable to find rartist_title, double check spelling"
            # print("Unable to locate rartist_title, double check spelling of term")
        else:
            rartist_title = yeet[permline - 1] # get line that has rartist_title og is 17
            rartist_title = rartist_title.split("'name': ",1)[1] # remove front part of rartist_title
            rartist_title = rartist_title[:-2] # remove end of rartist_title

track_list = []
artist_list = []
genre_list = []
search_type = ''
seed_counter = 0

# basic info about the program
print("\nHello! This program is Luke Sellmayer's Personal Project for the 2018-2019 school year.\n")
print("This program uses the Spotify Web API to provide you with personalized song recommendations.\n")
print("As the user, you will input songs and artists that you like, known as 'seeds', and the program\nwill use those seeds to give you song recommendations.\n")
print("Let's go ahead and enter some seeds by following the prompts below.\n")
print("Please note that when typing in prompts, song names or artist names, spelling and capitalization\nmatter, so be careful when typing or the program might not work.")

while (True):
    search_result_num = 0
    search_type = input("\nWould you like to add a 'song' or 'artist'? Or type 'quit' if you have entered all of your recommendation seeds: ")
    if search_type.lower() == "song":
        search_term_input = input("Enter the song you want to search for: ")
        searchSong(search_term_input, search_result_num)
        add_song_q = "Yeet"
        while (add_song_q.lower() != "yes"):
            add_song_q = input("Would you like to add this song to your recommendation seeds?(yes/no)")
            if (add_song_q.lower() == "yes"):
                track_list.append(track_id)
                seed_counter += 1
            else:
                hitormiss = input("Would you like to see the next search result for this search?(yes/no)")
                if (hitormiss.lower() == "yes"):
                    search_result_num += 1
                    searchSong(search_term_input, search_result_num)
                else:
                    break
    elif search_type.lower() == "artist":
        search_term_input = input("Enter the artist you want to search for: ")
        searchArtist(search_term_input, search_result_num)
        add_artist_q = "Yeet"
        while (add_artist_q.lower() != "yes"):
            add_artist_q = input("Would you like to add this artist to your recommendation seeds?(yes/no)")
            if (add_artist_q.lower() == "yes"):
                artist_list.append(artist_id)
                seed_counter += 1
            else:
                hitormiss = input("Would you like to see the next search result for this search?(yes/no)")
                if (hitormiss.lower() == "yes"):
                    search_result_num += 1
                    searchArtist(search_term_input, search_result_num)
                else:
                    break
                # BUG: if you say stop searching, it keeps on searching
    elif search_type.lower() == "view_seeds":
        print("Seeded songs: " )
        print(track_list)
        print("\nSeeded artists: ")
        print(artist_list)
        print("\nSeeded genres: ")
        print(genre_list)
    elif search_type.lower() == 'quit':
        if seed_counter <= 0:
            print("You need to enter at least one seed before you can quit!")
        else:
            break
    if seed_counter == 5:
        print("\nYou've entered in the max amount of seeds that you can. The program will now continue to give you recommendations.")
        break

print("\nNow that you have entered in the recommendation seeds, the program can now give you your song recommendations.")

while True:
    try:
        rec_num = int(input("\nHow many recommendations would you like? (Minimum is 1, Maximum is 100)"))
        break
    except ValueError:
        print("Make sure that you enter in a number!")

x = 1
while (x <= rec_num):
    getRecommendations(track_list, artist_list, genre_list)
    if rsong_title == None:
        print("An error has occurred with recommendation " + str(x) + ". Trying again...")
    else:
        print("Recommendation " + str(x) + ": ")
        print("    Song name: " + rsong_title)
        print("    Artist name: " + rartist_title)
        x += 1
    if os.path.exists("format.txt"):
        os.remove("format.txt")

if os.path.exists("format.txt"):
    os.remove("format.txt")
if os.path.exists("recommendation.txt"):
    os.remove("recommendation.txt")

closeit = input("\nProgram finished! You can close it and run it again to enter new seeds and get new recommendations. Press the enter key to close...")
