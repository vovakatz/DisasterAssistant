from typing import Optional

from app import services
from app.models.assistant_response import AssistantResponse
from app.models.chat_response import ChatResponse
from app.store.assistant import AssistantStore


class AssistantService:
    async def get_assistant_response(self, question: str, thread_id: Optional[str]):
        if not thread_id:
            thread = services.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )
            thread_id = thread.id
        else:
            services.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=question
            )

        run = services.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id="asst_sh3cHFY9moqlcjt8wvW5ZqMa",

        )

        if run.status == 'completed':
            messages = services.client.beta.threads.messages.list(
                thread_id=thread_id
            )
            print(messages)
            chat = ChatResponse.from_dict(messages.model_dump_json())

            await AssistantStore().save_q_and_a(thread_id, question,chat.data[0].content[0].text.value)

            return AssistantResponse(
                thread_id=thread_id,
                message=chat.data[0].content[0].text.value
            )
        else:
            print(run.status)
            return AssistantResponse(
                thread_id=thread_id,
                message="System experienced an issue, please try again."
            )
