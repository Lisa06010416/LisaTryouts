# NotionDailyPage

This experiment uses Codex app automation with Notion MCP to create a daily page inside a Notion tasks database.

## What It Does

The daily workflow:

1. gathers recent news focused on Taiwan, the United States, and major global events
2. filters for reliable economy, market, technology, and AI coverage
3. generates a concise summary
4. creates a new page in a Notion tasks database

Default title format:

```text
Daily News at YYYY-MM-DD
```

Default Notion properties:

- `start_date`: today's date
- `engery`: `Low Energy`
- `Status`: `Next Action`
- `Priority`: `Medium Priority`

## Notes

- The automation path depends on Codex app Automations and a working Notion MCP setup.
- The automation prompt tells Codex to inspect the target database schema first and then use the exact property names and types returned by Notion MCP.
- If you already know the tasks database URL, add it to the prompt before saving the automation so the run is more reliable.
