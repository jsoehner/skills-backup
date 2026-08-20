---

name: cloud-sql-sqlserver-data

description: Use these skills when you need to explore the database schema, execute

  SQL queries to interact with your data, and monitor system-level performance metrics

  using PromQL queries.

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



### execute_sql



Use this tool to execute SQL.



#### Parameters



Name | Type   | Description         | Required | Default

:--- | :----- | :------------------ | :------- | :------

sql  | string | The sql to execute. | Yes      |



--------------------------------------------------------------------------------



### list_tables



Lists detailed schema information (object type, columns, constraints, indexes,

triggers, comment) as JSON for user-created tables (ordinary or partitioned).

Filters by a comma-separated list of names. If names are omitted, lists all

tables in user schemas.



#### Parameters



| Name          | Type   | Description     | Required | Default    |

| :------------ | :----- | :-------------- | :------- | :--------- |

| table_names   | string | Optional: A     | No       | ``         |

:               :        : comma-separated :          :            :

:               :        : list of table   :          :            :

:               :        : names. If       :          :            :

:               :        : empty, details  :          :            :

:               :        : for all tables  :          :            :

:               :        : will be listed. :          :            :

| output_format | string | Optional: Use   | No       | `detailed` |

:               :        : 'simple' for    :          :            :

:               :        : names only or   :          :            :

:               :        : 'detailed' for  :          :            :

:               :        : full info.      :          :            :



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
