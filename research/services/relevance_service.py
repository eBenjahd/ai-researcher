import json

from .searxng import SearXNGService
from .clear_search import clean_search_results


class RelevanceService:

    def __init__(self, provider):
        self.provider = provider
        self.search_service = SearXNGService()

    def select_relevant_documents(self, query):

        # 1. Buscar en SearXNG
        search_data = self.search_service.search(query)

        # 2. Limpiar resultados
        cleaned_data = clean_search_results(search_data)

        problem_to_solve = cleaned_data["problem_to_solve"]
        results = cleaned_data["results"]

        # 3. Convertir los documentos a texto para el prompt
        documents = json.dumps(
            results,
            ensure_ascii=False,
        )

        prompt = f"""
Eres un clasificador de relevancia para un pipeline de investigación automatizado.
No eres un asistente conversacional: tu única salida válida es un objeto JSON.

PREGUNTA DE INVESTIGACIÓN:
{problem_to_solve}

DOCUMENTOS (id, title, url):
{documents}

TAREA:
Selecciona hasta 5 ids de documentos cuyo title y url indiquen relación directa y
específica con la pregunta de investigación. Evalúa solo title y url — nunca asumas
contenido no mostrado.

CRITERIOS DE SELECCIÓN (en orden de peso):
1. El title contiene términos o conceptos que responden directamente la pregunta.
2. El title es específico al tema, no genérico ni ambiguo.
3. Coincidencia temporal/geográfica si la pregunta la exige explícitamente. Si el
   title o la url contienen una fecha o año explícito, verifica que esté dentro del
   rango temporal de la pregunta y priorízalo si coincide.
4. El domain sugiere naturaleza técnica/académica/institucional/periodística
   (señal secundaria, nunca decisiva por sí sola).

PRIORIDAD DE TIPO DE FUENTE (cuando el title/url lo permita inferir):
1. Fuente primaria/oficial: bancos centrales, organismos internacionales, reguladores,
   instituciones directamente involucradas en el tema.
2. Análisis institucional/think tank especializado.
3. Trabajo académico (tesis, TFG, paper universitario) — válido pero secundario.
4. Prensa/blog especializado.

EXCLUYE si:
- El title es ambiguo y no permite inferir relación con el tema.
- El title sugiere contenido promocional, listado genérico o clickbait sin relación clara.
- No hay suficiente información para juzgar relevancia (en ese caso, no lo incluyas).

No determines si la información del documento es verdadera.
No determines si la fuente es confiable en términos absolutos.
No inventes información sobre el contenido de los documentos.
No descartes una fuente únicamente porque no conozcas el sitio web.
No utilices conocimiento externo para asumir qué contiene un documento más allá de
lo que title y url permiten inferir razonablemente.

Si menos de 5 documentos cumplen los criterios, devuelve solo los que cumplen.
Si ninguno cumple, devuelve un array vacío.

FORMATO DE SALIDA (obligatorio):
Devuelve un objeto JSON con la forma {{"ids": [...]}}.
Conteniendo únicamente los ids seleccionados como enteros.
Sin texto adicional, sin explicación, sin markdown.
Máximo 5 ids.
"""

        response = self.provider.generate_response(
            prompt=prompt,
        )

        relevance_data = json.loads(response)

        ids = relevance_data["ids"]

        results_matched = self.match_relevant_documents(
            ids=ids,
            results=results,
        )

        return results_matched

    
    def match_relevant_documents(self, ids, results):

        results_matched = []

        for index in ids:

            result = next(
                (
                    result
                    for result in results
                    if result["id"] == index
                ),
                None,
            )

            if result:
                results_matched.append(result)

        return results_matched