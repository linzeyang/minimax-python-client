"""test_client.py"""

import os
import unittest

import httpx

from minimax_client import AsyncMiniMax, MiniMax
from minimax_client.interfaces.chat_completion import AsyncChat


class TestMiniMax(unittest.TestCase):
    """Unit tests for the MiniMax client."""

    def test_init_without_api_key(self):
        """Test that an error is raised if no API key is provided."""
        with self.assertRaises(ValueError):
            if os.environ.get("MINIMAX_API_KEY"):
                del os.environ["MINIMAX_API_KEY"]

            MiniMax()

    def test_init_with_valid_api_key(self):
        """Test that the client is initialized with a valid API key."""
        client = MiniMax(api_key="valid_api_key")
        self.assertEqual(client.api_key, "valid_api_key")

    def test_del_closes_http_client(self):
        """Test that the __del__ method closes the HTTP client."""
        client = MiniMax(api_key="valid_api_key")
        client.http_client.close()
        self.assertTrue(client.http_client.is_closed)


class TestAsyncMiniMax(unittest.IsolatedAsyncioTestCase):
    """Unit tests for AsyncMiniMax"""

    async def test_constructor(self) -> None:
        """Test that the AsyncMiniMax constructor sets the API key and creates
        an AsyncChat instance with the HTTP client"""
        api_key = "test_api_key"
        async_minimax = AsyncMiniMax(api_key=api_key)
        self.assertEqual(async_minimax.api_key, api_key)
        self.assertIsInstance(async_minimax.chat, AsyncChat)
        self.assertIs(async_minimax.chat.completions.client, async_minimax.http_client)

    async def test_del_closes_http_client(self) -> None:
        """Test that the __del__ method closes the HTTP client"""
        async_minimax = AsyncMiniMax(api_key="valid_api_key")
        await async_minimax.http_client.aclose()
        self.assertTrue(async_minimax.http_client.is_closed)

    async def test_get_http_client(self) -> None:
        """Test that _get_http_client returns a new AsyncClient instance with
        the base URL and authorization header set"""
        api_key = "test_api_key"
        async_minimax = AsyncMiniMax(api_key=api_key)
        http_client = async_minimax._get_http_client()
        self.assertIsInstance(http_client, httpx.AsyncClient)
        self.assertEqual(http_client.headers["Authorization"], f"Bearer {api_key}")
