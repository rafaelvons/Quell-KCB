from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Fungsi untuk mengonversi harga dari INR ke IDR
def convert_inr_to_idr(price_inr, exchange_rate=200):
    return price_inr * exchange_rate

# Membaca data laptop dari file CSV
df = pd.read_csv('C:/xampp/htdocs/web-quell/python_api/laptop_data.csv')

# Mengonversi harga dari INR ke IDR
df['Price_IDR'] = df['Price'].apply(lambda x: convert_inr_to_idr(x))

# Filter berdasarkan kategori (contoh: programming, gaming, designing)
def filter_laptops(category, max_price=None, min_ram=None, min_cpu=None, min_gpu=None, min_screen=None, max_weight=None):
    filtered_df = df

    # Filter berdasarkan kategori
    if category == 'programming':
        filtered_df = filtered_df[(filtered_df['Ram'] >= 8) & (filtered_df['Cpu'].str.contains('Intel Core i5|Intel Core i7'))]
    elif category == 'gaming':
        filtered_df = filtered_df[filtered_df['Gpu'].str.contains('NVIDIA|AMD')]
    elif category == 'designing':
        filtered_df = filtered_df[(filtered_df['ScreenResolution'].str.contains('1920x1080|2560x1440|3840x2160')) & (filtered_df['Gpu'].str.contains('NVIDIA|AMD'))]
    
    # Filter harga maksimal
    if max_price:
        filtered_df = filtered_df[filtered_df['Price_IDR'] <= max_price]
    
    # Filter RAM minimum
    if min_ram:
        filtered_df = filtered_df[filtered_df['Ram'] >= min_ram]
    
    # Filter CPU minimum
    if min_cpu:
        filtered_df = filtered_df[filtered_df['Cpu'].str.contains(min_cpu)]
    
    # Filter GPU minimum
    if min_gpu:
        filtered_df = filtered_df[filtered_df['Gpu'].str.contains(min_gpu)]
    
    # Filter ukuran layar
    if min_screen:
        filtered_df = filtered_df[filtered_df['Inches'] >= min_screen]
    
    # Filter bobot maksimum
    if max_weight:
        filtered_df = filtered_df[filtered_df['Weight'] <= max_weight]

    return filtered_df

@app.route('/')
def home():
    return render_template('index.html')

from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Fungsi untuk mengonversi harga dari INR ke IDR
def convert_inr_to_idr(price_inr, exchange_rate=200):
    return price_inr * exchange_rate

# Membaca data laptop dari file CSV
df = pd.read_csv('C:/xampp/htdocs/web-quell/python_api/laptop_data.csv')

# Mengonversi harga dari INR ke IDR
df['Price_IDR'] = df['Price'].apply(lambda x: convert_inr_to_idr(x))

# Filter berdasarkan kategori (contoh: programming, gaming, designing)
def filter_laptops(category, max_price=None, min_ram=None, min_cpu=None, min_gpu=None, min_screen=None, max_weight=None):
    filtered_df = df

    # Debug: Ukuran awal DataFrame
    print(f"Initial DataFrame size: {len(filtered_df)}")

    # Filter berdasarkan kategori
    if category == 'programming':
        filtered_df = filtered_df[(filtered_df['Ram'] >= 8) & (filtered_df['Cpu'].str.contains('Intel Core i5|Intel Core i7'))]
        print(f"Filtered programming laptops: {len(filtered_df)}")
    elif category == 'gaming':
        filtered_df['Gpu'] = filtered_df['Gpu'].fillna('')  # Mengisi nilai kosong
        filtered_df = filtered_df[filtered_df['Gpu'].str.contains('NVIDIA|AMD', na=False)]
        print(f"Filtered gaming laptops: {len(filtered_df)}")
    elif category == 'designing':
        filtered_df = filtered_df[(filtered_df['ScreenResolution'].str.contains('1920x1080|2560x1440|3840x2160')) & (filtered_df['Gpu'].str.contains('NVIDIA|AMD', na=False))]
        print(f"Filtered designing laptops: {len(filtered_df)}")

    # Filter harga maksimal
    if max_price:
        filtered_df = filtered_df[filtered_df['Price_IDR'] <= max_price]
        print(f"After max_price filter ({max_price}): {len(filtered_df)}")
    
    # Filter lainnya...
    return filtered_df
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    description = data.get('description', '').lower()

    try:
        # Menentukan kategori berdasarkan deskripsi pengguna
        if 'programming' in description:
            category = 'programming'
        elif 'gaming' in description:
            category = 'gaming'
        elif 'designing' in description:
            category = 'designing'
        else:
            category = 'general'

        # Filter berdasarkan harga
        max_price = None
        if 'under 10 million' in description or 'dibawah 10 juta' in description:
            max_price = 10000000
        elif 'under 5 million' in description or 'dibawah 5 juta' in description:
            max_price = 5000000
        elif 'under 20 million' in description or 'dibawah 20 juta' in description:
            max_price = 20000000
        elif 'over 10 million' in description or 'di atas 10 juta' in description:
            max_price = 10000001  # Untuk harga di atas 10 juta
        elif 'over 20 million' in description or 'di atas 20 juta' in description:
            max_price = 20000001  # Untuk harga di atas 20 juta

        # Filter RAM minimum
        min_ram = None
        if '8gb ram' in description:
            min_ram = 8
        elif '16gb ram' in description:
            min_ram = 16

        # Filter CPU minimum
        min_cpu = None
        if 'i5' in description:
            min_cpu = 'Intel Core i5'
        elif 'i7' in description:
            min_cpu = 'Intel Core i7'
        
        # Filter GPU minimum
        min_gpu = None
        if 'nvidia' in description:
            min_gpu = 'NVIDIA'
        elif 'amd' in description:
            min_gpu = 'AMD'

        # Filter ukuran layar minimum
        min_screen = None
        if '14 inch' in description:
            min_screen = 14
        elif '15 inch' in description:
            min_screen = 15

        # Filter bobot maksimum
        max_weight = None
        if 'under 2 kg' in description or 'dibawah 2 kg' in description:
            max_weight = 2

        # Mendapatkan hasil filter
        laptops = filter_laptops(category, max_price, min_ram, min_cpu, min_gpu, min_screen, max_weight)

        # Mengonversi hasil filter menjadi format dictionary
        laptops = laptops.to_dict(orient='records')

        return jsonify(laptops)

    except Exception as e:
        import traceback
        # Pastikan ada indentasi untuk kode berikut
        error_traceback = traceback.format_exc()  # Menangani exception dengan benar
        print(f"Error Traceback: {error_traceback}")
        return jsonify({'error': 'Terjadi kesalahan saat mendapatkan rekomendasi.'})



if __name__ == '__main__':
    app.run(debug=True)



