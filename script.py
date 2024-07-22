import os
import re
import json

class ArticleLocation:
    AFIP_DAILY_NEWS = 0
    MESSAGES = 1

class Article:
    def __init__(self, article_link, article_title, article_description=None):
        self.article_link = article_link
        self.article_title = article_title
        self.article_description = article_description

    def format(self, where):
        if self.article_description is not None:
            if where == 1:
                return re.sub(r'\[(.*?)\]', r'\1', self.article_text) + " (" + self.article_link + ")"
            elif where == 0:
                return re.sub(r'\[(.*?)\]', r'[\1](' + self.article_link + ')', self.article_text)

    def to_dict(self):
        return {
            "article_link": self.article_link,
            "article_title": self.article_title,
            "article_description": self.article_description
        }

    def __str__(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(cls, data):
        return cls(data['article-link'], data['article_title'], data['article_description'])


class Main:
    def __init__(self):
        self.articles = []
        if not os.path.exists('articles.json'):
            with open('articles.json', 'w') as f:
                json.dumps([], f)
                
        with open('articles.json', 'r') as f:
            try:
                for item in json.load(f):
                    self.articles.append(Article.from_json(item))
            except Exception as err:
                print("An error occurred loading json, defaulting to empty list: " + str(err))

    def add(self, article: Article):
        self.articles.append(article)

    def save(self):
        with open('articles.json', 'w') as f:
            json.dump([article.to_dict() for article in self.articles], f, indent=4)
        

if __name__ == "__main__":
    print("USA Daily News Formatter")
    print(" ")
    Main()
