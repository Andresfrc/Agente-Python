def generar_cita_apa(paper):
    """
    Genera una cita en formato APA 7
    Args:
        paper(dict): Diccionario con la informacion del paper
            -autores:str o list

            -año:str
            -titulo:str
            -revista:str
            -volumen:str
            -numero:str
            -paginas:str
            -doi:str
            -utl:str
    Returns:
        str:Cita formateada en APA 7 
    """
    if isinstance(paper['autores'],list):
        if len(paper['autores'])==1:
            autores_formato=paper['autores'][0]
        elif len(paper['autores'])==2:
            autores_formato= f"{paper}['autores'][0] & {paper['autores'][1]}"
        elif len(paper['autores'])<=20:
            autores_formato=','.join(paper['autores'][:-1])+f",&{paper['autores'][-1]}"
        else:
            autores_formato=','.join(paper['autores'][:19])+",..."+{paper['autores']}
    else:
        autores_formato=paper['autores']  
    año=paper.get('año','s.f.')
    if año=='Sin año':
        año='s.f.'
    titulo=paper['titulo']
    revista=paper.get('revista','')
    cita=f"{autores_formato}({año}).{titulo}."
    if revista and revista !='Sin nombre':
        cita+=f"{revista}"

    url=paper.get('url','')
    if url and url!='Sin url':
        cita+=f"{url}"
    return cita

def generar_bibliografia_apa(lista_papers):
    
    """
    Generar una bibiliografia completa en formato APA
    Args:
        listar_papers (list):Lista de diccionarios con papers
    Returns:
        str:Bibliografia completa formateada

    """
    if not lista_papers:
        return "No hay papers"
    bibliografia="-"*60+"\n"
    for paper in lista_papers:
        cita=generar_cita_apa(paper)
        bibliografia+=f"{cita}\n\n"

    bibliografia="-"*60+"\n"
    return bibliografia

def mostrar_cita_paper(paper,numero,formato='apa'):
    """
    Muestra una cita individual formateada
    Args:
        paper (dict):Informacion de paper
        numero (int):Numero del paper en lista
        formato (str):'apa'
    Returns:
        str:Cita formateada para mostrar
    """

    formato=formato.lower()
    if formato=='apa':
        cita=generar_cita_apa(paper)
        titulo_formato='APA 7'
    else:
        return "Formato no valido"
    resultado=f"""
{'-*60'}
Cita#{numero}(Formato{titulo_formato})
{cita}
{'-'*60}
"""
    return resultado