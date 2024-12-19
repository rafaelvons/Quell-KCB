import spacy
from spacy.matcher import Matcher
import re
import pandas as pd
import os
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Path ke direktori proyek
project_dir = r'C:\xampp\htdocs\Quell-KCB\python_api'
csv_path = os.path.join(project_dir, 'laptop_price.csv')

# Membaca data laptop
data = pd.read_csv(csv_path, encoding='latin1')

# Kurs konversi dari Euro ke IDR
EURO_TO_IDR_RATE = 17000  # Misalnya, 1 EUR = 17.000 IDR

def convert_euro_to_idr(price_in_euro):
    """
    Mengonversi harga dari Euro ke IDR.
    """
    return price_in_euro * EURO_TO_IDR_RATE

# Fungsi preprocessing teks
def process_text(text):
    text = text.replace('laptop', '') 
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    text = text.lower()
    factory = StopWordRemoverFactory()
    stop_words = set(factory.get_stop_words())
    stemmer = StemmerFactory().create_stemmer()

    tokens = [stemmer.stem(word) for word in text.split() if word not in stop_words]
    return ' '.join(tokens)

def extract_entities(text):
    """
    Mengekstraksi entitas dari teks deskripsi input pengguna.
    """
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Pola entitas untuk brand, cpu, gpu, ram, price, type (model laptop)
    brands = data['Company'].dropna().unique()
    brand_patterns = [[{"LOWER": brand.lower()}] for brand in brands]
    matcher.add("BRAND", brand_patterns)

    cpu_patterns = [
        [{"LOWER": "intel"}],  # Intel CPU (without specific model)
        [{"LOWER": "amd"}, {"LOWER": "ryzen"}],  # AMD Ryzen CPU
        [{"LOWER": "intel"}, {"IS_DIGIT": True}],  # Intel CPU with model number (e.g., i5, i7)
        [{"LOWER": "amd"}, {"LOWER": "ryzen"}, {"IS_DIGIT": True}],  # AMD Ryzen CPU with model number
    ]
    matcher.add("CPU", cpu_patterns)

    ram_pattern = [[{"IS_DIGIT": True}, {"LOWER": "gb"}, {"LOWER": "ram"}]]
    matcher.add("RAM", ram_pattern)

    price_patterns = [
        [{"LOWER": "harga"}, {"LOWER": "tidak"}, {"LOWER": "lebih"}, {"LOWER": "dari"}, {"IS_DIGIT": True}],
        [{"LOWER": "di"}, {"LOWER": "bawah"}, {"IS_DIGIT": True}],  # Contoh: "di bawah 10 juta"
        [{"LOWER": "antara"}, {"IS_DIGIT": True}, {"LOWER": "sampai"}, {"IS_DIGIT": True}],  # Contoh: "antara 5 juta sampai 15 juta"
    ]
    matcher.add("PRICE", price_patterns)

    # Dynamically create type patterns from the dataset
    types = data['TypeName'].dropna().unique()
    type_patterns = [[{"LOWER": type_.lower()}] for type_ in types]
    matcher.add("TYPE", type_patterns)

    # Create product patterns based on the product names in the dataset
    product_patterns = [[{"LOWER": product.lower()}] for product in data['Product'].dropna().unique()]
    matcher.add("PRODUCT", product_patterns)

    # Pattern for weight in kg (e.g., "1.5kg", "2kg", "1kg")
    weight_pattern = [
        [{"IS_DIGIT": True}, {"LOWER": "kg"}],  # Weight in kg
        [{"IS_DIGIT": True}, {"LOWER": "lbs"}],  # Weight in lbs
    ]
    matcher.add("WEIGHT", weight_pattern)

    entities = {"brand": None, "type": None, "cpu": None, "gpu": None, "ram": None, "price": None, "product": None, "weight": None}

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        if label == "BRAND":
            entities["brand"] = span.text.title()
        elif label == "CPU":
            entities["cpu"] = span.text.upper()  # Capture just the CPU brand like "Intel" or "AMD"
        elif label == "GPU":
            entities["gpu"] = span.text.upper()  # Menambahkan GPU
        elif label == "RAM":
            entities["ram"] = f"{span[0].text}GB"
        elif label == "PRICE":
            # Deteksi pola harga kompleks
            if len(span) == 2 and span[0].text.lower() == "di":
                entities["price"] = int(span[-1].text) * 1000000  # 'di bawah 10 juta' -> 10000000
            elif len(span) == 4 and span[0].text.lower() == "antara":
                entities["price"] = (int(span[1].text) * 1000000, int(span[3].text) * 1000000)  # range -> (5000000, 15000000)
            else:
                entities["price"] = int(span[-1].text) * 1000000  # Example: '5000000' -> 5000000
        elif label == "TYPE":
            entities["type"] = span.text.title()
        elif label == "PRODUCT":
            entities["product"] = span.text.title()  # Capture the product name
        elif label == "WEIGHT":
            entities["weight"] = float(span[0].text)  # Capture weight value as a float (kg or lbs)

    # Log hasil ekstraksi
    print("Entities extracted:", entities)
    return entities

def filter_laptops_by_entities(entities):
    filtered = data.copy()

    # Mengonversi harga dari Euro ke IDR
    filtered['Price_in_IDR'] = filtered['Price_in_euros'].apply(convert_euro_to_idr)

    # Filter berdasarkan entitas yang ditemukan
    if entities.get("brand"):
        filtered = filtered[filtered['Company'].str.contains(entities["brand"], case=False, na=False)]

    if entities.get("type"):
        filtered = filtered[filtered['TypeName'].str.contains(entities["type"], case=False, na=False)]

    if entities.get("cpu"):
        filtered = filtered[filtered['Cpu'].str.contains(entities["cpu"], case=False, na=False)]

    if entities.get("gpu"):
        filtered = filtered[filtered['Gpu'].str.contains(entities["gpu"], case=False, na=False)]

    if entities.get("ram"):
        filtered = filtered[filtered['Ram'].astype(str).str.contains(entities["ram"], na=False)]

    if entities.get("price"):
        # Handling price filtering based on the type of the entity (below, range, or exact price)
        if isinstance(entities["price"], int):  # Single price
            filtered = filtered[filtered['Price_in_IDR'] <= entities["price"]]
        elif isinstance(entities["price"], tuple):  # Price range
            min_price, max_price = entities["price"]
            filtered = filtered[(filtered['Price_in_IDR'] >= min_price) & (filtered['Price_in_IDR'] <= max_price)]

    if entities.get("weight") is not None:  # Only filter by weight if it's provided
        filtered = filtered[filtered['Weight'].astype(float) <= entities["weight"]]

    if entities.get("product"):
        filtered = filtered[filtered['Product'].str.contains(entities["product"], case=False, na=False)]

    return filtered[[ 
        'Product', 'Company', 'TypeName', 'Cpu', 'Ram', 'Memory', 'Price_in_IDR', 'Inches',
        'Gpu', 'ScreenResolution', 'Weight', 'OpSys']]
