# High-Availability RAG System: Example Test Runs

This document contains example test runs of the High-Availability RAG system, showing how the system handles component failures and gracefully degrades using fallback mechanisms.



## Query 1: How do RAG systems work?

```plaintext
================================================================================
QUERY: How do RAG systems work?
================================================================================
2025-04-07 20:10:18,935 - HighAvailabilityRAG.System - INFO - Processing query: 'How do RAG systems work?'
2025-04-07 20:10:19,142 - HighAvailabilityRAG.Components.Embedders - INFO - Primary embedder: Generated embedding for 'How do RAG systems w...'
2025-04-07 20:10:19,356 - HighAvailabilityRAG.Components.Retrievers - INFO - Primary retriever: Retrieved 3 documents
2025-04-07 20:10:19,356 - HighAvailabilityRAG.Components.Generators - WARNING - Primary generator failed
2025-04-07 20:10:19,356 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component generator failed: Primary generation service unavailable
2025-04-07 20:10:19,356 - HighAvailabilityRAG.System - INFO - Trying fallback generator 1
2025-04-07 20:10:19,464 - HighAvailabilityRAG.Components.Generators - INFO - Fallback generator: Generated response for 'How do RAG systems w...'

RESPONSE:
Based on 3 documents, here's a basic answer to 'How do RAG systems work?...'

SYSTEM HEALTH:
  EMBEDDER:
    state: closed
    failure_rate: 0.000
    avg_response_time_ms: 205.768
  RETRIEVER:
    state: closed
    failure_rate: 0.000
    avg_response_time_ms: 213.772
  GENERATOR:
    state: closed
    failure_rate: 1.000
    avg_response_time_ms: 0.000
```

### Analysis of Test Scenarios - Query 1: How do RAG systems work?

**Component Performance:**

- **Embedder**: The primary embedder successfully generated an embedding for the query with no failures.
- **Retriever**: The primary retriever successfully retrieved 3 relevant documents with no failures.
- **Generator**: The primary generator failed, triggering the fallback mechanism. The fallback generator successfully produced a response.

**Circuit Breaker States:**

- All circuit breakers remain in the CLOSED state, indicating normal operation despite the generator failure.
- The generator's failure rate is at 100%, but since this is likely the first query, it hasn't reached the minimum sample threshold (3) required to open the circuit.

**System Resilience:**

- The system demonstrated graceful degradation by seamlessly switching to the fallback generator when the primary generator failed.
- The user still received a coherent response, albeit a simpler one from the fallback generator, rather than the more detailed response the primary generator would have provided.
- The response quality was maintained by using the successfully retrieved 'context documents' from the primary retriever.

**Key Takeaway:**
This example illustrates the system's ability to handle component failures without complete service disruption. Even though one component (the generator) failed, the overall RAG pipeline continued to function by leveraging the fallback strategy, providing a degraded but still useful response to the user.



## Query 2: What are the advantages of Docker containers?

```plaintext
================================================================================
QUERY: What are the advantages of Docker containers?
================================================================================
2025-04-07 20:10:21,935 - HighAvailabilityRAG.System - INFO - Processing query: 'What are the advantages of Docker containers?'
2025-04-07 20:10:22,142 - HighAvailabilityRAG.Components.Embedders - WARNING - Primary embedder failed
2025-04-07 20:10:22,142 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component embedder failed: Primary embedding service unavailable
2025-04-07 20:10:22,142 - HighAvailabilityRAG.System - INFO - Trying fallback embedder 1
2025-04-07 20:10:22,356 - HighAvailabilityRAG.Components.Embedders - INFO - Secondary embedder: Generated embedding for 'What are the advant...'
2025-04-07 20:10:22,456 - HighAvailabilityRAG.Components.Retrievers - INFO - Primary retriever: Retrieved 3 documents
2025-04-07 20:10:22,756 - HighAvailabilityRAG.Components.Generators - INFO - Primary generator: Generated response for 'What are the advant...'

RESPONSE:
Based on 3 documents including 'Document 5 with detailed information...', the answer to 'What are the advantages of Docker c...' is a detailed explanation with nuanced insights.

SYSTEM HEALTH:
  EMBEDDER:
    state: closed
    failure_rate: 0.500
    avg_response_time_ms: 214.000
  RETRIEVER:
    state: closed
    failure_rate: 0.000
    avg_response_time_ms: 100.000
  GENERATOR:
    state: closed
    failure_rate: 0.500
    avg_response_time_ms: 300.000
```

