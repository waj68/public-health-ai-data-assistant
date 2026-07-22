
# Phase 6A — AI/LLM SQL Integration Readiness Plan

## Project

Public Health AI Data Assistant

## Current Status

The current deployed app uses:

- Streamlit interface
- Semi-synthetic public health surveillance data
- DuckDB SQL execution
- Predefined public health questions
- Expanded rule-based free-text question handling
- Basic SQL safety checking
- Plain-language summaries

The app does not currently use a live AI/LLM model.

## Purpose of Phase 6A

Phase 6A prepares the project for future AI/LLM-based SQL generation.

The goal is to define the safety, privacy, prompt, and validation structure before connecting a real AI model.

## Proposed Future AI-SQL Workflow

1. User enters a public health question.
2. The app provides the AI model with schema context only.
3. The AI model generates a DuckDB-compatible SELECT query.
4. The app checks the SQL for safety.
5. Only approved read-only SELECT queries are executed.
6. Results are displayed in a table.
7. A plain-language summary is generated from the query result.
8. If the question is unclear, unsafe, or outside the schema, the app refuses safely or asks for clarification.

## What the AI Model May Receive

The AI model may receive:

- Table names
- Column names
- Column descriptions
- Join relationships
- High-level data notes
- The user's public health question

## What the AI Model Should Not Receive

The AI model should not receive:

- Real patient-level identifiable data
- Confidential health records
- Names, addresses, health card numbers, or direct identifiers
- Full raw datasets from operational systems
- Unnecessary row-level extracts from client or health-system data

## SQL Safety Rules

The AI-generated SQL must:

- Use DuckDB-compatible SQL
- Start with SELECT
- Be read-only
- Use only approved tables
- Avoid destructive commands such as INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, MERGE, GRANT, or REVOKE
- Be reviewed by the app's safety checker before execution

## Draft AI Prompt Template

System instruction:

You are a public health analytics SQL assistant. Generate only DuckDB-compatible SELECT queries. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, MERGE, GRANT, REVOKE, or other modifying SQL statements. Use only the tables and columns listed in the schema context. If the question cannot be answered using the available schema, return a refusal message instead of SQL.

Schema context:

[Insert table names, column names, descriptions, and relationships here]

User question:

[Insert user's question here]

Expected output:

Return only one SQL SELECT query. Do not include explanations before or after the SQL.

## Validation Requirements Before Real AI Integration

Before connecting a real AI/LLM model, the project should test:

- Whether generated SQL uses only approved tables
- Whether generated SQL starts with SELECT
- Whether blocked SQL keywords are rejected
- Whether unsupported questions are refused safely
- Whether outputs are consistent for common public health questions
- Whether summaries correctly describe the returned results
- Whether API keys are stored securely through Streamlit secrets or another secure mechanism
- Whether no confidential data are sent to external AI services

## Recommended Next Phase

Phase 6B should connect a real AI/LLM model only after the following are ready:

- Secure API key handling
- Stronger SQL parser or validation layer
- Clear cost-control plan
- Test question set
- Error handling for failed AI responses
- Documentation for privacy and deployment boundaries

## Current Recommendation

Do not connect real operational or patient-level data to an external AI/LLM service.

For real client or health-system deployment, the preferred model is:

- Run the app inside the client-controlled environment
- Send only schema context to the AI model when possible
- Avoid sending identifiable row-level data to external services
- Keep SQL safety checks active before execution
