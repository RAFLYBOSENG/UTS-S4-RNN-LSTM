import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Set style
sns.set_theme()
sns.set_palette("husl")

# Baca data
print("Membaca data...")
csv_path = os.path.join(APP_DIR, 'preprocessed_comments.csv')
df = pd.read_csv(csv_path)

# Fungsi untuk membuat wordcloud
def create_wordcloud(text, title, filename, color='black'):
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        max_words=100,
        max_font_size=150,
        color_func=lambda *args, **kwargs: color,
        random_state=42
    ).generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, pad=20, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Wordcloud untuk setiap kategori
categories = {
    'positif': {'color': 'green'},
    'netral': {'color': 'blue'},
    'marah': {'color': 'red'},
    'negatif': {'color': 'orange'},
    'takut': {'color': 'purple'},
    'sedih': {'color': 'gray'}
}

for category, settings in categories.items():
    # Filter komentar berdasarkan kategori
    if category in ['positif', 'netral', 'negatif']:
        filtered_comments = df[df['sentimen'] == category]['komentar']
    else:
        filtered_comments = df[df['emosi'] == category]['komentar']
    
    # Gabungkan komentar
    text = ' '.join(filtered_comments.astype(str))
    
    # Buat wordcloud
    create_wordcloud(
        text,
        f'Wordcloud Komentar {category.capitalize()}',
        f'wordcloud_{category}.png',
        settings['color']
    )

print("Visualisasi wordcloud selesai! File gambar telah disimpan.")

# Tampilkan statistik
print("\nStatistik Komentar:")
for category in categories:
    if category in ['positif', 'netral', 'negatif']:
        count = len(df[df['sentimen'] == category])
    else:
        count = len(df[df['emosi'] == category])
    print(f"{category.capitalize()}: {count} komentar")