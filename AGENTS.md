# Resin instructions for coding agents 

## Project Overview

This is the `resin` project for fetching GTR API data. It uses DuckDB for storage and SQLAlchemy for query building.

## Setup Commands

- Install dependencies: `uv sync`
- Run CLI: `uv run resin`

## CLI Commands

- `resin bronze init` - Create bronze layer tables
- `resin bronze fetch` - Fetch data from GTR API into bronze layer
- `resin silver init` - Create silver layer tables
- `resin silver load` - Load data into silver tables from bronze
- `resin silver sql <entity>` - Print SQL for a silver entity

## Code Style

- Python 3.12+
- Type annotations required on all functions
- Keep things simple and functional
- Don't over-engineer or add unnecessary abstractions

## Critical Rules

**FOLLOW INSTRUCTIONS EXACTLY. DO NOT BE "CLEVER" OR HELPFUL BEYOND WHAT IS ASKED.**

1. **Answer what is asked, nothing more**
   - If asked for OPTIONS, provide options only - do not implement anything
   - If asked to make a specific change, make only that change
   - Do not add features, refactors, or "improvements" unless explicitly requested

2. **Do not assume what the user wants**
   - If they ask "how do I do X?", explain how - don't do it for them
   - If they ask "what are my options?", list options - don't pick one and implement it
   - If a problem arises during implementation, STOP and present it to the user

3. **When making code changes:**
   - Make the minimal change requested
   - Do not refactor, reorganize, or "improve" code unless asked
   - Do not enhancements unless requested
   - Do not add unnecessary blank lines, formatting, or spacing changes
   - Do not add comments explaining what code does - only add comments that explain WHY
   - Always check diagnostics before considering work complete
   - When editing multiple similar files, maintain consistent patterns
   - Verify import chains won't create circular dependencies before writing code

4. **Precision and honesty:**
   - Be precise and accurate in all answers
   - If you don't know something, be honest about it
   - Don't make assumptions or fill gaps with speculation

## Testing Instructions

- Run diagnostics on all modified files before considering work complete
- Fix type errors, linting issues, and other diagnostics

## Version control instructions

- Do not commit code ever. This is a critical rule
