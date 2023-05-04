import pickle
from fuzzywuzzy import fuzz


def find_matching_images(keyword):
    """
    Finds images that match a given keyword based on the labels in the dictionary.

    Args:
    keyword: A string input by the user.

    Returns:
    matched_word: A string representing the closest matching label from the dictionary.
    ratio: An integer representing the partial match ratio of the closest matching label.
    animal_list: A list of strings representing the paths of the images with the closest matching label.
    """
    # Open the file in binary read mode to fetch the pickle data
    with open("label.pickle", "rb") as f:
        # Load the dictionary from the file
        animal_dict = pickle.load(f)

    match_dict = {}
    for word in animal_dict:
        # Calculate the partial match ratio
        ratio = fuzz.partial_ratio(keyword.lower(), word.lower())

        match_dict[word] = ratio

    # Find the word with the highest match ratio
    matched_word = max(match_dict, key=match_dict.get)

    return matched_word, match_dict[matched_word], animal_dict[matched_word]
