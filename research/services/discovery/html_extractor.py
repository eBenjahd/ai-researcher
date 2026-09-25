import trafilatura


class HTMLExtractionService:

    def extract(self, html: str) -> str:
        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
        )

        if not text:
            raise ValueError(
                "Could not extract content from HTML"
            )

        return text