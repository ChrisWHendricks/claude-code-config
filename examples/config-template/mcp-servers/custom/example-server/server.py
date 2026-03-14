#!/usr/bin/env python3
"""
Example custom MCP server implementation.

This demonstrates how to create a simple MCP server for your organization.
"""

import json
import sys
from typing import Any


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    """Handle an MCP request."""
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "example_tool",
                    "description": "An example tool from your organization",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "A message to process",
                            }
                        },
                        "required": ["message"],
                    },
                }
            ]
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "example_tool":
            message = arguments.get("message", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Example server processed: {message}",
                    }
                ]
            }

    return {"error": "Method not supported"}


def main():
    """Main server loop - reads JSON-RPC requests from stdin."""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {"error": str(e)}
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()
