# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **a2a-samples** repository - a collection of code samples demonstrating the Agent2Agent (A2A) Protocol, a standardized JSON-RPC based protocol for AI agents to communicate with each other. The project is maintained by Google but is not an officially supported product.

## Repository Structure

```
samples/
├── python/         # Python agent implementations (primary language)
├── java/           # Java/Spring Boot agents
├── go/             # Go client/server implementations
├── javascript/     # JavaScript/TypeScript agents
└── tools/          # Development tools and utilities

demo/              # Mesop-based web UI for testing agents
├── server/        # Demo server implementation
└── static/        # Frontend assets
```

## Technology Stack

- **Python**: 3.12+ with `uv` package manager
- **Java**: Spring Boot with Maven
- **JavaScript/TypeScript**: Node.js with pnpm
- **Go**: Standard library + Gemini AI SDK

## Common Commands

### Python Development
```bash
# Install dependencies
cd samples/python/<agent-name>
uv sync

# Run an agent
uv run agent_<name>.py

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

### Demo UI
```bash
cd demo
uv sync
uv run demo
# Access at http://localhost:32168
```

### Java Development
```bash
cd samples/java/<agent-name>
mvn clean install
mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=5003"
```

### JavaScript Development
```bash
cd samples/javascript/<agent-name>
pnpm install
pnpm run dev  # or pnpm start
```

## Architecture & Key Concepts

### Agent Types
1. **Task Agents**: Perform specific tasks (weather, calculator, etc.)
2. **Host Agents**: Route requests to appropriate task agents
3. **Multi-Agent Systems**: Complex orchestrations using frameworks like CrewAI, LangGraph

### Protocol Structure
- Communication via JSON-RPC 2.0 over HTTP/SSE
- Agents expose `/agent/invoke` endpoint
- Streaming support via Server-Sent Events
- Structured error handling with A2A error codes

### Agent Registration
Agents register with host agents by:
1. Implementing the A2A protocol endpoints
2. Providing agent metadata (name, description, capabilities)
3. Host agents maintain routing tables for registered agents

## Development Patterns

### Creating New Agents
1. Follow existing agent structure in your language of choice
2. Implement required endpoints: `/agent/invoke`, `/agent/info` (optional)
3. Use the a2a-sdk for Python agents when possible
4. Add proper error handling with A2A error codes

### Testing Agents
- Use the demo UI for interactive testing
- Test clients available in `samples/python/test_client/`
- Ensure agents handle malformed requests gracefully

## Security Considerations

**CRITICAL**: All agents should treat external agents as untrusted:
- Never execute code from agent responses
- Validate and sanitize all inputs
- Use structured data formats, avoid string interpolation
- Implement proper error boundaries
- Follow the security guidelines in the main README

## Framework-Specific Notes

### Google ADK Agents
- Located in `samples/python/adk_*`
- Require ADK CLI installation
- Use `adk gen` for code generation

### LangGraph Agents
- Use checkpoint persistence
- Implement proper state management
- See `samples/python/langgraph_agent/`

### CrewAI Agents
- Define crews with specific roles
- Configure task delegation
- See `samples/python/crewai_*`

## Environment Variables

Common environment variables used across agents:
- `GEMINI_API_KEY`: For Gemini AI integration
- `ANTHROPIC_API_KEY`: For Claude integration
- `OPENAI_API_KEY`: For OpenAI integration
- `PORT`: Agent server port (defaults vary by agent)

## Error Codes

Standard A2A error codes:
- `INVALID_PARAMS`: Invalid or malformed parameters
- `TASK_FAILED`: Agent task execution failed
- `INTERNAL_ERROR`: Unexpected server error
- `NOT_FOUND`: Resource or capability not found