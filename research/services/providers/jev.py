# from django.conf import settings

# import asyncio

# from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score


# async def main() -> None:
#     async with AsyncTypeSafeClient(
#         api_key=settings.JEV_API_KEY, 
#         model="jev-1.13.0"
#         ) as client:
#         response = await client.system_one(
#             state={"document": "I was charged twice. Please fix this ASAP."},
#             questions={
#                 "billing": Noul(instructions="Is this ticket about billing?"),
#                 "tone": Choice(
#                     instructions="What is the customer's tone?",
#                     criteria={"calm": None, "frustrated": None, "angry": None},
#                 ),
#                 "urgency": Score(
#                     instructions="How urgent is this ticket?",
#                     criteria=["can wait", "this week", "today"],
#                 ),
#             },
#         )

#     print(response.nouls["billing"].noul)
#     print(response.choices["tone"].choice)
#     print(response.scores["urgency"].score)


from typesafe_sdk import AsyncTypeSafeClient


class JEVService:

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def evaluate(
        self,
        state: dict,
        questions: dict,
    ):
        async with AsyncTypeSafeClient(
            api_key=self.api_key,
            model=self.model,
        ) as client:

            response = await client.system_one(
                state=state,
                questions=questions,
            )

        return response