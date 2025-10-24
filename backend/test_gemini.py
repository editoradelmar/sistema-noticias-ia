import google.generativeai as genai

# Configura tu API Key
API_KEY = "AIzaSyDDHjIbuMk2CpRMu9SSkbGzwkYhC_A6678"
genai.configure(api_key=API_KEY)

# Puedes listar los modelos disponibles para tu cuenta

models = genai.list_models()
print("Modelos disponibles:")
for m in models:
    print(f"- {m.name}")


# Usa el modelo correcto (ajusta el nombre según lo que imprima arriba)
model_name = "models/gemini-2.5-flash"  # Usa el nombre exacto de la lista
model = genai.GenerativeModel(model_name)

# Prueba una generación simple
response = model.generate_content("Explain how AI works in a few words")
print("\nRespuesta del modelo:")
print(response.text)
