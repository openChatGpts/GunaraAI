from django.test import TestCase

# Create your tests here.
def add_title_to_content(content):
    words = content.split()
    title_words = [word.capitalize() for word in words]
    title = " ".join(title_words)
    return title

content = '''
Natural language processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans through natural language. It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like language.

One of the tasks in NLP is text summarization, where the goal is to generate a concise and coherent summary of a given text. In this example, we'll use an extractive summarization approach to generate a title for a given article.

Extractive summarization involves selecting important sentences or phrases from the original text and combining them to create a summary. We'll use the NLTK library in Python to tokenize the text, remove stop words, calculate word frequencies, and select the most important sentences.

Let's g
'''
title_content = add_title_to_content(content)
print(title_content)