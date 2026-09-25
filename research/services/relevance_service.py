from typesafe_sdk import Noul

from .searxng import SearXNGService
from .clear_search import clean_search_results


class RelevanceService:

    def __init__(self, provider):
        self.provider = provider
        self.search_service = SearXNGService()

    async def select_relevant_documents(self, query):

        # 1. Buscar en SearXNG
        search_data = await self.search_service.search(query)

        # 2. Limpiar resultados
        cleaned_data = clean_search_results(search_data)

        problem_to_solve = cleaned_data["problem_to_solve"]
        results = cleaned_data["results"]

        # 3. Crear una pregunta JEV por documento
        questions = {
            f"document_{result['id']}": Noul(
                instructions=(
                    "You are an expert research assistant specializing "
                    "in preliminary source filtering.\n"

                    "Evaluate how relevant this document could be to the "
                    "research question, using ONLY the research question, "
                    "document title, and URL.\n"

                    "Consider how directly the document appears to address "
                    "the research question, how specific its topic is, and "
                    "whether it could reasonably provide useful information "
                    "for the investigation.\n"

                    "Use this relevance scale:\n"
                    "0.90 - 1.00: Extremely relevant. The document appears "
                    "to directly address the specific research question.\n\n"
                    "0.70 - 0.89: Highly relevant. The document clearly "
                    "relates to the question but may be broader or more indirect.\n\n"
                    "0.40 - 0.69: Potentially relevant. The document relates "
                    "to the general topic but may provide limited value.\n\n"
                    "0.00 - 0.39: Low relevance. The document appears "
                    "unlikely to contribute useful information.\n\n"
                    "Do not evaluate source quality, credibility, or truthfulness. "
                    "Do not favor or penalize a source because of its type, "
                    "authority, or publication platform.\n\n"
                    "Do not penalize information for supporting, challenging, "
                    "or contradicting a possible conclusion. Different "
                    "perspectives can all be relevant to the investigation.\n\n"
                    "Do not assume information about the document's actual "
                    "contents beyond what can reasonably be inferred from "
                    "its title and URL."
                )
            )
            for result in results
        }

        # 4. Enviar pregunta + documentos a JEV
        response = await self.provider.evaluate(
            state={
                "research_question": problem_to_solve,
                "documents": results,
            },
            questions=questions,
        )

        # 5. Extraer scores
        scores = {
            int(key.removeprefix("document_")): answer.noul
            for key, answer in response.nouls.items()
        }

        # # TEMPORAL: mostrar scores
        # print("\nJEV SCORES:")
        # for document_id, score in sorted(
        #     scores.items(),
        #     key=lambda item: item[1],
        #     reverse=True,
        # ):
        #     document = next(
        #         (
        #             result
        #             for result in results
        #             if result["id"] == document_id
        #         ),
        #         None,
        #     )

        #     if document:
        #         print(
        #             f"{score:.3f} | "
        #             f"{document['title']}"
        #         )

        # 6. Ordenar documentos por relevancia
        ranked_ids = [
            document_id
            for document_id, score in sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]

        # 7. Quedarnos con los 5 primeros
        top_ids = ranked_ids[:5]

        # 8. Recuperar los documentos originales
        return self.match_relevant_documents(
            ids=top_ids,
            results=results,
        )

    def match_relevant_documents(self, ids, results):

        results_by_id = {
            result["id"]: result
            for result in results
        }

        return [
            results_by_id[index]
            for index in ids
            if index in results_by_id
        ]