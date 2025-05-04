from flask import Flask, render_template, jsonify
import pandas as pd
import plotly
import plotly.express as px
import json
import re
import os
from wordcloud import WordCloud

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Baca data CSV
        df = pd.read_csv('preprocessed_comments.csv')
        # Pastikan kolom 'sentimen' dan 'emosi' ada
        if 'sentimen' not in df.columns:
            raise KeyError("Kolom 'sentimen' tidak ditemukan pada file CSV.")
        if 'emosi' not in df.columns:
            raise KeyError("Kolom 'emosi' tidak ditemukan pada file CSV.")
        # Normalisasi label sentimen & emosi (strip, lower, hapus spasi ganda)
        def norm(x):
            return re.sub(r'\s+', ' ', str(x)).strip().lower()
        df['sentimen'] = df['sentimen'].apply(norm)
        df['emosi'] = df['emosi'].apply(norm)
        # Kategori utama
        kategori_sentimen_utama = ['positif', 'netral', 'negatif']
        kategori_emosi_utama = ['sedih', 'marah', 'takut']
        # Hitung distribusi sentimen
        sentimen_counts = df['sentimen'].value_counts().to_dict()
        sentimen_data = {k: sentimen_counts.get(k, 0) for k in kategori_sentimen_utama}
        # Tambahkan label lain jika ada
        lainnya = 0
        for k in sentimen_counts:
            if k not in kategori_sentimen_utama:
                sentimen_data[k] = sentimen_counts[k]
                lainnya += sentimen_counts[k]
        # Pie chart sentimen
        fig_sentimen = px.pie(values=list(sentimen_data.values()), 
                              names=list(sentimen_data.keys()),
                              title='Distribusi Sentimen Komentar',
                              hole=0.3)
        graphJSON_sentimen = json.dumps(fig_sentimen, cls=plotly.utils.PlotlyJSONEncoder)
        # Statistik
        total_komentar = len(df)
        positif = sentimen_data.get('positif', 0)
        netral = sentimen_data.get('netral', 0)
        negatif = sentimen_data.get('negatif', 0)
        # Emosi
        emosi_counts = df['emosi'].value_counts().to_dict()
        emosi_data = {k: emosi_counts.get(k, 0) for k in kategori_emosi_utama}
        # Tambahkan label lain jika ada
        for k in emosi_counts:
            if k not in kategori_emosi_utama:
                emosi_data[k] = emosi_counts[k]
        sedih = emosi_data.get('sedih', 0)
        marah = emosi_data.get('marah', 0)
        takut = emosi_data.get('takut', 0)
        # Bar chart emosi
        fig_emosi = px.bar(x=list(emosi_data.keys()), y=list(emosi_data.values()), 
                           labels={'x': 'Emosi', 'y': 'Jumlah Komentar'},
                           title='Distribusi Emosi dalam Komentar',
                           color=list(emosi_data.keys()),
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        graphJSON_emosi = json.dumps(fig_emosi, cls=plotly.utils.PlotlyJSONEncoder)
        # Kirim semua komentar untuk wordcloud
        all_comments = ' '.join(df['komentar'].astype(str))
        # Kirim data tabel
        komentar_data = df[['komentar', 'emosi']].to_dict(orient='records')
        error_message = None
        wordcloud_files = [
            {'label': 'Positif', 'file': 'wordcloud_positif.png'},
            {'label': 'Netral', 'file': 'wordcloud_netral.png'},
            {'label': 'Negatif', 'file': 'wordcloud_negatif.png'},
            {'label': 'Marah', 'file': 'wordcloud_marah.png'},
            {'label': 'Takut', 'file': 'wordcloud_takut.png'},
            {'label': 'Sedih', 'file': 'wordcloud_sedih.png'},
        ]
    except Exception as e:
        graphJSON_sentimen = None
        graphJSON_emosi = None
        error_message = str(e)
        total_komentar = positif = netral = negatif = sedih = marah = takut = 0
        all_comments = ''
        komentar_data = []
        wordcloud_files = []
    return render_template(
        'index.html',
        graphJSON_sentimen=graphJSON_sentimen,
        graphJSON_emosi=graphJSON_emosi,
        error_message=error_message,
        total_komentar=total_komentar,
        positif=positif,
        netral=netral,
        negatif=negatif,
        sedih=sedih,
        marah=marah,
        takut=takut,
        wordcloud_url='static/wordcloud.png',
        sumber_links=[
            {
                'nama': 'Detik News',
                'desc': 'Berita Detik',
                'icon': '📰',
                'url': 'https://news.detik.com/berita/d-7882563/kronologi-ribut-debt-collector-berujung-pengeroyokan-depan-polsek-di-riau'
            },
            {
                'nama': 'Kompas',
                'desc': 'Berita Kompas',
                'icon': '📰',
                'url': 'https://regional.kompas.com/read/2025/04/21/080807878/duduk-perkara-pengeroyokan-wanita-di-pekanbaru-persaingan-debt-collector'
            },
            {
                'nama': 'Facebook Kompas',
                'desc': 'Video Facebook',
                'icon': '📺',
                'url': 'https://www.facebook.com/KOMPAScom/videos/wanita-dikeroyok-debt-collector-di-depan-kantor-polisi-berujung-kapolsek-dicopot/1355506062238243/'
            },
            {
                'nama': 'Instagram Bandung Banget',
                'desc': 'Reel Instagram',
                'icon': '📸',
                'url': 'https://www.instagram.com/bandung.banget/reel/DIxrB2IyAy3/'
            },
            {
                'nama': 'YouTube',
                'desc': 'Video YouTube',
                'icon': '▶️',
                'url': 'https://www.youtube.com/watch?v=SFdny8GIQvM'
            },
        ],
        all_comments=all_comments,
        komentar_data=komentar_data,
        wordcloud_files=wordcloud_files
    )

@app.route('/analisis')
def analisis():
    try:
        df = pd.read_csv('preprocessed_comments.csv')
        if 'sentimen' not in df.columns or 'emosi' not in df.columns:
            raise KeyError('Kolom tidak ditemukan.')
        # Normalisasi dan drop NaN/kosong
        def norm(x):
            return re.sub(r'\s+', ' ', str(x)).strip().lower()
        df['sentimen'] = df['sentimen'].astype(str).apply(norm)
        df['emosi'] = df['emosi'].astype(str).apply(norm)
        df = df[(df['sentimen'] != '') & (df['emosi'] != '')]
        if df.empty:
            raise ValueError('Data sentimen/emosi kosong atau tidak valid.')
        # Pie chart sentimen
        sentimen_counts = df['sentimen'].value_counts().to_dict()
        fig_sentimen = px.pie(values=list(sentimen_counts.values()), names=list(sentimen_counts.keys()), title='Distribusi Sentimen', hole=0.3)
        graphJSON_sentimen = json.dumps(fig_sentimen, cls=plotly.utils.PlotlyJSONEncoder)
        # Bar chart emosi
        emosi_counts = df['emosi'].value_counts().to_dict()
        fig_emosi = px.bar(x=list(emosi_counts.keys()), y=list(emosi_counts.values()), labels={'x': 'Emosi', 'y': 'Jumlah Komentar'}, title='Distribusi Emosi', color=list(emosi_counts.keys()), color_discrete_sequence=px.colors.qualitative.Pastel)
        graphJSON_emosi = json.dumps(fig_emosi, cls=plotly.utils.PlotlyJSONEncoder)
        error_message = None
        wordcloud_files = [
            {'label': 'Positif', 'file': 'wordcloud_positif.png'},
            {'label': 'Netral', 'file': 'wordcloud_netral.png'},
            {'label': 'Negatif', 'file': 'wordcloud_negatif.png'},
            {'label': 'Marah', 'file': 'wordcloud_marah.png'},
            {'label': 'Takut', 'file': 'wordcloud_takut.png'},
            {'label': 'Sedih', 'file': 'wordcloud_sedih.png'},
        ]
    except Exception as e:
        graphJSON_sentimen = None
        graphJSON_emosi = None
        error_message = str(e)
        wordcloud_files = []
    return render_template('analisis.html', graphJSON_sentimen=graphJSON_sentimen, graphJSON_emosi=graphJSON_emosi, error_message=error_message, wordcloud_files=wordcloud_files)

@app.route('/daftar-komentar')
def daftar_komentar():
    try:
        df = pd.read_csv('preprocessed_comments.csv')
        komentar_list = df.to_dict(orient='records')
        error_message = None
    except Exception as e:
        komentar_list = []
        error_message = str(e)
    return render_template('daftar_komentar.html', komentar_list=komentar_list, error_message=error_message)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
