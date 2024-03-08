# MiniMax Python Client

[![PyPI version](https://img.shields.io/pypi/v/minimax-client.svg)](https://pypi.org/project/minimax-client/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)
[![image](https://img.shields.io/pypi/l/minimax-client.svg)](https://pypi.org/project/minimax-client)
[![image](https://img.shields.io/pypi/pyversions/minimax-client.svg)](https://pypi.org/project/minimax-client)

An (unofficial) python native client for easy interaction with [MiniMax Open Platform](https://api.minimax.chat/)

The current implementation includes the following official API from MiniMax:
- ChatCompletion v2

## Prerequisites
- Python >= 3.8
- pip
- An API KEY acquired from [MiniMax Open Platform](https://api.minimax.chat/user-center/basic-information/interface-key)

## Quick Start

### Install the package

```bash
pip install minimax-client
```

### Import the package and invoke the client

#### Sync call

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

#### Sync call with streaming

```python
from minimax_client import MiniMax


client = MiniMax(api_key="<YOUR_API_KEY>")


stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "1 + 1 equals: ",
        }
    ],
    stream=True,
)


for chunk in stream:
    print(chunk.choices[0].delta.content if chunk.choices[0].delta else "", end="")
```

#### Async call

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

#### Async call with streaming

```python
import asyncio

from minimax_client import AsyncMiniMax


async def demo():
    client = AsyncMiniMax(api_key="<YOUR_API_KEY>")

    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "1 + 1 equals: ",
            }
        ],
        stream=True,
    )

    async for chunk in stream:
        print(chunk.choices[0].delta.content if chunk.choices[0].delta else "", end="")


asyncio.run(demo())
```
