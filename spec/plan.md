# Implementation Plan


## Repository Context
Fictional training repository: https://github.com/fdm-training/banking-complaint-solution
- Specification:/specs/banking-complaint-assistant/spec.md
- Plan:/specs/banking-complaint-assitant/plan.md
- Task:/specs/banking-complaint-assitant/task.md
- Complaint model: /app/complaint/model.py
- Complaint repository: /app/complaint/repository.py
- Account model:/app/account/model.py
- Account repository: /app/account/repository.py
- Transaction model: /app/transaction/model.py
- Transaction repository:/app/transaction/repository.py
- Desposit model: /app/deposit/model.py
- Deposit repository: /app/deposit/repository.py
- Fee model: /app/fee/model.py
- Fee repository: /app/transaction/model.py
- Service request model: /app/service request/model.py
- service request repository:/app/service request/repository.py
- Audit model: /app/audit/model.py
- Audit repository:/app/audit/repository.py
- Tests:/tests/disputes/

## Technology stack

| Area |  Decision  | 
| --- | --- |
| Language | Python |
| API Framework | FastAPI |
| Valiation | Pydantic V2 |
| Persistence | PostgreSQL |
| Migrations | Alembic |
| ORM | SQLAlchemy |
| Unit tets| pytest |
| API tests | FastAPI TestClient |
| embedding and indexing| Chromadb |



## Project structure


```
banking-complaint-resolution/ 
├── app/
|   ├── backend/
|   |      └── src/
|   |           ├── model/        Complaint, Account, Transaction, deposit, fee, service request
|   |           ├── Repository/  Complaintrepo, Accountrepo, Transactionrepo, depositrepo, feerepo, service requestrepo
|   |           ├── services
|   |           ├── routes
|   |           └── RAG/ Ingestion, embedding, store, retriever, pipeline
|   ├── frontend/
|   |       └── src/
│   └── investigation/ 
│       ├── schemas.py 
│       ├── repository.py
│       ├── investigation_service.py 
│       └── router.py
├── tests/ 
│   ├── unit/disputes/test_investigation__service.py 
│   └── integration/disputes/test_investigation__api.py 
└── specs/banking-complaint-assistant/ 
    ├── spec.md 
    ├── plan.md 
    └── tasks.md


```


## Proposed API
POST/api/v1/Complaint/{complaint_id}/investigation
### Request:


## Component responsibilities


| Component |  responsibilities | 
| --- | --- |
| Ingestion |  Read the the knowledge base, break it down into chunks, emebed the shcunks and index them.|
| Retireval |  Input a query that is embedded then indexed i n the same way, then match the k number of close matches from the kb chunks. |
| Synthesis |  Take the in the query with its top k chunk matches to augment the LLM and create an output |


1. Load approved documents 

2. Chunk documents 

3. Generate embeddings 

4. Store vectors 

5. Build retrieval API 

6. Generate answers 

7. Add citations 

8. Add testing 


## Deterministic validation order

## Technical decisions
| Component |  Decision | 
| --- | --- |
| Embeddings | ChromaDB stores the vectors and the embeddings fro both the kb and the query  |
| Retrieval | retrieveal is done using vector search |
| k number | the number of close matches used will be 3 |
| chunk size | each chunk size will be 500 tokens |
| chunk overlap | each chunk will overlap by 100 tokens |
| Chunks metadata | Metadata is created for each chunk created|





## Security and Data handling

- Each chunk that is returned will also return all the following metadata to confirm its existence and provenance:

| Field | Example | Purpose |
|---|---|---|
| `passage_id` | `KB-001#c003` | The evidence ID used in citations.|
| `document_id` | `KB-001` | The source document the chunk came from which document |
| `document_title` | Overdraft Fee Policy | The name of the document title retrieved from |
| `section` | 3.2 Fee reversal | Heading of the chunk |
| `version` | 2.1 | Which version of the document was used |
| `effective_date` | 2026-03-01 | When was the version created |
| `retrieved_at` | 2026-11-23 10:15:02 | When the chunk was retrieved at|

- When a query doesn't match any relevant chunks, or has 2 chunks that are providing with different or contradcitory information the following results should be output.

| Situation | Result |
|---|---|
| No passage above the threshold | `INSUFFICIENT_EVIDENCE` |
| Two current passages disagree on the same point | `CONTRADICTORY_EVIDENCE`, both are returned, routed to a supervisor |



