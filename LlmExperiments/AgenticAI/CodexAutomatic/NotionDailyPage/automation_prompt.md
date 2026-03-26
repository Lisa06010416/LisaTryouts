# Daily News To Notion Automation Prompt

Run this automation every day at 09:00 in the project:

`/Users/linlisa/Documents/LisaTryouts/LlmExperiments/AgenticAI/CodexAutomatic/NotionDailyPage`

## Prompt

Use web research and Notion MCP to create today's daily news page in my tasks database.

Tasks database URL: https://www.notion.so/Tasks-2ff4bafa9e25817a9d54f777ce273901?source=copy_link

Use Asia/Taipei timezone to determine {today} and the last 24 hours window.

Task requirements:
- Gather reliable news from the last 24 hours only.
- Focus on Taiwan, the United States, and major global events.
- Focus topics: economy, stock market, technology, AI.
- Prioritize reliable sources such as Reuters, AP, CNBC, Bloomberg, Financial Times, WSJ, Nikkei Asia, Focus Taiwan, and other similarly reliable mainstream outlets.
- Include article links in the final page.
- Write the summary in Traditional Chinese.
- Use 3-6 high-signal items only. Prefer fewer items over filler.

Workflow:
1. Use web research to collect the most relevant news from the last 24 hours.
2. Keep only high-signal items from reliable sources.
3. Produce a concise summary:
   - 4-6 bullet executive summary
   - Why it matters with 3 bullets
   - Watch next with 3 bullets
4. Use the Tasks database URL above with Notion MCP to fetch the target database.
5. Before creating the page, inspect the database schema and use the exact property names and types from Notion.
6. Before creating a new page, check whether a page titled `Daily News {today}` already exists in the tasks database. If it exists, do not create a duplicate.
7. Create one new page in the tasks database only when there is meaningful news, with:
   - Title: `Daily News {today}`
   - Start Date: {today}
   - Energy: `Low Energy`
   - Status: `Next Action`
   - Priority: `Medium Priority`
8. If the database uses different property names, map them to the closest matching properties after checking the schema.
9. Put the summary and the source links in the page body.
10. If there are no meaningful items in the last 24 hours, do not create low-quality filler content. Report that there was nothing important to add.

Output expectations:
- Create the Notion page when there is meaningful news.
- Include a short run summary with:
   - page title
   - created Notion page URL
   - top sources used

Safety rules:
- Do not modify unrelated files in the repository.
- Prefer using a background worktree for this automation.
- If the tasks database cannot be fetched from the URL above, stop and report the issue.
