# Daily Routing To Notion Automation Prompt

Run this automation every day at 09:00

## Prompt

Use Notion MCP to create today's daily routing page in my tasks database.

Workflow:

1. Collect news information:

   * Use web research to collect the most relevant news from the last 24 hours.
   * Keep only high-signal items from reliable sources.
   * Produce a concise summary:

     * "Why it matters" with 3 bullets
     * "Watch next" with 3 bullets
2. Collect information about the JPY/TWD and USD/TWD exchange rates.
3. Create the Notion page - Daily Routing at {Today}:

   * Use Notion MCP to find or fetch my tasks database.
   * Before creating the page, inspect the database schema and use the exact property names and types from Notion.
   * Create one new page in the tasks database with:
     * Title: \`Daily News a {today}\`
     * Start Date: {today}
     * Energy: \`Low Energy\`
     * Status: \`Next Action\`
     * Priority: \`Medium Priority\`
   * If my database uses different property names, map them to the closest matching properties after checking the schema.
4. Fill in the content:

   * Mail section — remind me to read mail: {Mail Inbox URL}
   * Exchange rate section
   * News section -- Include a short run summary in the automation result with:
     * summary
     * reference news link

## Safety rules:

- Do not modify unrelated files in the repository.
- Prefer using a background worktree for this automation.
- If the tasks database cannot be identified, stop and report what database URL or page URL you need.

## Suggested database hint

If you already know the tasks database URL, append this line to the automation prompt before saving it:

Tasks database URL: {Your URL}
