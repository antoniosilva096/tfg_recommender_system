# 🛍️ TFG – Plataforma de Algoritmos de Recomendación para eCommerce

Este repositorio contiene el Trabajo de Fin de Grado de **Antonio Silva**, titulado  
**“Integración de la Inteligencia Artificial en el E-Commerce para la mejora de la experiencia de usuario y optimización de ventas”**,  
defendido en la **Universidad de Sevilla**, en el **Grado en Ingeniería Informática – Tecnologías Informáticas**.

---

## 🎯 Objetivo del proyecto

Diseñar e implementar una plataforma web interactiva donde se puedan cargar productos reales y aplicar distintos algoritmos de recomendación con inteligencia artificial, permitiendo:

- Comparar su rendimiento en términos de personalización y ventas
- Evaluar métricas de eficacia como precisión, diversidad o cobertura
- Entender cómo funcionan técnicas modernas usadas por Amazon, Netflix o Spotify
- Adaptar estas técnicas a un entorno accesible, sin necesidad de grandes recursos

---

## ⚙️ Tecnologías utilizadas

- **Backend:** Python · Django  
- **Frontend:** Bootstrap · HTML5 · JavaScript  
- **Base de Datos:** PostgreSQL  
- **Librerías IA:** Scikit-learn · Surprise · Pandas · NumPy  
- **Visualización:** Matplotlib · Plotly  
- **Datos reales:** [Amazon Reviews 2023 – HuggingFace](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023)

---

## 🧠 Algoritmos de recomendación implementados

- Filtros colaborativos:
  - `SVD`, `SVD++` (factorización de matrices)
  - `KNN` (basado en usuarios y productos)
- Recomendación basada en contenido
- Popularidad
- Modelos híbridos (combinación de señales)
- Arquitectura preparada para añadir modelos avanzados (deep learning, autoencoders, redes neuronales)

---

## 📊 Características destacadas

- Visualización de resultados por modelo y usuario
- Dashboard con métricas automáticas (precision, recall, F1-score, etc.)
- Comparación entre algoritmos integrados
- Carga de datasets externos (proceso ETL incluido)
- Interfaz ligera, pensada para investigación y pruebas rápidas
- Adaptación a hardware convencional (sin GPU)
- Enfoque pedagógico y extensible para futuros desarrollos o spin-offs

---

## 📁 Estructura del proyecto

```text
tfg_ecommerce_clean/
├── recommendations/     # Lógica de entrenamiento y predicción
│   ├── train_svd.py
│   ├── train_knn.py
│   └── ...
├── datasets/            # Datos estructurados y preprocesados
│   └── productos_amazon.csv
├── core/                # Módulo principal de Django (vistas, urls, lógica)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── templates/           # Plantillas HTML de la interfaz web
│   └── base.html
├── static/              # Archivos estáticos: CSS, JS, imágenes
│   ├── css/
│   ├── js/
│   └── img/
├── manage.py
├── .env.example         # Plantilla para variables de entorno
├── requirements.txt     # Dependencias del proyecto
└── README.md
```
---

## 🚫 Nota importante

Por limitaciones de GitHub, este repositorio **no incluye los modelos entrenados (`.pkl`)**.  
Puedes generarlos localmente ejecutando los scripts de entrenamiento en `recommendations/`.

---

## ▶️ Instrucciones de uso

```
# 1. Clona el repositorio
git clone https://github.com/antoniosilva096/tfg_ecommerce_clean.git](https://github.com/antoniosilva096/tfg_recommender_system
cd tfg_ecommerce_clean

# 2. Crea y activa un entorno virtual
python -m venv env
env\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura tu base de datos PostgreSQL en Settings

# 5. Aplica migraciones y ejecuta
python manage.py migrate
python manage.py runserver

```

🧾 Cargar datos reales (productos, reseñas, usuarios)

1️⃣ Cargar productos
```
# Desde HuggingFace (150k productos de la categoria Electronics)
cd data/

py procesar_dataset_productos.py #Genera el CSV procesado de productos Aplicando un proceso ETL

python manage.py load_products #Carga en la bbdd los productos desde el csv limpio generado en el paso anterior

```
⚠️ Solo se cargan productos válidos con título, precio, imagen y categorías.


2️⃣ Importar reseñas y usuarios
```
python manage.py filter_reviews #Procesa el dataset en bruto de reviews extraido del repositorio de hugging face para la categoria electronics
python manage.py load_amazon_reviews #Carga y vincula a usuarios en la bbdd las reviews procesadas y limpias

```

4️⃣ Limpiar para DEMO o Entrenamiento
```
# Limpieza real → mantiene solo 5000 productos con más calidad
python manage.py clean_for_demo
```
💡 Filtra productos con imagen, categoría, +5 reviews, y buen rating
---

📈 Entrenamiento de modelos
```
python manage.py train_models
```

## 🧪 Metodología aplicada

El desarrollo del proyecto siguió una **metodología híbrida** que combina lo mejor del enfoque tradicional en cascada con elementos ágiles como **Scrum** y **Kanban**, permitiendo una gestión eficaz y adaptable.

### 🔧 Enfoque adoptado:

- 📌 Fases claramente definidas: *Análisis, diseño, implementación y pruebas*
- 🗂️ Gestión por sprints con tableros **Kanban**
- 📝 Documentación técnica continua y estructurada
- ✅ Validación mediante **historias de usuario**, requisitos funcionales y trazabilidad
- 📦 Proceso **ETL optimizado** para manejar +150.000 productos reales del dataset de Amazon

Este enfoque permitió entregar una solución funcional, escalable y bien documentada, combinando buenas prácticas de ingeniería con flexibilidad en la ejecución.

---

## 📚 Autor

**👨‍💻 Antonio Silva Gordillo**  
Trabajo dirigido por: **Dr. Juan Antonio Ortega Ramírez**

- 📧 [antoniosilva096@gmail.com](mailto:antoniosilva096@gmail.com)  
- 🔗 [LinkedIn](https://www.linkedin.com/in/antoniosilva096/)  
- 🏛️ Departamento de **Lenguajes y Sistemas Informáticos**, ETSII – Universidad de Sevilla  
- 📅 Convocatoria: **Junio, curso 2024–2025**

---


inteligencia artificial · eCommerce · sistemas de recomendación · Django · Python · aprendizaje automático · personalización · data-driven development






