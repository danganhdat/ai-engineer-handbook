# Keep state and enforce ownership

Design persistence and authorization for conversation history and uploaded documents. The design will support retrieval across multiple users.

**Supporting · 85 minutes** · **Prerequisites** [Expose a typed API](fastapi.md) and basic familiarity with SQL.

## The problem

Conversations disappear after a restart, and a document ID alone says nothing about who can read it. Store durable state and derive access from an authenticated caller.

## Design the data boundary

Use PostgreSQL for conversations, turns, document metadata, and access records. Use object storage for uploaded file bytes. PostgreSQL can update related rows in a transaction. Blob Storage handles file bytes independently. Use a generated object key and keep the original filename as display metadata.

Authentication establishes the caller's identity. Authorization checks whether that identity can act on a record. Resolve the caller from a validated token and apply the ownership condition in the same query that reads records. This PostgreSQL excerpt assumes that `documents` has `id`, `owner_id`, `object_key`, and `status` columns.


```sql
PREPARE owned_document (uuid, uuid) AS
SELECT id, object_key, status
FROM documents
WHERE id = $1 AND owner_id = $2;
```


Bind both values as parameters. The second comes from the trusted caller context. Index the columns used by common queries, for example `(owner_id, created_at)` for listing an owner's documents. A connection pool reuses connections, so bound pool size when you add API replicas.

## Trace an upload

Create a pending document record. Store bytes under its generated key. Record successful upload and schedule indexing. A database transaction cannot roll back a completed object write. If updating the database fails, a cleanup task or retry can reconcile the pending record and its object key. Use migrations to evolve the schema and record which changes each environment has applied.

## Practice and debugging

Assume Alice uploads document A. Try Alice's token with A, Bob's token with A, and no token. Expect Alice to find A, Bob to receive the same response as an unknown ID, and the unauthenticated caller to receive `401`. If Bob sees A, inspect the dependency that resolves identity and the actual SQL predicate. A valid token alone cannot enforce ownership.

## Engineering decisions

PostgreSQL fits when conversations, documents, and permissions have relationships and need transactions. A document database can fit independent JSON aggregates when you know how they will be partitioned and read. In Azure, validate Entra issuer, audience, expiry, signature and required scopes. An application identity used to access storage serves a different purpose from the token sent by an end user.

## Recap and next step

You defined the ownership boundary that retrieval will enforce. [Next: Budget tokens and build prompts](../03-llm-engineering/context.md)

[PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html), [PostgreSQL prepared statements](https://www.postgresql.org/docs/current/sql-prepare.html), [Microsoft Entra access tokens](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
