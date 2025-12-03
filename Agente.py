import ollama
from Buscar_papers import burcar_papers,formato_resultado,resumen_paper

instructions = """
Eres una asistente experto en investigacion academica y cientifica.

Tus funcione principales son:
1. Ayudar a buscar y analizar literatura cientifica 
2. Generar citas bibliograficas en formato APA e IEEE
3. Resumit papers y articulos academicos
4. Ayudar a estructurar proyectosde investigacion
5.Explicar conceptos cientificos de forma clara

Formato de citas:
*APA: Apellido,A.A.(Año).Titulo del articulo. Nombre de la revista, volumen(numero), paginas. https://doi.org/xxx
*IEEE: [1] A.A. Apellido, "Titulo del articulo," Nombre de la revista, vol. X,no. Y,pp. ZZ-ZZ, Mes Año

Se preciso, academico y siempre proporciona fuentes cuando sea posible.

"""

historial=[]

def chat(mensaje_user):
    mensajes=[
        {
            'role':'system',
            'content':instructions
        }
    ]
    mensajes.extend(historial)
    mensajes.append({
        'role':'user',
        'content':mensaje_user
    })
    try:
        respuesta=ollama.chat(
            model='gemma3:1b',
            messages=mensajes,
            stream=False
        )
        texto_respuesta=respuesta['message']['content']
        historial.append({
            'role':'user',
            'content':mensaje_user
        })
        historial.append({
            'role':'assistant',
            'content':mensaje_user
        })
        return texto_respuesta
    except Exception as e:
        return f"Error:{e}"
    
while True:
    mensaje=input("👤 Tu: ").strip()
    if mensaje.lower()=='salir':
        print("\n 👋 Nos pillamos")
        break
    if mensaje.lower()=='limpiar':
        historial.clear()
        print('\n 🫓 Conversacion reiniciada')
    if not mensaje:
        continue
    if mensaje.lower().startswith('buscar'):
        termino=mensaje[7:].strip()
        if not termino:
            print("Se debe especificar que buscar ej: IA ")
            continue
        resultados=burcar_papers(termino,max_resultados=5)
        if resultados:
            ultimo_resultado=resultados
            resumen=resumen_paper(resultados)
            pregunta=f"Buscare de '{termino}'"
            respuesta=chat(pregunta,contexto_extra=resumen)
            print(f"\nAnalisis:{respuesta}")
            print("-"*60)
        else:
            print("No se encontro nada")

    else:
        contexto:None
        if ultimo_resultado and any(palabra in mensaje.lower()for palabra in ['paper','articulo','cita','referencia','estos','resultados']):
         contexto=resumen_paper(ultimo_resultado)            

    respuesta=chat(mensaje)
    print(f"\n 🤖 Agent:\n{respuesta}\n")
    print("-"*60)    