import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

# Import fungsi pembantu dari utils.py
from utils import process_text

# Import data pelatihan tambahan
from extra_training_data import training_data

# Unduh NLTK resources jika belum
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Path ke direktori proyek
project_dir = r'C:\xampp\htdocs\Quell-KCB\python_api'  # Sesuaikan dengan path Anda

# Path ke file CSV
csv_path = os.path.join(project_dir, 'laptop_price.csv')

# Membaca CSV
try:
    data = pd.read_csv(csv_path, encoding='latin1')
    print("CSV file successfully read with 'latin1' encoding.")
except UnicodeDecodeError:
    try:
        data = pd.read_csv(csv_path, encoding='cp1252')
        print("CSV file successfully read with 'cp1252' encoding.")
    except UnicodeDecodeError as e:
        print("Failed to read CSV file with both 'latin1' and 'cp1252' encodings.")
        raise e

# Menampilkan nama kolom
print("Nama kolom dalam CSV:", data.columns.tolist())

# Preprocessing kolom Weight untuk menghapus 'kg' dan mengubah menjadi float
data['Heavy'] = pd.to_numeric(
    data['Weight'].str.replace('kg', '', regex=False)
                .str.replace(' Kg', '', regex=False)
                .str.strip(),
    errors='coerce'
)
data = data.dropna(subset=['Heavy'])
print(f"'Heavy' column created. {data.shape[0]} records remaining after dropping NaNs.")

# Menambahkan kolom Price_in_IDR
conversion_rate = 16000  # 1 EUR = 16,000 IDR
data['Price_in_IDR'] = data['Price_in_euros'] * conversion_rate
print("'Price_in_IDR' column added.")

# Membuat label kategori berdasarkan berat
def categorize_weight(weight):
    if weight <= 1.5:
        return 'Ringan'
    elif 1.5 < weight <= 2.5:
        return 'Sedang'
    else:
        return 'Berat'

data['category'] = data['Heavy'].apply(categorize_weight)

# Membuat label prosesor berdasarkan kolom Gpu dan Cpu
def extract_processor(gpu, cpu):
    if 'Nvidia' in gpu or 'Nvidia' in cpu:
        return 'Nvidia'
    elif 'AMD' in gpu or 'AMD' in cpu:
        return 'AMD'
    elif 'Intel' in cpu:
        return 'Intel'
    elif 'Apple' in cpu:
        return 'Apple'
    else:
        return 'Other'

data['processor'] = data.apply(lambda row: extract_processor(row['Gpu'], row['Cpu']), axis=1)

# Membuat label harga berdasarkan Price_in_IDR
def categorize_price(price_idr):
    if price_idr <= 8000000:
        return 'Murah'
    elif 8000000 < price_idr <= 20000000:
        return 'Biasa saja'
    else:
        return 'Mahal'

data['price'] = data['Price_in_IDR'].apply(categorize_price)

# Menambahkan kolom 'company_type' dan 'product'
if 'Company' in data.columns and 'Product' in data.columns:
    data['company_type'] = data['Company']
    data['product'] = data['Product']
else:
    raise ValueError("Kolom 'Company' atau 'Product' tidak ditemukan dalam DataFrame.")

# Menyiapkan data pelatihan dari data tambahan
training_texts = [item[0] for item in training_data]
training_labels = [item[1] for item in training_data]

# Membuat DataFrame dari training_data
df_train_extra = pd.DataFrame(training_labels)
df_train_extra['description'] = training_texts

# Mengambil deskripsi dari data asli
df_train_original = data[['Product', 'category', 'processor', 'price', 'company_type', 'product']].copy()
df_train_original.rename(columns={'Product': 'description'}, inplace=True)

# Menggabungkan data asli dengan data tambahan
df_train = pd.concat([df_train_original, df_train_extra], ignore_index=True)

# Menghapus baris dengan NaN dalam target variabel
df_train = df_train.dropna(subset=['category', 'processor', 'price', 'company_type', 'product'])
X = df_train['description'].apply(process_text)
y = df_train[['category', 'processor', 'price', 'company_type', 'product']]

# Mengurangi High Cardinality pada 'product'
top_n = 100
top_products = y['product'].value_counts().nlargest(top_n).index
y.loc[:, 'product'] = y['product'].apply(lambda x: x if x in top_products else 'Other')

# Membagi data menjadi train dan test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membangun pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2))),
    ('clf', MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')))
])

# Melatih model
print("Training model...")
pipeline.fit(X_train, y_train)
print("Model training completed.")

# Prediksi pada data test
y_pred = pipeline.predict(X_test)

# Evaluasi model
labels = y.columns
for i, label in enumerate(labels):
    print(f"\nClassification Report for '{label}':")
    print(classification_report(y_test[label], y_pred[:, i], zero_division=0))

# Menyimpan model
model_path = os.path.join(project_dir, 'model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print("\nModel berhasil disimpan di 'model.pkl'.")
