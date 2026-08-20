---
name: accidental-data-loss-prevention
description: |
  **STOP AND VERIFY**: Before running any command or tool that results in irreversible data loss, you MUST obtain explicit user consent.
  When in doubt, ask. It is better to wait for confirmation than to accidentally delete production data or critical project assets.
  Use this for:
  - SQL: DROP TABLE/VIEW/SCHEMA/DATABASE, TRUNCATE, or broad DELETE (missing WHERE or using 1=1).
  - Cloud Storage: gsutil rm or gcloud storage rm targeting production data or critical buckets.
  - Infrastructure: gcloud projects delete, deleting Spanner/BigQuery/Dataproc resources, deleting secrets, or KMS key destruction.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

# Accidental Data Loss Prevention

> [!CAUTION]
>
> **STOP AND VERIFY**: Before running any command or tool that results in
> irreversible data loss, you **MUST** obtain explicit user consent.

## Mandatory Procedure

1.  **Halt Execution**: Do **not** execute the command.
2.  **Request Consent**: Explain clearly to the user:
    -   The **impact** of this deletion.
    -   **Why** you believe this is necessary.
    -   A request for their **explicit approval** to proceed.
3.  **Wait**: Only proceed if the user provides clear, affirmative consent in
    the conversation.
4.  **Capture Context**: Trigger the standardized capture script to record the reason for the data loss request and the user's consent decision.

## 6) Memory Sync

After a data loss risk assessment or a consent-based deletion is completed, you **MUST** trigger the local memory capture. 

1. Save the final risk assessment or the summary of the consent-based deletion as a Markdown file in the project directory.
2. Invoke the capture script: 
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that high-risk operations and their associated approvals/justifications are automatically routed to the correct storage (OKF or ChromaDB).
