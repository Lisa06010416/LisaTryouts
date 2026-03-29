# NotionDailyPage

This experiment uses Codex app automation with Notion MCP to create a daily routing page inside a Notion tasks database.

## What It Does

The daily workflow:

1. gathers recent news focused on Taiwan, the United States, and major global events
2. filters for reliable economy, market, technology, and AI coverage
3. collects JPY/TWD and USD/TWD exchange rate information
4. generates a concise summary with "Why it matters" and "Watch next" sections
5. creates a new page in a Notion tasks database
6. fills the page with a Mail section, an exchange rate section, and a news section

Default title format:

```text
Daily Routing at YYYY-MM-DD
```

Default Notion properties:

- `Title`: `Daily News a {today}`
- `Start Date`: today's date
- `Energy`: `Low Energy`
- `Status`: `Next Action`
- `Priority`: `Medium Priority`

## Notes

- The automation path depends on Codex app Automations and a working Notion MCP setup.
- The automation prompt tells Codex to inspect the target database schema first and then use the exact property names and types returned by Notion MCP.
- If you already know the tasks database URL, add it to the prompt before saving the automation so the run is more reliable.
