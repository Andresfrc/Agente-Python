from scholarly import scholarly
import time

def buscar_papers(consulta,max_resultados=5):
    """
    Buscar papers academicos en Google Scholar
    Args:
        consulta(str):Termino de busqueda (ej:"machine learning")
        max_resultado (int): Numero maximo de resultados a devolver
        
    Returns:
        list: Lista de diccionarios con informacion de papers    


    """
    print(f"\n🔍 Buscando")
    print(f"⌛⌛⌛ puede tardar")

    resultados=[]
    try:
        busqueda=scholarly.search_pubs(consulta)
        for i in range(max_resultados):
            try:
                paper=next(busqueda)
                info_paper={
                    'titulo':paper.get('bib',{}).get('title','sin titulo'),
                    'autores':paper.get('bib',{}).get('author','sin autor'),
                    'año':paper.get('bib',{}).get('pub_year','sin año'),
                    'revista':paper.get('bib',{}).get('veneu','sin nombre'),
                    'resumen':paper.get('bib',{}).get('abstract','sin resumen'),
                    'citacion':paper.get('citaciones',0),
                    'url':paper.get('pub_url') or paper.get('eprint_url','sin url')
                }
                resultados.append(info_paper)
                time.sleep
            except StopIteration:
                print(f"\n Solo se obtuvieron {len(resultados)}")
                break
            except Exception as e:
                print(f"Error {e}")
                continue
        print(f"\n Busqueda completa")
        return resultados
    except Exception as e:
        print(f"Error {e}")
        return[]
    
def formato_resultado(paper,numero):
    """
    Formatea la informacion de un paper para mostrarla mas bonito
    Args:
        paper (dict): Diccionario con la info del paper
        numero(int):Numero del paper en la lista
    
    Returns:
        str: Texto formateado 
    """    

    if isinstance(paper['autores'], list):
        autores=','.join(paper['autores'])
    else:
        autores=paper['autores']

    resumen=paper['resumen']
    if len(resumen)>300:
        resumen=resumen[:300]+"..."
    texto=f"""
    {'-'*60}
    PAPER #{numero}
    {'-'*60}
    TITULO: {paper['titulo']}
    {'-'*60}
    Autor: {autores}
    {'-'*60}
    Revista: {paper['citacion']}
    {'-'*60}
    Cita {paper['citacion']}
    {'-'}*60
    Resumen:
    {resumen}
    {'-'*60}
    URL:{paper['url']}
    """    
    return texto

def mostrar_resultados(resultados):
    """
    Muestra todos los resultados de forma organizada
    Args:
        resultados(list):Lista de papers encontrados
    """
    if not resultados:
        print("No hay resultados")
        return
    print(f"Resultados")
    for i, paper in enumerate(resultados,1):
        print(formato_resultado(paper,i))

def resumen_paper(resultados):
    """
    Crea un resumen texto de todos los papers para pasarlo al siguiente agente
    Args:
        resultados(list): Lista de papers
    Returns:
        str: Resumen de texto en todos los papers
    """
    if not resultados:
        return "No se encuentran papers"
    resumen_texto=f"Se encuentran{len(resultados)}"
    for i,paper in enumerate(resultados,1):
        autores=','.join(paper['autores']) if isinstance(paper['autores'],list)else (paper['autores'],list)
        resumen_texto+=f"""
        Paper {i}:
        -Titulo:{paper['titulo']}
        -Autores:{paper['autores']}
        -Año:{paper['año']}
        -Revista:{paper['revista']}
        -Citas:{paper['citacion']}
        -Resumen:{paper['resumen'][:200]}
        -Url:{paper['url']}
        """
        return resumen_texto