### Analysis of Test Scenarios - Query 2: What are the advantages of Docker containers?

**Component Performance:**

- **Embedder**: The primary embedder failed, triggering the fallback to the secondary embedder, which succeeded.
- **Retriever**: The primary retriever successfully retrieved 3 relevant documents with no failures.
- **Generator**: The primary generator successfully generated a detailed response.

**Circuit Breaker States:**

- All circuit breakers remain in the CLOSED state.
- The embedder's failure rate is at 50% (1 failure out of 2 total calls), which is above the threshold (40%) but hasn't reached the minimum sample threshold (3) yet.
- The generator's failure rate is also at 50% (1 failure from Query 1, 1 success from Query 2).

**System Resilience:**

- The system demonstrated the first level of fallback for the embedding component, switching to the secondary embedder.
- Despite using a lower-quality embedding (768 dimensions vs. 1536), the system still provided high-quality retrieval and generation.
- The user received a detailed response from the primary generator, showing that fallbacks in earlier stages don't necessarily impact the final output quality if later stages perform well.

**Key Takeaway:**
This example shows how the system can recover from failures in the initial stages of the pipeline. The secondary embedder provided sufficient quality for the retriever to find relevant documents, allowing the generator to produce a high-quality response.



## Query 3: Explain circuit breaker patterns

```plaintext
================================================================================
QUERY: Explain circuit breaker patterns
================================================================================
2025-04-07 20:10:25,935 - HighAvailabilityRAG.System - INFO - Processing query: 'Explain circuit breaker patterns'
2025-04-07 20:10:26,142 - HighAvailabilityRAG.Components.Embedders - WARNING - Primary embedder failed
2025-04-07 20:10:26,142 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component embedder failed: Primary embedding service unavailable
2025-04-07 20:10:26,142 - HighAvailabilityRAG.System - INFO - Trying fallback embedder 1
2025-04-07 20:10:26,356 - HighAvailabilityRAG.Components.Embedders - WARNING - Secondary embedder failed
2025-04-07 20:10:26,356 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component embedder failed: Secondary embedding service unavailable
2025-04-07 20:10:26,356 - HighAvailabilityRAG.System - INFO - Trying fallback embedder 2
2025-04-07 20:10:26,456 - HighAvailabilityRAG.Components.Embedders - INFO - Cached embedder: Retrieved embedding for 'Explain circuit bre...'
2025-04-07 20:10:26,556 - HighAvailabilityRAG.Components.Retrievers - INFO - Primary retriever: Retrieved 3 documents
2025-04-07 20:10:26,756 - HighAvailabilityRAG.Components.Generators - INFO - Primary generator: Generated response for 'Explain circuit bre...'

RESPONSE:
Based on 3 documents including 'Document 12 with detailed information...', the answer to 'Explain circuit breaker patte...' is a detailed explanation with nuanced insights.

SYSTEM HEALTH:
  EMBEDDER:
    state: open
    failure_rate: 0.667
    avg_response_time_ms: 100.000
  RETRIEVER:
    state: closed
    failure_rate: 0.000
    avg_response_time_ms: 100.000
  GENERATOR:
    state: closed
    failure_rate: 0.333
    avg_response_time_ms: 200.000
```

### Analysis of Test Scenarios - Query 3: Explain circuit breaker patterns

**Component Performance:**

- **Embedder**: Both primary and secondary embedders failed, forcing the system to use the cached embedder as a last resort.
- **Retriever**: The primary retriever successfully retrieved 3 documents.
- **Generator**: The primary generator successfully generated a detailed response.

