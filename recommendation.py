
import pandas as pd

df_mobil_bekas = pd.read_csv('./Kuliah-tugas-besar-bigdata/Data/mobil-bekas-spark.csv')

def get_recomendation(new_input):
    if '#rekomendasi' in new_input:
        hasil = [word for word in new_input.split() if not word.startswith("#")]
        if len(hasil) == 3:

            jenis_mobil = hasil[0]
            kilometer_mobil = int(hasil[1])
            harga = int(hasil[2])

            # Filter data berdasarkan kriteria input pengguna
            filtered_df = df_mobil_bekas[
            (df_mobil_bekas['Jenis_Mobil'].str.lower() == jenis_mobil.lower()) &  
            (df_mobil_bekas['Kilometer_Mobil'] >= kilometer_mobil) &  
            (df_mobil_bekas['Harga'] >= harga)  
            ]
            
            # Urutkan hasil berdasarkan harga dan kilometer mobil
            sorted_df = filtered_df.sort_values(['Harga', 'Kilometer_Mobil'])
            
            # Pilih kolom yang diperlukan dan batasi hasil maksimal 10 baris
            result = sorted_df[['Link_Produk', 'Harga', 'Nama_Produk', 'Kilometer_Mobil', 'tipe_mobil', 'Platform']].head(10)
            
            if len(result) == 0:
                # Jika tidak ada kecocokan, cari mobil yang mendekati berdasarkan harga saja
                filtered_df = df_mobil_bekas[
                    (df_mobil_bekas['Jenis_Mobil'].str.lower() == jenis_mobil.lower()) 
                ]
                sorted_df = filtered_df.sort_values('Harga')  # Urutkan hanya berdasarkan harga
                result = sorted_df[['Link_Produk', 'Harga', 'Nama_Produk', 'Kilometer_Mobil', 'tipe_mobil', 'Platform']].head(10)
            
            # Format hasil menjadi string per baris
            recommendations = ""
            for i, row in enumerate(result.itertuples(), 1):  # Mulai penghitung dari 1
                recommendation = f"{i}. link produk {row.Link_Produk} - harga Rp {row.Harga} - mobil {row.Nama_Produk} - kilometer mobil {row.Kilometer_Mobil} - tipe mobil {row.tipe_mobil} - platform {row.Platform}"
                recommendations += recommendation + "\n"  # Gabungkan rekomendasi dalam satu string, dipisahkan baris baru

            return recommendations

    else:
        return "Pesan yang kamu masukkan tidak sesuai format, sertakan '#rekomendasi'"

