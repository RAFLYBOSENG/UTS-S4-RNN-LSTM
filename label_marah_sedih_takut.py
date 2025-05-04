import pandas as pd
from label import get_sentiment

# Baca data
df = pd.read_csv('preprocessed_comments.csv')

def emosi(text):
    text_lower = text.lower()
    
    # Kata kunci untuk setiap emosi (perluas sesuai kebutuhan)
    marah_keywords = ['marah', 'kesal', 'geram', 'murka', 'emosi', 'jengkel', 'benci', 'gondok', 'sebel', 
                     'mangkel', 'gak suka', 'ga suka', 'tidak suka', 'kzl', 'kezel', 'anjir', 'anjg',
                     'bangsat', 'bngst', 'sialan', 'kampret', '🤬', '😠', '😡']
                     
    sedih_keywords = ['sedih', 'kecewa', 'pilu', 'duka', 'nestapa', 'merana', 'galau', 'putus asa',
                      'depresi', 'menyesal', 'kehilangan', 'ditinggal', 'baper', 'nangis', 'menangis',
                      'terluka', 'sakit hati', '😢', '😭', '😔', '😞', '😥']
                      
    takut_keywords = ['takut', 'khawatir', 'cemas', 'was-was', 'ngeri', 'panik', 'trauma', 'paranoid',
                      'gelisah', 'gemetar', 'ketakutan', 'merinding', 'horor', 'horror', 'teror',
                      'mengancam', 'bahaya', '😨', '😰', '😱', '😳']
    
    # Cek kata kunci dengan bobot
    marah_count = sum(1 for word in marah_keywords if word in text_lower)
    sedih_count = sum(1 for word in sedih_keywords if word in text_lower)
    takut_count = sum(1 for word in takut_keywords if word in text_lower)
    
    counts = {
        'Marah': marah_count,
        'Sedih': sedih_count,
        'Takut': takut_count
    }
    
    max_emotion = max(counts.items(), key=lambda x: x[1])
    
    # Jika ada emosi spesifik, ambil itu
    if max_emotion[1] > 0:
        return max_emotion[0]
    # Jika tidak ada, fallback ke 'Netral' daripada 'Lainnya'
    return 'Netral'

# Terapkan label emosi
df['emosi'] = df['komentar'].apply(emosi)

# Simpan ke file baru
df.to_csv('preprocessed_comments_emosi.csv', index=False, encoding='utf-8')

print("Labeling emosi selesai! Cek file preprocessed_comments_emosi.csv")

# Tampilkan distribusi label emosi
print("\nDistribusi Label Emosi:")
print(df['emosi'].value_counts())