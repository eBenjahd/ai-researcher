import asyncio

from rest_framework.response import Response
from rest_framework.views import APIView

from research.services.factory import build_research_service


class ResearchView(APIView):

    def post(self, request):

        query = request.data.get("query")

        if not query:
            return Response(
                {"error": "query is required"},
                status=400,
            )

        research_service = build_research_service()

        result = asyncio.run(
            research_service.run(query)
        )

        return Response({
            "query": query,
            **result,
        })