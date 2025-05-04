from textblob import TextBlob
import re
import logging
import pandas as pd

def contains_emoji(text):
    return any(char in text for char in ['😊', '👍', '💪', '🙏', '😂', '🤣', '😅', '😭', '😢', '😔', '😩', '😫', '😤', '😡', '❤️', '💕', '💗', '💓', '💝', '💖', '♥️', '😍', '🥰', '😘', '😗', '😚', '😙', '🤗', '🫂', '👏', '🙌', '✌️', '🤝', '🫡', '🤩', '🌟', '⭐', '✨', '💫', '🎉', '🎊', '😨', '😰', '😱', '😳', '😖', '😞', '😟', '😕', '😣', '😖', '😫', '😩', '😤', '😠', '😡', '🤬'])

def count_repeated_chars(text):
    patterns = ['w+k+w+k+', 'h+a+h+a+', 'h+e+h+e+', 'h+i+h+i+', 'x+i+x+i+']
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text.lower()))
    return count

def count_punctuation(text):
    return len(re.findall(r'[!?]{2,}|\.{2,}', text))

def get_emoji_sentiment(text):
    positive_emoji = ['😊', '👍', '💪', '🙏', '❤️', '💕', '😍', '🥰', '🤗']
    negative_emoji = ['😢', '😭', '😔', '😩', '😫', '😤', '😡']
    neutral_emoji = ['😂', '🤣', '😅']
    
    pos_count = sum(text.count(emoji) for emoji in positive_emoji)
    neg_count = sum(text.count(emoji) for emoji in negative_emoji)
    
    if pos_count > 0:
        return 1
    elif neg_count > 0:
        return -1
    return 0

def get_sentiment(text):
    if not text or not isinstance(text, str):
        return 'Netral'
        
    text = text.strip()
    if len(text) == 0:
        return 'Netral'
        
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    text_lower = text.lower()
    
    positive_keywords = [
        'semangat', 'support', 'dukung', 'bagus', 'menarik', 'keren', 'mantap', 
        'hebat', 'wow', 'amazing', 'setuju', 'smangat', 'semangatt', 'mantapp',
        'salut', 'kagum', 'inspirasi', 'inspiratif', 'keren', 'mantul', 'joss',
        'sukses', 'berhasil', 'hebat', 'luar biasa', 'kece', 'top', 'the best',
        'alhamdulillah', 'syukur', 'senang', 'bahagia', 'gembira', 'asik',
        'suka', 'happy', 'seneng', 'asyik', 'alhamdulilah'
    ]

    has_positive = any(keyword in text_lower for keyword in positive_keywords)
    has_emoji = contains_emoji(text)
    
    repeated_chars = count_repeated_chars(text)
    excessive_punctuation = count_punctuation(text)
    word_count = len(text_lower.split())
    
    emoji_score = get_emoji_sentiment(text) * 0.3
    keyword_score = 0
    
    if has_positive:
        keyword_score = 0.4
    
    polarity_score = polarity * 0.3
    
    final_score = emoji_score + keyword_score + polarity_score
    
    if final_score > 0.2:
        return 'Positif'
    elif final_score < -0.2:
        return 'Negatif'
    else:
        return 'Netral'

# df = pd.read_csv("komentar_sentimen6.csv")

data = [
    {"komentar": "Saya sangat senang dengan hasil ini.", "sentimen": "Positif"},
    {"komentar": "Biasa saja.", "sentimen": "Netral"},
    {"komentar": "Pelayanannya buruk sekali.", "sentimen": "Negatif"},
]

# df = pd.read_csv("komentar_dengan_sentimen121.csv")
# df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
# df.to_csv("komentar_dengan_sentimen.csv121", index=False)