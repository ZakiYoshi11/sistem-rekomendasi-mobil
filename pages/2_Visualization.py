import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

# Load DataFrame untuk WordCloud
df_chatbot = pd.read_csv('./Kuliah-tugas-besar-bigdata/Data/prep-data-chatbot.csv')

# Load DataFrame untuk Mobil Bekas
df_mobil_bekas = pd.read_csv('./Kuliah-tugas-besar-bigdata/Data/mobil-bekas-spark.csv')

# Judul Aplikasi
st.title("Dashboard Visualisasi")

# Sidebar untuk memilih visualisasi
menu = st.sidebar.selectbox(
    "Pilih Visualisasi",
    ["Chatbot Visualization", "Visualization Mobil Bekas"]
)

# Visualisasi Word Cloud Chatbot
if menu == "Chatbot Visualization":
    # Filter data berdasarkan kategori yang dipilih
    kategori = st.selectbox("Pilih Kategori", df_chatbot['tag'].unique())
    filtered_data = df_chatbot[df_chatbot['tag'] == kategori]

    # Menggabungkan teks dalam kategori yang dipilih
    all_text_list = filtered_data['prep'].tolist()
    all_words = []
    for sublist in all_text_list:
        words = [word.strip() for word in sublist.split(',')]
        cleaned_words = [re.sub(r'[^\w\s]', '', word).lower() for word in words if word.strip()]
        all_words.extend(cleaned_words)

    # Menghitung frekuensi kata
    word_counts = Counter(all_words)

    # Membuat WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

    # Menampilkan WordCloud
    st.subheader(f"Word Cloud untuk Kategori: {kategori}")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Kemunculan Kata Kategori: {kategori}")
    st.pyplot(fig)

# Visualisasi Data Mobil Bekas
elif menu == "Visualization Mobil Bekas":
    st.subheader("Visualisasi Data Mobil Bekas")

    # Rata-rata harga mobil berdasarkan jenis
    avg_price_per_brand = df_mobil_bekas.groupby('Jenis_Mobil')['Harga'].mean().sort_values(ascending=False)
    plt.figure(figsize=(15, 6))
    plt.bar(avg_price_per_brand.index, avg_price_per_brand.values)
    plt.xticks(rotation=45, ha='right')
    plt.title('Harga Mobil Bekas Berdasarkan Jenis Mobil')
    plt.xlabel('Jenis Mobil')
    plt.ylabel('Harga Rata-rata (Rp)')
    plt.tight_layout()
    st.pyplot(plt)

    # Harga vs Kilometer
    st.subheader("Harga Mobil vs Kilometer Berdasarkan Jenis Mobil")
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df_mobil_bekas, x='Kilometer_Mobil', y='Harga', hue='Jenis_Mobil', alpha=0.6)
    plt.title('Harga Mobil vs Kilometer Berdasarkan Jenis Mobil')
    plt.xlabel('Kilometer')
    plt.ylabel('Harga (Rp)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Distribusi Tahun Produksi
    st.subheader("Distribusi Tahun Produksi Mobil Bekas")
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df_mobil_bekas, x='Tahun', bins=30)
    plt.title('Distribusi Tahun Produksi Mobil Bekas')
    plt.xlabel('Tahun Produksi')
    plt.ylabel('Jumlah Mobil')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(plt)
