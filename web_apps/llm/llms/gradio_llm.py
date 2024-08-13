from typing import List, Optional, Any
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage

from langchain_core.outputs import (
    ChatGeneration,
    ChatResult,
)
from gradio_client import Client

gradio_url = "https://s5k.cn/api/v1/studio/ZhipuAI/glm-4-9b-chat-vllm/gradio/"


class GradioChatModel(BaseChatModel):
    url = gradio_url
    messages = []

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        generations = []
        client = Client(self.url)
        result = client.predict(
            str(messages[-1].content),
            self.messages,
            api_name="/predict_1"
        )
        self.messages = result[1]
        gen = ChatGeneration(
            message=AIMessage(content=self.messages[-1][-1])
        )
        generations.append(gen)
        return ChatResult(
            generations=generations,
            llm_output={},
        )

    @property
    def _llm_type(self):
        return "gradio_llm"


if __name__ == '__main__':
    llm = GradioChatModel(url=gradio_url)
    res = llm.stream('nihao')
    print(res)
    for i in res:
        print(i)
    res = llm.stream('我刚才说了啥')
    print(res)
    for i in res:
        print(i)
    print(llm.invoke('1+1=?'))