---
name: alloydb-omni-replication
description: Use these skills when you need to monitor the health of database replication,
  manage sync states between nodes, and audit publication tables for distributed setups.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and
`<param_value>` with actual values.

**Bash:** `node <skill_dir>/scripts/<script_name>.js '{"<param_name>":
"<param_value>"}'`

**PowerShell:** `node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\":
\"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env
files. Do not ask the user to set vars unless skill executions fails due to env
var absence.

## Scripts

### database_overview

Fetches the current state of the PostgreSQL server, returning the version,
whether it's a replica, uptime duration, maximum connection limit, number of
current connections, number of active connections, and the percentage of
connections in use.

--------------------------------------------------------------------------------

### list_publication_tables

#### Parameters

| Name              | Type    | Description     | Required | Default |
| :---------------- | :------ | :-------------- | :------- | :------ |
| table_names       | string  | Optional:       | No       |         |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of table   :          :         :
:                   :         : names.          :          :         :
| publication_names | string  | Optional:       | No       |         |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of         :          :         :
:                   :         : publication     :          :         :
:                   :         : names.          :          :         :
| schema_names      | string  | Optional:       | No       |         |
:                   :         : Filters by a    :          :         :
:                   :         : comma-separated :          :         :
:                   :         : list of schema  :          :         :
:                   :         : names.          :          :         :
| limit             | integer | Optional: The   | No       | `50`    |
:                   :         : maximum number  :          :         :
:                   :         : of rows to      :          :         :
:                   :         : return.         :          :         :

--------------------------------------------------------------------------------

### list_replication_slots

List key details for all PostgreSQL replication slots (e.g., type, database,
active status) and calculates the size of the outstanding WAL that is being
prevented from removal by the slot.

--------------------------------------------------------------------------------

### replication_stats

Lists each replica's process ID, user name, application name, backend_xmin
(standby's xmin horizon reported by hot_standby_feedback), client IP address,
connection state, and sync_state, along with lag sizes in bytes for sent_lag
(primary to sent), write_lag (sent to written), flush_lag (written to flushed),
replay_lag (flushed to replayed), and the overall total_lag (primary to
replayed).

--------------------------------------------------------------------------------

## Anti-Patterns

- NEVER execute raw DML/DDL operations on production database instances without verification.
- NEVER ignore connection limits and connection pool starvation indicators.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
