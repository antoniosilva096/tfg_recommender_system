#!/usr/bin/env python3
import argparse
import logging
import re
import csv
from datasets import load_dataset
from nltk import download
from nltk.corpus import stopwords
from tqdm import tqdm

# --- Configuración de logging ---

def setup_logger(level: str):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Nivel de log inválido: {level}")
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=numeric_level
    )

# --- Argumentos de línea de comandos ---

def parse_args():
    parser = argparse.ArgumentParser(
        description="Pipeline de limpieza y extracción de Amazon Reviews"
    )
    parser.add_argument(
        "--output", "-o",
        default="products_clean.csv",
        help="Ruta del CSV de salida"
    )
    parser.add_argument(
        "--target", "-t",
        type=int,
        default=150000,
        help="Número máximo de registros a exportar"
    )
    parser.add_argument(
        "--dataset", "-d",
        default="McAuley-Lab/Amazon-Reviews-2023",
        help="Nombre del dataset en Hugging Face"
    )
    parser.add_argument(
        "--subset", "-s",
        default="raw_meta_Electronics",
        help="Subset del dataset"
    )
    parser.add_argument(
        "--log",
        default="INFO",
        help="Nivel de logging: DEBUG, INFO, WARNING, ERROR"
    )
    return parser.parse_args()

# --- Expresiones regulares y Stopwords ---
RE_NON_ALPHANUM = re.compile(r'[^A-Za-z0-9\.]')
RE_WHITESPACE = re.compile(r'\s+')

# Se descarga en runtime
# download('stopwords')
# STOPWORDS = set(stopwords.words('english'))

# --- Funciones de utilidad ---

def clean_text(text: str, lowercase: bool = True, remove_stopwords: bool = False) -> str:
    """
    Normaliza y limpia texto:
    - strip/trailing
    - lowercase opcional
    - elimina caracteres no alfanuméricos (excepto punto)
    - normaliza espacios
    - elimina stopwords opcionalmente
    """
    if not isinstance(text, str):
        return ""
    text = text.strip().replace("\n", " ")
    if lowercase:
        text = text.lower()
    text = RE_NON_ALPHANUM.sub(' ', text)
    text = RE_WHITESPACE.sub(' ', text)
    if remove_stopwords:
        tokens = [tok for tok in text.split() if tok not in STOPWORDS]
        text = ' '.join(tokens)
    return text.strip()


def get_main_image_url(images: dict) -> str:
    """
    Retorna la primera URL válida en orden de prioridad: hi_res, large, thumb.
    """
    if not images or not isinstance(images, dict):
        return ""
    for key in ('hi_res', 'large', 'thumb'):
        urls = images.get(key, [])
        if isinstance(urls, list):
            for url in urls:
                if url:
                    return url
    return ""


def transform(example: dict) -> dict | None:
    """
    Procesa un registro raw y devuelve un diccionario listo para CSV.
    Devuelve None si faltan campos o hay error en tipos.
    """
    try:
        title = clean_text(example.get('title', ''), lowercase=False)
        categories = example.get('categories', [])
        categories_str = ' > '.join(categories) if isinstance(categories, list) else clean_text(categories)

        price = float(example['price'])
        avg_rating = float(example['average_rating'])
        asin = example.get('parent_asin') or example.get('asin', '')
        image_url = get_main_image_url(example.get('images', {}))

        if not asin or not title or not categories_str:
            raise ValueError("Campos esenciales vacíos")

        return {
            'asin': asin,
            'title': title,
            'categories': categories_str,
            'price': price,
            'average_rating': avg_rating,
            'image_url': image_url
        }

    except KeyError as e:
        logging.warning(f"Campo faltante en registro: {e}")
    except ValueError as e:
        logging.debug(f"Registro filtrado: {e}")
    return None

# --- Función principal ---

def main():
    args = parse_args()
    setup_logger(args.log)
    logging.info("Descargando stopwords de NLTK...")
    download('stopwords')
    global STOPWORDS
    STOPWORDS = set(stopwords.words('english'))

    logging.info(f"Cargando dataset {args.dataset}, subset {args.subset} en streaming...")
    ds = load_dataset(
        args.dataset,
        args.subset,
        split="full",
        streaming=True,
        trust_remote_code=True
    )

    count = 0
    with open(args.output, mode='w', encoding='utf-8', newline='') as f:
        fieldnames = ['asin', 'title', 'categories', 'price', 'average_rating', 'image_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for example in tqdm(ds, total=args.target, desc="Procesando registros"):
            record = transform(example)
            if record:
                writer.writerow(record)
                count += 1
                if count >= args.target:
                    break

    logging.info(f"Exportados {count} registros a {args.output}")

if __name__ == '__main__':
    main()
