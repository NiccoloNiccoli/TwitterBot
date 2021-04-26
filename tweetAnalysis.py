import re


class TweetCleaner:
    def skim(self, query):
        #delete characters
        query = re.sub(r'http\S+', '', query)  # removes links
        query = re.sub(r'@\S*', '', query)  # removes tags
        query = re.sub(r'#\S*$','',query)#removes hashtags at the end?
        query = re.sub(r'^#\S*', '', query)  # removes hashtags at the beginning?
        query = re.sub(r'#','',query)#removes hashtag character
        query = re.sub(r"^\s+", "", query)  # removes spaces at the start
        query = re.sub(r"\s+$", "", query)  # removes spaces at the end

        # enhance the formatting
        query = re.sub(r'\.', '. ', query)
        return query
