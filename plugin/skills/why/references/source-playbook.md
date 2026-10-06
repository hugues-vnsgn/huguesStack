# Source playbooks

Assign each investigator one available tool or MCP and its single category playbook below. These are pinned examples for common services; their tool names, integrations, SQL tables and columns are templates, not installed-service claims. Inspect the actual tool schema and access before translating each search. Record a missing tool, inaccessible source or retention gap separately from a completed empty search. Read the selected file in full. Include this index's adaptation rules in the investigator handoff.

Follow the current human authority supplied by the coordinator. Keep all searches read-only and send no messages. Run available read-only source queries, including schema inspection and SQL retrieval, within the current research request and authorized source access. Inspect tool effects; service writes/setup or new private-data transmission outside that source scope requires explicit current authority. Apply that boundary to tools that launch new AI analyses, including the Sentry Seer example. Read existing reports as evidence; running apps or tests requires explicit consumer authority. Prepare a query and report the gap only when actual authority or capability excludes it. If authentication or a connection is missing, stop that source and report the gap. Leave service setup to a separately authorized task.

| Category | Playbook | Example MCP it documents |
|---|---|---|
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |
| Issue / ticket tracker | [`linear.md`](./sources/linear.md) | Linear (adapt for Jira, GitHub Issues, Plane, Shortcut) |
| Long-form documents | [`notion.md`](./sources/notion.md) | Notion (adapt for Confluence, Google Docs, Coda) |
| Real-time team chat | [`slack.md`](./sources/slack.md) | Slack (adapt for Discord, Microsoft Teams, Mattermost) |
| Infrastructure observability | [`datadog.md`](./sources/datadog.md) | Datadog (adapt for New Relic, Honeycomb, Grafana, Splunk) |
| Error / exception tracking | [`sentry.md`](./sources/sentry.md) | Sentry (adapt for Rollbar, Bugsnag, Airbrake) |
| Product analytics warehouse | [`databricks.md`](./sources/databricks.md) | Databricks SQL (adapt for Snowflake, BigQuery, ClickHouse, dbt) |

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler).
