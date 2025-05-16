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

recommendations/ # Lógica de entrenamiento y predicción
datasets/ # Datos estructurados y preprocesados
core/ # Módulo principal Django (urls, views, lógica)
templates/ # Plantillas HTML
static/ # Archivos CSS, JS y recursos estáticos


---

## 🚫 Nota importante

Por limitaciones de GitHub, este repositorio **no incluye los modelos entrenados (`.pkl`)**.  
Puedes generarlos localmente ejecutando los scripts de entrenamiento en `recommendations/`.

---

## ▶️ Instrucciones de uso

```bash
# 1. Clona el repositorio
git clone https://github.com/antoniosilva096/tfg_ecommerce_clean.git](https://github.com/antoniosilva096/tfg_recommender_system
cd tfg_ecommerce_clean

# 2. Crea y activa un entorno virtual
python -m venv env
env\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura tu base de datos PostgreSQL y archivo .env

# 5. Aplica migraciones y ejecuta
python manage.py migrate
python manage.py runserver

# 6. Entrena modelos
python manage.py train_models
```


🧪 Metodología aplicada
El desarrollo siguió una metodología híbrida (cascada + ágil), combinando:

Fases bien definidas (análisis, diseño, implementación, pruebas)

Sprints gestionados mediante tableros Kanban

Documentación técnica continua

Validación de requisitos mediante historias de usuario y trazabilidad

Procesos ETL optimizados para trabajar con más de 150.000 productos de Amazon


Antonio Silva Gordillo
Trabajo dirigido por: Dr. Juan Antonio Ortega Ramírez
📧 antoniosilva096@gmail.com
🔗 LinkedIn
🧪 Departamento: Lenguajes y Sistemas Informáticos – ETSII, Universidad de Sevilla
📅 Convocatoria: Junio, curso 2024-2025


inteligencia artificial · eCommerce · sistemas de recomendación · Django · Python · aprendizaje automático · personalización · data-driven development






