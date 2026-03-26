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
Daily News a2 YYYY-MM-DD
```

Default Notion properties:
- `start_date`: today's date
- `engery`: `Low Energy`
- `Status`: `Next Action`
- `Priority`: `Medium Priority`

## Recommended: Codex App Automation

OpenAI's Codex automations documentation says automations:
- run in the background in the Codex app
- require the app to be running and the selected project to be available on disk
- can run either in the local project or in a separate worktree
- should be tested manually in a regular thread before being scheduled

Reference:
- https://developers.openai.com/codex/app/automations

### Setup steps

1. Open the Codex app.
2. Open this project folder.
3. Make sure your Notion MCP integration is available in Codex.
4. Open the Automations pane in the Codex sidebar.
5. Create a recurring automation scheduled for `09:00` every day.
6. Prefer running it in a background worktree.
7. Copy the prompt from [`automation_prompt.md`](./automation_prompt.md).
8. If you know your tasks database URL, append it to the prompt before saving the automation.
9. Test the prompt once manually before enabling the recurring schedule.

### What the automation should do

The prompt in [`automation_prompt.md`](./automation_prompt.md) instructs Codex to:
- research the last 24 hours of relevant news
- summarize it in Traditional Chinese
- inspect your Notion tasks database schema through MCP
- create a Notion page with the required task properties
- insert the summary and links into the page body

## Notes

- The automation path depends on Codex app Automations and a working Notion MCP setup.
- The automation prompt tells Codex to inspect the target database schema first and then use the exact property names and types returned by Notion MCP.
- If you already know the tasks database URL, add it to the prompt before saving the automation so the run is more reliable.
