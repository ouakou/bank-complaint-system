



# Document inventory

| source_id | title | document_type | version | effective_date | access_label | status |
|---|---|---|---|---|---|---|
| KB-001 | Enterprise Complaint Management Policy | Policy | 3 | 2026-01-01 | Internal | Approved |
| KB-002 | Escalation, Approval and Decision Authority Standard | Policy | 2.1 | 2026-02-15 | Restricted | Approved |
| KB-003 | Fee, Charge and Interest Complaint Playbook | Playbook | 2 | 2026-03-01 | Internal | Approved |
| KB-004 | Digital Banking and Account Access Operations Guide | Guide | 2 | 2026-03-20 | Internal | Approved |
| KB-005 | Customer Service, Communication and Accessibility Standard | Policy | 2 | 2026-04-01 | Internal | Approved |
| KB-006 | Mortgage Servicing Complaint Investigation Playbook | Playbook | 2 | 2026-04-15 | Internal | Approved |
| KB-007 | Complaint Investigation and Resolution Analyst Playbook | Playbook | 2 | 2026-05-01 | Internal | Approved |
| KB-008 | AI Governance, Information Security and Audit Standard | Policy | 2 | 2026-05-15 | Restricted | Approved |
| KB-009 | Complaint Operations Knowledge Articles and FAQ | FAQ | 1 | 2026-06-01 | Internal | Approved |
| KB-010 | Historical Complaint Casebook | Casebook | 1 | 2026-06-15 | Internal | Approved |
| BUL-2026-01 | Operational Bulletin: Approval Threshold Clarification | Bulletin | 1 | 2026-02-20 | Internal | Approved |
| BUL-2026-02 | Operational Bulletin: RAG Source and Citation Controls | Bulletin | 1 | 2026-05-20 | Restricted | Approved |
| KB-001-OLD | Superseded Complaint Handling Policy | Policy | 1.4 | 2024-01-01 | Internal | Superseded |




# Document metadata model


| Field | Type / format | Allowed values or rule | Description |
|---|---|---|---|
| `source_id` | str | Unique across all documents | Stable identifier for the source document |
| `title` | str | Not empty | Document title, shown in citations |
| `document_type` | str | `Policy`, `Playbook`, `Guide`, `FAQ`, `Casebook`, `Bulletin` | Classification used by the retrieval filter. Use this exact name in the retrieval contract |
| `category` |  str  | Fee Dispute, Service Delay, Transaction Error, Online Banking, Card Issue, Customer Service, Fraud Claim | Subject area |
| `version` |  str  | For example `3`, `2.1`, `1.4` | Document version |
| `effective_date` |  date, `YYYY-MM-DD` | A real calendar date | When this version becomes applicable |
| `access_label` | str| `Internal`, `Restricted` | Access-control value used by retrieval filtering |
| `status` |  str  | `Approved`, `Superseded` | Only `Approved` is retrievable |
| `checksum` |  str  | Computed from the source file | Content-integrity value |


# Chunk fields metadata model

| Field |  Type / format | Rule | Description |
|---|---|---|---|
| `chunk_id` |  str | Unique. For example `KB-001#c003` | Evidence ID used in citations |
| `source_id` |  str | Must match an existing document | Parent document |
| `heading` / `section` |  str | Same header as the section, For example `3.2 Fee reversal` | Section the chunk came from |
| `sequence` | int | Starts at 1 for each document and has no gaps | Position of the chunk in the document |
| `access_label` | str  | Same values as the document | Copied from the parent so filtering can run on chunks |



# Index strategy

- Vector indexing is needed to embedd each chunk of around 500 tokens, to match to the correct chunk
- Text indexing is needed to embedd each word or group of texts used to match the query to the exact words or section within the chunk that correpsonds best to it.
- Metadata indexing is needed to embedd the metadata of a chunk (document type or title potentially) to match initially to the most relative document. 



document types : `Policy`, `Playbook`, `Guide`, `FAQ`, `Casebook`, `Bulletin`
effective version: Latest version (`Approved`), If its an older version then: (`superseded`)
access label: `Internal` or `restricted` 
