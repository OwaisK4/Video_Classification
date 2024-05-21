# import nltk
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

text = """
Charlie, you don't understand. Heaven never listens. They didn't listen to me.
They won't listen to you. You don't know that. I do. 
You didn't know that when I tried this all before. My dreams were too hard to defend.
And in the end, I won't lose it all again. Now you're the only thing worth fighting for.
More than anything. More than anything. I shall turn the door you more than anything.
Dad, I don't need you to protect me from this. I just don't want you to be crushed by them like I was.
Dad, when I was young, I didn't really know you at all. I always felt so small.
I heard your stories and I wasn't thronged. It tells about your lofty dreams.
I've listened breathlessly. Imagining it could be me. So in the end, it's the view I had of you.
That show me dreams can be worth fighting for. More than anything. More than anything.
I need to save my people.
"""

tokens = word_tokenize(text)
tagged_words = pos_tag(tokens)
named_entities = ne_chunk(tagged_words)

print(named_entities)