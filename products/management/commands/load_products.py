import logging
import re
import nltk
import pandas as pd
from django.core.management.base import BaseCommand
from datasets import load_dataset
from products.models import Product

# Descargar stopwords (solo la primera vez)
nltk.download('stopwords')

# Pre-compilación de expresiones regulares (puedes incluir limpieza si lo deseas)
RE_NON_ALPHANUM = re.compile(r'[^A-Za-z0-9.]')
RE_WHITESPACE = re.compile(r'\s+')

def text_cleaning(text: str) -> str:
    """
    Limpia el texto: pasa a minúsculas, elimina caracteres no alfanuméricos (excepto el punto) y normaliza espacios.
    """
    text = text.strip().lower()
    text = RE_NON_ALPHANUM.sub(' ', text)
    text = RE_WHITESPACE.sub(' ', text)
    return text.strip()

class Command(BaseCommand):
    help = "Carga productos de Electronics desde el dataset de Amazon Reviews 2023 (muestra limpia de 150k registros)"

    def handle(self, *args, **kwargs):
        logging.info("Cargando dataset...")
        # Cargar el dataset desde Hugging Face
        dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", "raw_meta_Electronics", split="full", trust_remote_code=True)
        df = pd.DataFrame(dataset)

        logging.info("Total de registros en el dataset: %d", len(df))

        # Filtrar registros con campos imprescindibles: title, categories y price
        df = df.dropna(subset=['title', 'categories', 'price'])
        logging.info("Registros tras filtrar NaNs en campos requeridos: %d", len(df))

        # Convertir la columna 'price' a numérico
        df['price_numeric'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price_numeric'].notna()]
        logging.info("Registros con precio convertible: %d", len(df))

        # Seleccionar una muestra de 150k registros (si hay suficientes)
        if len(df) >= 150000:
            df_sample = df.head(150000)
        else:
            logging.warning("El dataset tiene menos de 150k registros; se usarán %d registros", len(df))
            df_sample = df.copy()

        logging.info("Muestra final: %d registros", len(df_sample))

        # Recorrer el DataFrame y guardar en la BD
        for _, row in df_sample.iterrows():
            asin = row['parent_asin'] if 'parent_asin' in row else None
            title = text_cleaning(row['title'])
            # Si 'categories' es una lista, unir los elementos con comas
            if isinstance(row['categories'], list):
                categories = ", ".join(row['categories'])
            else:
                categories = text_cleaning(row['categories'])
            price = float(row['price_numeric'])
            average_rating = float(row['average_rating']) if 'average_rating' in row and pd.notnull(row['average_rating']) else None

            # Guardar o actualizar el producto
            product, created = Product.objects.get_or_create(
                asin=asin,
                defaults={
                    'title': title,
                    'categories': categories,
                    'price': price,
                    'average_rating': average_rating,
                }
            )
            if created:
                self.stdout.write(f"Producto creado: {title}")
        self.stdout.write("Carga de productos completada.")
