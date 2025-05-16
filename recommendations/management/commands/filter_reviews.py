import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Filtra las reseñas de un CSV original a un subset manejable y lo guarda en un archivo CSV final."

    def add_arguments(self, parser):
        parser.add_argument(
            '--input', 
            type=str, 
            default='data/reviews_electronics.csv', 
            help='Ruta del archivo CSV original con las reseñas.'
        )
        parser.add_argument(
            '--output', 
            type=str, 
            default='data/reviews_subset.csv', 
            help='Ruta del archivo CSV donde se guardará el subset.'
        )
        parser.add_argument(
            '--top_users', 
            type=int, 
            default=100000, 
            help='Número de usuarios más activos a seleccionar.'
        )
        parser.add_argument(
            '--top_items', 
            type=int, 
            default=150000, 
            help='Número de productos más reseñados a seleccionar.'
        )
        parser.add_argument(
            '--sample_size', 
            type=int, 
            default=100000, 
            help='Cantidad de reseñas a muestrear si se supera este número.'
        )

    def handle(self, *args, **options):
        input_path = options.get('input')
        output_path = options.get('output')
        top_users_limit = options.get('top_users')
        top_items_limit = options.get('top_items')
        sample_size = options.get('sample_size')

        # 1) Cargar CSV
        try:
            df = pd.read_csv(input_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al cargar el archivo {input_path}: {e}"))
            return

        self.stdout.write(f"Primeras filas:\n{df.head()}\nDimensiones iniciales: {df.shape}")

        # 2) Filtrar ratings fuera de 1–5
        df = df[df['rating'].between(1, 5)]
        self.stdout.write(f"Después de filtrar ratings inválidos: {df.shape}")

        # 3) Contar reseñas por usuario y por producto (asin)
        user_counts = df['user_id'].value_counts()
        item_counts = df['asin'].value_counts()

        self.stdout.write(f"Cantidad de usuarios únicos: {len(user_counts)}")
        self.stdout.write(f"Cantidad de productos únicos: {len(item_counts)}")

        # 4) Seleccionar los top N usuarios y top M productos
        top_users = user_counts.index[:top_users_limit]
        top_items = item_counts.index[:top_items_limit]

        df_filtered = df[
            df['user_id'].isin(top_users) &
            df['asin'].isin(top_items)
        ]
        self.stdout.write(f"Dimensiones tras filtrar por top usuarios y productos: {df_filtered.shape}")

        # 5) Muestrear reseñas si el dataset filtrado es mayor o igual al tamaño deseado
        if len(df_filtered) >= sample_size:
            df_final = df_filtered.sample(n=sample_size, random_state=42)
            self.stdout.write(f"Se tomó una muestra de {sample_size} reseñas.")
        else:
            df_final = df_filtered
            self.stdout.write(f"El número de reseñas filtradas es menor a {sample_size}. Se utilizarán todas ({df_final.shape[0]} reseñas).")

        self.stdout.write(f"Dimensiones finales del dataset: {df_final.shape}")

        # 6) Guardar el dataset final en un CSV
        try:
            df_final.to_csv(output_path, index=False)
            self.stdout.write(self.style.SUCCESS(f"Subset guardado exitosamente en {output_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al guardar el archivo {output_path}: {e}"))