**Circuit Breaker States:**

- The embedder circuit breaker has transitioned to the OPEN state due to a high failure rate (67%, 2 failures out of 3 calls) exceeding both the threshold (40%) and minimum samples (3).
- Other circuit breakers remain CLOSED.

**System Resilience:**

- The system demonstrated multi-tier fallback for the embedding component, going all the way to the third option (cached embedder).
- Despite using the lowest-quality embedding (384 dimensions), the retriever still found relevant documents.
- The primary generator successfully used these documents to create a detailed response.

**Key Takeaway:**
This example illustrates the circuit breaker pattern in action. After multiple failures, the embedder circuit breaker opened, which will cause future requests to bypass the primary and secondary embedders entirely until the recovery timeout period. It also shows how even the lowest-tier fallback can still enable a functional system.



## Query 4: How to implement fallback strategies?

```plaintext
================================================================================
QUERY: How to implement fallback strategies?
================================================================================
2025-04-07 20:10:35,935 - HighAvailabilityRAG.System - INFO - Processing query: 'How to implement fallback strategies?'
2025-04-07 20:10:35,942 - HighAvailabilityRAG.CircuitBreaker - INFO - Circuit for embedder is OPEN, using fallback
2025-04-07 20:10:35,942 - HighAvailabilityRAG.System - INFO - Trying fallback embedder 1
2025-04-07 20:10:36,142 - HighAvailabilityRAG.Components.Embedders - WARNING - Secondary embedder failed
2025-04-07 20:10:36,142 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component embedder failed: Secondary embedding service unavailable
2025-04-07 20:10:36,142 - HighAvailabilityRAG.System - INFO - Trying fallback embedder 2
2025-04-07 20:10:36,256 - HighAvailabilityRAG.Components.Embedders - INFO - Cached embedder: Retrieved embedding for 'How to implement fa...'
2025-04-07 20:10:36,356 - HighAvailabilityRAG.Components.Retrievers - WARNING - Primary retriever failed
2025-04-07 20:10:36,356 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component retriever failed: Primary retrieval service unavailable
2025-04-07 20:10:36,356 - HighAvailabilityRAG.System - INFO - Trying fallback retriever 1
2025-04-07 20:10:36,456 - HighAvailabilityRAG.Components.Retrievers - INFO - Reduced retriever: Retrieved 2 documents
2025-04-07 20:10:36,656 - HighAvailabilityRAG.Components.Generators - WARNING - Primary generator failed
2025-04-07 20:10:36,656 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component generator failed: Primary generation service unavailable
2025-04-07 20:10:36,656 - HighAvailabilityRAG.System - INFO - Trying fallback generator 1
2025-04-07 20:10:36,756 - HighAvailabilityRAG.Components.Generators - INFO - Fallback generator: Generated response for 'How to implement fa...'

RESPONSE:
Based on 2 documents, here's a basic answer to 'How to implement fallback strategi...'

SYSTEM HEALTH:
  EMBEDDER:
    state: half_open
    failure_rate: 0.500
    avg_response_time_ms: 114.000
  RETRIEVER:
    state: closed
    failure_rate: 0.250
    avg_response_time_ms: 100.000
  GENERATOR:
    state: closed
    failure_rate: 0.500
    avg_response_time_ms: 100.000
```

### Analysis of Test Scenarios - Query 4: How to implement fallback strategies?

**Component Performance:**

- **Embedder**: The circuit breaker for the embedder was OPEN from the previous query, so the system immediately tried the secondary embedder, which failed. It then used the cached embedder successfully.
- **Retriever**: The primary retriever failed, so the system used the reduced retriever, which returned fewer documents (2 instead of 3).
- **Generator**: The primary generator failed, so the system used the fallback generator.

**Circuit Breaker States:**

- The embedder circuit breaker has transitioned to HALF_OPEN state, indicating that the recovery timeout period has elapsed and the system is testing if the primary embedder has recovered.
- Other circuit breakers remain CLOSED despite failures, as they haven't exceeded thresholds yet.

