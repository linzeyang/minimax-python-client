# MiniMax Python Client

[![PyPI version](https://img.shields.io/pypi/v/minimax-client.svg)](https://pypi.org/project/minimax-client/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![License](https://img.shields.io/pypi/l/minimax-client.svg)](https://pypi.org/project/minimax-client)
[![python-versions](https://img.shields.io/pypi/pyversions/minimax-client.svg)](https://pypi.org/project/minimax-client)
[![Main Workflow](https://github.com/linzeyang/minimax-python-client/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/linzeyang/minimax-python-client/actions/workflows/main.yml)

An (unofficial) python native client for easy interaction with [MiniMax Open Platform](https://www.minimaxi.com/platform)

The current implementation includes the following official APIs offered by MiniMax:
- ChatCompletion v2
- Embeddings
- File
- Finetune
- Assistants

## Prerequisites
- Python >= 3.8
- pip (or any other tool that does the same job)
- Internet connection
- An API KEY acquired from [MiniMax Open Platform](https://www.minimaxi.com/user-center/basic-information/interface-key)

## Quick Start

### 1. Install the package

```bash
pip install minimax-client
```

### 2. Import the package and invoke the client

#### 2.1 Sync call

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "1 + 1 equals: ",
        }
    ]
)


print(response.choices[0].message.content)
```

#### 2.2 Sync call with streaming

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is the term GPT short for?",
        }
    ],
    stream=True,
)


for chunk in stream:
    print(chunk.choices[0].delta.content if chunk.choices[0].delta else "", end="")
```

#### 2.3 Sync call with tools, stream enabled

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


stream = client.chat.completions.create(
    model="abab5.5-chat",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant",
        },
        {
            "role": "user",
            "content": "What's the weather like in Log Angeles right now?",
        },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_function_2936815621",
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "arguments": '{"location": "LogAngeles"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "call_function_2936815621",
            "content": "LogAngeles / Sunny / 51°F / Wind: East 5 mph",
        },
    ],
    stream=True,
    tool_choice="auto",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Retrieve the current weather of given location",
                "parameters": '{"type": "object", "properties": {"location": {"type": "string", "description": "Name of a city, eg. Paris, London"}}, "required": ["location"]}',
            },
        }
    ],
)

for chunk in stream:
    print(chunk.choices[0].delta.content if chunk.choices[0].delta else "", end="")

# It's currently sunny in Log Angeles, with a temperature of 51°F and wind from the east at 5 mph.
```


#### 2.4 Async call

```python
import asyncio

from minimax_client import AsyncMiniMax


async def demo():
    client = AsyncMiniMax(api_key="<YOUR_API_KEY>")

    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "1 + 1 equals: ",
            }
        ]
    )

    print(response.choices[0].message.content)


asyncio.run(demo())
```

#### 2.5 Async call with streaming

```python
import asyncio

from minimax_client import AsyncMiniMax


async def demo():
    client = AsyncMiniMax(api_key="<YOUR_API_KEY>")

    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "What is the term GPT short for?",
            }
        ],
        stream=True,
    )

    async for chunk in stream:
        print(chunk.choices[0].delta.content if chunk.choices[0].delta else "", end="")


asyncio.run(demo())
```

#### 2.6 Sync call for embeddings

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


response = client.embeddings.create(
    input=["Hello world!", "Nice to meet you!"],
    target="db",
)

print(response.vectors[0][:10])
print(response.vectors[1][:10])
```

#### 2.7 Async call for embeddings

```python
import asyncio

from minimax_client import AsyncMiniMax


async def demo():
    client = AsyncMiniMax(api_key="<YOUR_API_KEY>")

    response = await client.embeddings.create(
        input=["Hello async world!", "Nice to meet you async!"],
        target="query",
    )

    print(response.vectors[0][:10])
    print(response.vectors[1][:10])


asyncio.run(demo())
```

#### 2.8 Sync call for files

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


resp = client.files.create(filepath="sample.txt", purpose="retrieval")
print(resp.file.file_id)

resp = client.files.list(purpose="retrieval")
print(resp.files[0].file_id)

resp = client.files.retrieve(file_id=resp.files[0].file_id)
print(resp.file.bytes)

resp = client.files.delete(file_id=resp.file.file_id)
print(resp.file_id)
```

#### 2.9 Async call for files

```python
import asyncio

from minimax_client import AsyncMiniMax


async def demo():
    client = AsyncMiniMax(api_key="<YOUR_API_KEY>")

    resp = await client.files.create(filepath="sample.txt", purpose="retrieval")
    print(resp.file.file_id)

    resp = await client.files.list(purpose="retrieval")
    print(resp.files[0].file_id)

    resp = await client.files.retrieve(file_id=resp.files[0].file_id)
    print(resp.file.bytes)

    resp = await client.files.delete(file_id=resp.file.file_id)
    print(resp.file_id)

asyncio.run(demo())
```

#### 2.10 Sync call for files

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")

resp = client.fine_tuning.jobs.create(
    model="abab5.5s-chat-240123", training_file=..., suffix="test"
)
print(resp.id)
print(resp.fine_tuned_model)

resp = client.fine_tuning.jobs.list(limit=5)
print(resp.job_list[0])

resp = client.model.list()
print(resp.model_list[0])

resp = client.model.retrieve(model="ft:abab5.5s-chat-240123_XXXXXXXXXXXXX:test")
print(resp.model.id)
```

#### 2.11 Sync call for assistants

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")

resp = client.assistants.create(model="abab5.5s-chat-240123")

client.assistants.update(
    assistant_id=resp.id,
    model="abab5.5s-chat-240123",
    name="test-assistant",
    instructions="You are a helpful assistant.",
)

client.assistants.retrieve(assistant_id=resp.id)

client.assistants.list(limit=5)

client.assistants.delete(assistant_id=resp.id)
```
