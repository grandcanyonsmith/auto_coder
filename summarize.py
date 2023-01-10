# importing libraries
import nltk
import pandas as pd

nltk.download("wordnet")
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# function that reads a file and returns the content
def read_file(file_name):
    """This function reads a file and returns the content"""
    try:
        with open(file_name, "r") as fp:
            content = fp.read()
        return content
    except Exception as e:
        print(f"Error: {e}")


# function that does the stemming
def stem_content(content):
    """This function does the stemming"""
    try:
        # instantiating the stemmer
        stemmer = PorterStemmer()

        # split the sorce file into words
        words = content.split()

        return [stemmer.stem(word) for word in words]
    except Exception as e:
        print(f"Error: {e}")


# function to lemmantize
def lemmatize_content(content):
    """This function lemmatizes the content"""
    try:
        # instantiating the lemmatizer
        lemmatizer = WordNetLemmatizer()

        # split the source file into words
        words = content.split()

        return [lemmatizer.lemmatize(word) for word in words]
    except Exception as e:
        print(f"Error: {e}")


# function to tokenize the words
def tokenize_words(content):
    """This function tokenizes the words"""
    try:
        # tokenize the words
        words = word_tokenize(content)

        return words
    except Exception as e:
        print(f"Error: {e}")


# main function
def main():
    # get the content from the file
    file_name = input("Enter the file name: ")
    content = read_file(file_name)

    # tokenize the words
    words_tokenized = tokenize_words(content)

    # stem the words
    words_stemmed = stem_content(content)

    # lemmantize the words
    words_lemmatized = lemmatize_content(content)

    # creating the list of words
    words_list = []

    for i in range(len(words_stemmed)):
        if words_stemmed[i] == words_lemmatized[i]:
            words_list.append(words_stemmed[i])
        else:
            words_list.append(words_stemmed[i] + "/" + words_lemmatized[i])

    # print the list of words
    print("The list of words is:")
    for word in words_list:
        print(word)


# run the file
if __name__ == "__main__":
    main()


# # 1. Download and install the necessary libraries for NLTK:

# #         $ pip install nltk

# # 2. Import the necessary functions from the NLTK library for file summarization:

# from nltk.tokenize import sent_tokenize,word_tokenize
# from nltk.corpus import stopwords
# from nltk.probability import FreqDist
# from heapq import nlargest
# from string import punctuation
# nltk.download('punkt')
# nltk.download('stopwords')
# # 3. Read in the contents of the file as a string:

# with open("sample.txt", "r") as f:
#     text_content = f.read()

# # 4. Tokenize the text into sentences:

# sentences = sent_tokenize(text_content)

# # 5. Tokenize the sentences into words:

# words = word_tokenize(text_content)

# # 6. Identify and remove stopwords from the text:

# stop_words = set(stopwords.words("english"))
# filtered_words = [w for w in words if w not in stop_words]

# # 7. Create a frequency dictionary for each word in the sentence for which we’ll use for scoring:

# freq_dict = FreqDist(filtered_words)

# # 8. Create a score for each sentence based on the words it contains:

# sentence_scores = {}
# for sentence in sentences:
#     sum_words = 0
# for word in nltk.word_tokenize(sentence.lower()):
#         if word in freq_dict.keys():
#             sum_words += freq_dict[word]
# sentence_scores[sentence] = sum_words

# # 9. Find the n largest sentences in terms of their word score:

# important_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)

# # 10. Finally, combine the sentences into a summary string:

# summary = ' '.join(important_sentences)

# print(summary)