**System Resilience:**

- This query demonstrates the most extensive degradation so far, with fallbacks used at every stage of the pipeline.
- The system still produced a coherent response despite using lower-quality components throughout.
- The reduced number of context documents and simpler generator resulted in a more basic response.

**Key Takeaway:**
This example shows how the system can continue functioning even when multiple components fail simultaneously. The multi-tier fallback strategy ensures that users still receive responses, albeit of lower quality, rather than experiencing complete outages.



## Query 5: What is graceful degradation?

```plaintext
================================================================================
QUERY: What is graceful degradation?
================================================================================
2025-04-07 20:10:45,935 - HighAvailabilityRAG.System - INFO - Processing query: 'What is graceful degradation?'
2025-04-07 20:10:45,942 - HighAvailabilityRAG.CircuitBreaker - INFO - Circuit for embedder transitioning to HALF_OPEN
2025-04-07 20:10:46,142 - HighAvailabilityRAG.Components.Embedders - INFO - Primary embedder: Generated embedding for 'What is graceful de...'
2025-04-07 20:10:46,142 - HighAvailabilityRAG.CircuitBreaker - INFO - Circuit for embedder recovering, closing circuit
2025-04-07 20:10:46,356 - HighAvailabilityRAG.Components.Retrievers - WARNING - Primary retriever failed
2025-04-07 20:10:46,356 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component retriever failed: Primary retrieval service unavailable
2025-04-07 20:10:46,356 - HighAvailabilityRAG.System - INFO - Trying fallback retriever 1
2025-04-07 20:10:46,456 - HighAvailabilityRAG.Components.Retrievers - WARNING - Reduced retriever failed
2025-04-07 20:10:46,456 - HighAvailabilityRAG.CircuitBreaker - WARNING - Component retriever failed: Reduced retrieval service unavailable
2025-04-07 20:10:46,456 - HighAvailabilityRAG.System - INFO - Trying fallback retriever 2
2025-04-07 20:10:46,457 - HighAvailabilityRAG.Components.Retrievers - INFO - NoRetriever: No documents retrieved
2025-04-07 20:10:46,656 - HighAvailabilityRAG.Components.Generators - INFO - Primary generator: Generated response for 'What is graceful de...'

RESPONSE:
The answer to 'What is graceful degradation?...' is a detailed explanation without reference documents.

SYSTEM HEALTH:
  EMBEDDER:
    state: closed
    failure_rate: 0.200
    avg_response_time_ms: 200.000
  RETRIEVER:
    state: open
    failure_rate: 0.400
    avg_response_time_ms: 100.000
  GENERATOR:
    state: closed
    failure_rate: 0.400
    avg_response_time_ms: 199.000
```

### Analysis of Test Scenarios - Query 5: What is graceful degradation?

**Component Performance:**
- **Embedder**: The circuit breaker was in HALF_OPEN state, allowing a test of the primary embedder, which succeeded and caused the circuit to close again.
- **Retriever**: Both the primary and reduced retrievers failed, forcing the system to use the NoRetriever fallback, which returns no documents.
- **Generator**: The primary generator successfully generated a response, but without any context documents.

**Circuit Breaker States:**
- The embedder circuit breaker has returned to CLOSED state after a successful test in HALF_OPEN state.
- The retriever circuit breaker has transitioned to OPEN state due to exceeding the failure threshold.
- The generator circuit breaker remains CLOSED.

**System Resilience:**
- This query demonstrates the circuit breaker recovery mechanism, with the embedder circuit successfully transitioning from HALF_OPEN back to CLOSED.
- It also shows the most extreme retrieval degradation, where no context documents are available.
- Despite the lack of context, the primary generator was able to produce a response based solely on the query.

**Key Takeaway:**
This example illustrates the complete circuit breaker lifecycle (CLOSED → OPEN → HALF_OPEN → CLOSED) and shows how the system can provide responses even in the worst-case scenario where no relevant documents are retrieved. The query about "graceful degradation" is itself answered by a system demonstrating that very concept.

