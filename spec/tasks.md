# Implementation tasks


## Task-01 Retrieve the complaint and account information

| Field | Value |
| --- | --- |
| Requirements | FR-001, FR-003 |
| Files |   /app/complaint/model.py, /app/complaint/repository.py, /app/account/model.py, /app/account/repository.py  |

### Implementation Instructions

- Define the complaint model
- Define the account model
- Retrieve complaint information
- Retrieve account infomration
- Define eligibility reason codes. (`INVALID_COMPLAINT`, `COMPLAINT_NOT_FOUND `, `ACCOUNT_NOT_FOUND`)
- Attach where each retrieved information comes from
- Reject unsupported reason values. 


### Definition of done

- Searching up a complaint returns all its information
- Searching up an account returns all its information based on the complaint
- The results show where it was retrieved from
- Unknown complaints or accounts are stated explictly (`INVALID_COMPLAINT`, `COMPLAINT_NOT_FOUND `, `ACCOUNT_NOT_FOUND`)

### Copilot command

Implement Task-01 only. Read the specfication and implementation plans first. Access and modify only the cited files, if other files are needed to complete the task request for access first. Run the tests and document the results based on the definition of done.



## Task-02: Implement details of complaint
| Field | Value |
| --- | --- |
| Requirements | FR-002, FR-003|
|Files| app/backend/src/repository; repository tests|
### Implementation Instructions
- Define Complaint and StatusHistory files from Data Models section of spec
- Retrive information of complaint through `complaint_id` using SQL
- Follow security not found convention
### Definition of Done
- All operational facts are tested and verified to be correct
- No account data is exposed
- AC-001, AC-002 both pass
### Copilot command

Implement Task-02 only. Read the specfication and implementation plans first. Access and modify only the cited files, if other files are needed to complete the task request for access first. Run the tests and document the results based on the definition of done.


## Task-03 Retrieve the transaction information


| Field | Value |
| --- | --- |
| Requirements | FR-002, FR-003 |
| Files |   /app/transaction/model.py, /app/transaction/repository.py, 





# RAG Tasks

## Task 1 Load policy PDFs : 

### Implementation Instructions

- Read the approved policy PDFs from the knowledge base folder
- Extract the text with its section headings
- Read `document_id`, `document_title`, `version` and `effective_date` for each document
- Skip documents that are not approved


### Definition of done

- Every approved PDF is loaded with its text and sections
- A document missing its version or effective date is rejected with a clear error
- AC-005 is completed




## Task 2 Create chunking service: 

 
 ### Implementation Instructions

- Split each document into chunks of 500 tokens with a 100-token overlap
- Give each chunk a `passage_id`
- Attach the document metadata to every chunk

### Definition of done

- No chunk is longer than 500 tokens
- Neighbouring chunks overlap by 100 tokens
- Every chunk carries `passage_id`, `document_id`, `document_title`, `section`, `version` and `effective_date`
- AC-006 and 008 are completed



### Task 3 Generate embeddings : 

### Implementation Instructions

- Embed every chunk with the chosen embedding model
- Store the vectors and the chunk metadata in ChromaDB
- Embed queries with the same model
- Record the model name used

### Definition of done

- Every chunk has one stored vector
- Chunk and query vectors have the same length


## Task 4 Implement vector search : 

### Implementation Instructions

- Embed the query and return the top 3 closest chunks (k = 3)
- Return each chunk with its metadata and `retrieved_at`
- Define reason codes (`OK`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTORY_EVIDENCE`)

### Definition of done

- A query about a known policy returns the expected chunk in the top 3
- Every returned chunk includes all required metadata
- The same query returns the same results in the same order
- AC-008 is completed


## Task 5 Implement citation: 


### Implementation Instructions


- Require a citation on every policy statement in the case summary
- Reject any citation that was not in the retrieved set

### Definition of done

- Every policy statement in the summary has a citation
- AC-006



## Task 6 Implement abstention logic : 


### Implementation Instructions

- Return `INSUFFICIENT_EVIDENCE` when no chunk scores above the threshold
- Return `CONTRADICTORY_EVIDENCE`, with both chunks, when two current chunks disagree
- Send contradictory cases to a supervisor


### Definition of done

-  An off-topic query returns `INSUFFICIENT_EVIDENCE` and no chunks
- Two conflicting chunks return `CONTRADICTORY_EVIDENCE` with both included
- No policy statement is produced when the status is not `OK`
- AC-005 and 007 are completed






### Implementation Instructions

- Define the transaction model
- Define eligibility reason codes. 


### Definition of Done
- AC-003 passes
- Must be read-only files and not create anything extra

### Copilot command

Implement Task-03 only. Read the specfication and implementation plans first. Access and modify only the cited files, if other files are needed to complete the task request for access first. Run the tests and document the results based on the definition of done.
