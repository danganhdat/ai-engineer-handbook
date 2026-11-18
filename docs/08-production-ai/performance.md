# Measure performance and cache results

Estimate concurrency, choose a low-risk cache, and work out whether another API replica would help.

**Core · 70 minutes** · **Prerequisites** [Observe quality, latency and cost](observability.md).

## The problem

At peak load, Document Assistant spends money embedding repeated questions and waiting for model capacity. Scaling API containers may leave the provider bottleneck unchanged.

## Measure the bottleneck

If 12 requests per second each spend an average of two seconds in flight, expect about 24 concurrent requests under steady load. Compare that estimate with measured p95 latency, provider limits, connection pool, and worker counts. Test realistic query mixes, including streaming and cold requests. Batching embeddings can increase throughput and add a wait before a batch is sent.

## Sketch a cache

Redis can hold computed embeddings under a key with a time to live (TTL). Begin with a key that incorporates scope, embedding deployment version, and an HMAC of the exact embedding input. An HMAC uses a secret to generate the digest, so the key need not expose the original question.

| Request | Result with a 300-second TTL |
| --- | --- |
| Tenant A, model v1, question Q, time 0 | Miss and compute |
| Tenant A, model v1, Q, time 30 | Hit |
| Tenant B, model v1, Q, time 30 | Miss because the scope differs |
| Tenant A, model v2, Q, time 30 | Miss because the model version differs |
| Tenant A, model v1, Q, time 310 | Miss after expiry |

This cache holds embeddings. Retrieval still enforces document access. Caching entire answers needs a stronger key with corpus and permission versions because documents and access can change.

## Practice and debugging

Traffic doubles. CPU stays low while model rate limits and database pool waits rise. Explain why adding API replicas can raise pressure on both dependencies. Introduce bounded model concurrency, review retries and consider a separately scaled worker. Verify p95, throughput, provider errors, and cache hit rate on the same load profile.

## In production

Treat a cache as a performance dependency. Tune its deadline and define how to fall back when it fails. Measure memory, expiry, and stale results. If a single miss triggers a burst of duplicate work, combine concurrent refreshes or stagger expirations. Use Azure Managed Redis when a managed cache is justified. Microsoft's retirement guidance covers the older Azure Cache for Redis service.

## Recap and next step

You can choose which work to cache and distinguish scaling an API from scaling its dependencies. [Next: Scale ingestion with queues and workers](ingestion-workers.md)

[Redis EXPIRE](https://redis.io/docs/latest/commands/expire/), [Azure Redis retirement guidance](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/retirement-faq)
