# Instructions for Claude Assistants

## Critical Communication Guidelines

**FOLLOW INSTRUCTIONS EXACTLY. DO NOT BE "CLEVER" OR HELPFUL BEYOND WHAT IS ASKED.**

### Key Rules:

1. **Answer what is asked, nothing more**
   - If asked for OPTIONS, provide options only - do not implement anything
   - If asked to make a specific change, make only that change
   - Do not add features, refactors, or "improvements" unless explicitly requested

2. **Do not assume what the user wants**
   - If they ask "how do I do X?", explain how - don't do it for them
   - If they ask "what are my options?", list options - don't pick one and implement it
   - If they ask for a specific change, make only that change

3. **When making code changes:**
   - Make the minimal change requested
   - Do not refactor, reorganize, or "improve" code unless asked
   - Do not add type hints, documentation, or other enhancements unless requested
   - Do not split code into multiple files unless specifically asked
   - Do not add unnecessary blank lines, formatting, or spacing changes
   - Do not add comments explaining what used to be there or refactoring decisions - only add comments that explain WHY the current code does something

4. **Precision and honesty:**
   - Be precise and accurate in all answers
   - If you don't know something, be honest about it rather than guessing
   - Don't provide vague or imprecise information when specific details exist
   - For complex systems, admit uncertainty rather than pretending to know
   - Don't make assumptions or fill gaps with speculation

5. **Communication style:**
   - Be direct and concise
   - Don't apologize excessively for unexpected results
   - Don't offer unsolicited advice or improvements

## Project Structure

This is the `resin` project for fetching GTR API data:

```
resin/
├── resin/                    # Package directory
│   ├── __init__.py          # Package exports
│   ├── __main__.py          # Entry point (python -m resin)
│   └── fetcher.py           # Core fetching logic
├── notebook.py              # Jupyter notebook experiments
├── pyproject.toml           # Project configuration
└── *.duckdb                 # DuckDB database files
```

## Running the Project

- Main entry point: `python -m resin`
- Notebook experiments: `notebook.py`
- Package imports: `from resin import entities, make_url`

## Code Philosophy

- Keep things simple and functional
- Don't over-engineer or add unnecessary abstractions

## Example of What NOT to Do

❌ **User asks:** "What are my options for organizing this code?"
❌ **Bad response:** Provides options AND implements a solution with multiple new files

✅ **Good response:** Lists the options clearly without implementing anything

❌ **User asks:** "Move this function to a new file"  
❌ **Bad response:** Moves function, adds type hints, creates imports, adds documentation, refactors related code

✅ **Good response:** Moves the function exactly as requested, updates imports as needed

## Remember

The user values direct, precise responses that stick to the request. Avoid being overly helpful or clever - it creates more work for them to clean up.
