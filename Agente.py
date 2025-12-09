import ollama
from Buscar_papers import buscar_papers, formato_resultado, resumen_paper
from Generar_citas import generar_cita_apa,generar_bibliografia_apa,mostrar_cita_paper


instructions = """
Eres una asistente experto en investigación académica y científica.

Tus funciones principales son:
1. Ayudar a buscar y analizar literatura científica.
2. Generar citas bibliográficas en formato APA e IEEE.
3. Resumir papers y artículos académicos.
4. Ayudar a estructurar proyectos de investigación.
5. Explicar conceptos científicos de forma clara.

Formato de citas:
* APA: Apellido, A.A. (Año). Título del artículo. Nombre de la revista, volumen(número), páginas. https://doi.org/xxx
* IEEE: [1] A. A. Apellido, "Título del artículo," Nombre de la revista, vol. X, no. Y, pp. ZZ-ZZ, Mes Año.

Sé preciso, académico y siempre proporciona fuentes cuando sea posible.
"""

historial = []
ultimo_resultado = None   # ← Inicializado correctamente


# ---------------------------------------------------------
# FUNCIÓN DE CHAT
# ---------------------------------------------------------
def chat(mensaje_user, contexto_extra=None):
    mensajes = [
        {'role': 'system', 'content': instructions}
    ]

    # Si hay contexto adicional (resumen de papers), se agrega
    if contexto_extra:
        mensajes.append({'role': 'system', 'content': contexto_extra})

    mensajes.extend(historial)

    mensajes.append({
        'role': 'user',
        'content': mensaje_user
    })

    try:
        print("\n🤖 Pensando...", end="", flush=True)
        respuesta = ollama.chat(
            model='gemma3:1b',
            messages=mensajes,
            stream=False
        )
        texto_respuesta = respuesta['message']['content']

        # Guardamos correctamente en historial
        historial.append({'role': 'user', 'content': mensaje_user})
        historial.append({'role': 'assistant', 'content': texto_respuesta})

        return texto_respuesta

    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------
while True:
    mensaje = input("👤 Tu: ").strip()

    if mensaje.lower() == 'salir':
        print("\n 👋 Nos pillamos")
        break

    if mensaje.lower() == 'limpiar':
        historial.clear()
        ultimo_resultado = None
        print('\n 🫓 Conversación reiniciada\n')
        continue

    if not mensaje:
        continue

    # -----------------------------------------------------
    # OPCIÓN DE BÚSQUEDA
    # -----------------------------------------------------
    if mensaje.lower().startswith('buscar'):
        termino = mensaje[7:].strip()

        if not termino:
            print("⚠ Debes especificar qué buscar. Ejemplo: buscar IA\n")
            continue

        resultados = buscar_papers(termino, max_resultados=5)

        if resultados:
            ultimo_resultado = resultados

            # Resumen general
            resumen = resumen_paper(resultados)

            pregunta = f"Analiza los siguientes papers encontrados sobre '{termino}' y genera un resumen académico."
            respuesta = chat(pregunta, contexto_extra=resumen)

            print("\n📄 **Análisis de los papers encontrados:**")
            print(respuesta)
            print("-" * 60)

        else:
            print("❌ No se encontró ningún paper.\n")
    if mensaje.lower().startswith('cita apa:'):
        if not ultimo_resultado:
            print("Se debe de buscar primero")
            continue
        try:
            numero=int(mensaje[10:].strip())
            if 1<=numero<=len(ultimo_resultado):
                paper=ultimo_resultado[numero-1]
                print(mostrar_cita_paper(paper,numero,formato='apa'))
            else:
                print(f"Resultado invalido")
        except ValueError:
            print("error al citar")
            continue
    if mensaje.lower()=='bibliografia apa':
        if not ultimo_resultado:
            print("Se debe de bsucar primero")
            continue
        bibliografia=generar_bibliografia_apa(ultimo_resultado)
        print(f"\n{bibliografia}\n")
        continue
    else:

     contexto = None
    if (
        ultimo_resultado and 
        any(palabra in mensaje.lower() for palabra in 
            ['paper', 'artículo', 'cita', 'referencia', 'estos', 'resultados'])
    ):
        contexto = resumen_paper(ultimo_resultado)

    # -----------------------------------------------------
    # RESPUESTA NORMAL DEL CHAT
    # -----------------------------------------------------
    respuesta = chat(mensaje, contexto_extra=contexto)
    print(f"\n🤖 Agent:\n{respuesta}\n")
    print("-" * 60)
