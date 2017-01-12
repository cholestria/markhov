import twitter
import os
import sys
from random import choice


def open_and_read_file(filepath):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    file = open(filepath)
    open_file = file.read()
    file.close()

    return open_file


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)    

    return chains


def make_text(chains, max_characters):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]

    while key in chains:
        word = choice(chains[key])
        twitter_text = " ".join(words) + " " + word
        if len(twitter_text) < max_characters:
            words.append(word)
            key = tuple(words[-2:])
        else:
            break    
    
    result = " ".join(words)

    print result
    return result


def tweet_function(chains):
    """takes chains as input and asks if we want to tweet"""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()

    

    user_input = raw_input("Do you want to tweet? ")

    # while True:

    if user_input == "Y":
        status = api.PostUpdate(make_text(chains, 140))
        print status.text

input_path = "janeausten.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains, 140)

# print other_random_text
tweet_status = tweet_function(chains)

# print random_text
