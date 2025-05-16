import pandas as pd
import pickle

# Imports de Surprise
from surprise import Dataset, Reader, accuracy, SVD, KNNBasic, SVDpp
from surprise.model_selection import train_test_split

def load_data(csv_path):
    """
    Carga el CSV final (reviews_subset.csv) y lo retorna como DataFrame.
    Verifica que las columnas user_id, asin, rating existan.
    """
    df = pd.read_csv(csv_path)
    required_cols = {"user_id", "asin", "rating"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"El CSV debe tener al menos {required_cols}. Columnas encontradas: {df.columns}")
    return df

def create_surprise_dataset(df):
    """
    Crea el dataset para Surprise utilizando únicamente las columnas user_id, asin y rating.
    Se utiliza un Reader para definir el rango de ratings.
    """
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'asin', 'rating']], reader)
    return data

def split_data(data, test_size=0.2):
    """
    Divide el dataset en trainset y testset según la proporción deseada.
    """
    trainset, testset = train_test_split(data, test_size=test_size, random_state=42)
    return trainset, testset

def train_svd(trainset):
    """
    Entrena el modelo SVD con 50 factores latentes.
    """
    algo = SVD(
        n_factors=50,     # Aumentar a 100, 150, 200...
        n_epochs=20,      # Por defecto 20, pero puedes subirlo a 50+ si tienes tiempo
        lr_all=0.005,     # Tasa de aprendizaje
        reg_all=0.02,     # Regularización
        random_state=42
    )
    algo.fit(trainset)
    return algo

def train_knn(trainset):
    """
    Entrena el modelo KNN (item-based) utilizando similitud coseno.
    """
    sim_options = {
        'name': 'cosine', 
        'user_based': False
    }
    algo = KNNBasic(
        k=40,             # Número de vecinos
        min_k=1,
        sim_options=sim_options
    )
    algo.fit(trainset)
    return algo

def train_svdpp(trainset):
    """
    Entrena el modelo SVD++.
    """
    algo = SVDpp(
        n_factors=100, 
        n_epochs=30,
        random_state=42
        )
    algo.fit(trainset)
    return algo

def evaluate_model(algo, testset):
    """
    Evalúa el modelo utilizando RMSE.
    """
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=False)
    return rmse

def save_model(algo, filename):
    """
    Guarda el modelo entrenado en un archivo pickle.
    """
    with open(filename, "wb") as f:
        pickle.dump(algo, f)
    print(f"Modelo guardado en {filename}")

def main():
    # 1) Cargar CSV
    df = load_data("../data/reviews_subset.csv")
    print(f"Reseñas cargadas: {df.shape[0]} filas")

    # 2) Crear dataset para Surprise
    data = create_surprise_dataset(df)

    # 3) Dividir en train/test
    trainset, testset = split_data(data, test_size=0.2)
    print(f"Entrenamiento: {trainset.n_ratings} interacciones. Test: {len(testset)}")

    # Diccionario de modelos a entrenar: clave = nombre, valor = (función de entrenamiento, nombre de archivo)
    modelos = {
        "SVD": (train_svd, "model_svd.pkl"),
        "KNN (item-based)": (train_knn, "model_knn.pkl"),
        "SVD++": (train_svdpp, "model_svdpp.pkl")
    }

    # Entrenar, evaluar y guardar cada modelo
    for nombre, (train_func, filename) in modelos.items():
        print(f"\nEntrenando {nombre}...")
        modelo = train_func(trainset)
        rmse = evaluate_model(modelo, testset)
        print(f"RMSE({nombre}): {rmse:.4f}")
        save_model(modelo, filename)

    print("\nProceso de entrenamiento y guardado completado.")

if __name__ == "__main__":
    main()
