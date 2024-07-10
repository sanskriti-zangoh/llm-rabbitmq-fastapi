from langchain_community.llms.ollama import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

model="llama3"
max_tokens=1024
temperature=0
system="You are a very romantic poet."
messages=["Hello, nice weather today huh?"]

ollama = Ollama(
    model=model,
    temperature=temperature,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    system=system
)

ollama.stream(model=model, max_tokens=max_tokens, temperature=temperature, system=system, input=messages)
