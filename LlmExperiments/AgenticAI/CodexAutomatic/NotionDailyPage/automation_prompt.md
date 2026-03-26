# Daily News To Notion Automation Prompt

Run this automation every day at 09:00 in the project:

`LlmExperiments/AgenticAI/CodexAutomatic/NotionDailyPage`

## Prompt

Use Notion MCP to create today's daily news page in my tasks database.

Task requirements:

- Gather reliable news from the last 24 hours only.
- Focus on Taiwan, the United States, and major global events.
- Focus topics: economy, stock market, technology, AI.
- Prioritize reliable sources such as Reuters, AP, CNBC, Bloomberg, Financial Times, WSJ, Nikkei Asia, Focus Taiwan, and other similarly reliable mainstream outlets.
- Include article links in the final page.
- Write the summary in Traditional Chinese.

Workflow:

1. Use web research to collect the most relevant news from the last 24 hours.
2. Keep only high-signal items from reliable sources.
3. Produce a concise summary:
   - 4-6 bullet executive summary
   - "Why it matters" with 3 bullets
   - "Watch next" with 3 bullets
4. Use Notion MCP to find or fetch my tasks database.
5. Before creating the page, inspect the database schema and use the exact property names and types from Notion.
6. Create one new page in the tasks database with:
   - Title: `Daily News a {today}`
   - Start Date: {today}
   - Energy: `Low Energy`
   - Status: `Next Action`
   - Priority: `Medium Priority`
7. If my database uses different property names, map them to the closest matching properties after checking the schema.
8. Put the summary and the source links in the page body.
9. If there are no meaningful items in the last 24 hours, do not create low-quality filler content. Archive the automation run or report that there was nothing important to add.

Output expectations:

- Create the Notion page when there is meaningful news.
- Include a short run summary in the automation result with:
  - page title
  - created Notion page URL
  - top sources used

Safety rules:

- Do not modify unrelated files in the repository.
- Prefer using a background worktree for this automation.
- If the tasks database cannot be identified, stop and report what database URL or page URL you need.

## Suggested database hint

If you already know the tasks database URL, append this line to the automation prompt before saving it:

`Tasks database URL: <paste-your-notion-database-url-here>`
