# RAG Resilience Patterns Explained

This document sheds light on the technical details of our high-availability RAG simulation system, focusing on the circuit breaker pattern and its components—embedders, retrievers, and generators. Keep in mind that the specifics here are tailored for this exercise to illustrate key concepts, not to mirror the exact standards of large-scale, real-world RAG-enabled AI systems.



## Circuit Breaker Pattern

The circuit breaker pattern is a resilience design pattern that prevents cascading failures in distributed systems. It's named after electrical circuit breakers that automatically interrupt electrical flow when a fault is detected.



### How Circuit Breakers Work in Our System

Each major component in our RAG pipeline (embedder, retriever, and generator) has its own independent circuit breaker that:

1. **Monitors component health**: Tracks success/failure rates and response times
2. **Manages state transitions**: Moves between three distinct states based on component performance
3. **Routes requests appropriately**: Either to the primary component or to fallbacks



### Circuit Breaker States

Our circuit breakers operate in three states:

1. **CLOSED** (normal operation)
   - All requests go to the primary component.
   - Failures are tracked but don't trigger special handling.
   - This is the default starting state.

2. **OPEN** (failure mode)
   - Primary component is bypassed completely.
   - All requests are immediately routed to fallbacks.
   - Triggered when failure rate exceeds threshold.
   - Remains in this state for a recovery timeout period.

3. **HALF_OPEN** (recovery testing)
   - After the recovery timeout expires, the circuit enters this state.
   - A single request is sent to the primary component as a test.
   - If successful, circuit returns to CLOSED state.
   - If it fails again, circuit returns to OPEN state for another timeout period.



### Circuit Breaker Configuration

In our implementation, each circuit breaker is configured with:

- `failure_threshold = 0.4`: When 40% or more of attempts fail, the circuit may open.
- `min_samples = 3`: Need at least 3 total attempts before making a decision.
- `recovery_timeout = 10`: After opening, wait 10 seconds before trying the half-open state.



### Triggering Conditions

A circuit breaker transitions from CLOSED to OPEN when:
1. At least `min_samples` (3) calls have been made to the component.
2. The failure rate equals or exceeds the `failure_threshold` (40%).

For example, if 2 out of 5 calls fail (40% failure rate), the circuit will open, and subsequent requests will bypass the primary component until the recovery timeout period.



## Component Implementations

Our RAG system implements multiple tiers of components with different performance characteristics, allowing for graceful degradation when failures occur.



### Embedders

Embedders convert text (queries and documents) into numerical vector embeddings that capture semantic meaning.

1. **PrimaryEmbedder**
   - Highest quality embeddings (1536 dimensions)
   - Simulates a large, high-quality embedding model like OpenAI's text-embedding-ada-002
   - Moderate response time (50-200ms)
   - Higher failure rate (30% in our simulation)
   - Best semantic understanding but least reliable

2. **SecondaryEmbedder**
   - Medium quality embeddings (768 dimensions)
   - Simulates a medium-sized embedding model like MPNet or BERT-based models
   - Slightly slower response time (100-300ms)
   - Lower failure rate (15% in our simulation)
   - Good balance between quality and reliability

3. **CachedEmbedder**
   - Lowest quality embeddings (384 dimensions)
   - Simulates pre-computed embeddings stored in a cache
   - Near-instant response time
   - Never fails (100% reliability)
   - Limited semantic understanding but always available



### Retrievers

Retrievers use the embedded query vector to find semantically similar documents in a vector database.

1. **PrimaryRetriever**
   - Returns comprehensive results (up to 20 high-quality documents)
   - Simulates a full-featured vector database with rich metadata
   - Moderate response time (100-300ms)
   - Higher failure rate (30% in our simulation)
   - Best retrieval quality but least reliable

2. **ReducedRetriever**
   - Returns fewer results (up to 10 medium-quality documents)
   - Simulates a simplified vector database with basic functionality
   - Faster response time (50-150ms)
   - Lower failure rate (15% in our simulation)
   - Reduced context but more reliable

3. **NoRetriever**
   - Returns no documents (empty context)
   - Simulates a last-resort fallback when all retrieval options fail
   - Instant response time
   - Never fails (100% reliability)
   - Forces the generator to work without context



### Generators

Generators take the user query and retrieved 'context documents' and generate a response via an LLM.

1. **PrimaryGenerator**
   - Produces detailed, nuanced responses
   - Simulates a large language model like GPT-4 or Claude
   - Slower response time (200-500ms)
   - Higher failure rate (30% in our simulation)
   - Best response quality but least reliable

2. **FallbackGenerator**
   - Produces simpler, more basic responses
   - Simulates a smaller language model like GPT-3.5 or Llama 2
   - Faster response time (100-250ms)
   - Lower failure rate (15% in our simulation)
   - Reduced quality but more reliable

3. **TemplateGenerator**
   - Produces template-based responses with minimal customization
   - Simulates a rule-based fallback system with no LLM
   - Instant response time
   - Never fails (100% reliability)
   - Limited usefulness but always available



## Fallback Strategy

The fallback strategy defines the degradation pathway for each component type. When a primary component fails, the system automatically tries the next component in the fallback chain.



### Fallback Chain Execution

1. When a component fails, its circuit breaker records the failure.
2. If the failure rate exceeds the threshold, the circuit opens.
3. Subsequent requests are routed to the fallback chain.
4. The system tries each fallback in order until one succeeds.
5. If all fallbacks fail, a default response is returned.



### Graceful Degradation

This multi-tiered approach allows the system to degrade gracefully rather than fail completely:

- If the primary embedder fails, the system can still use the secondary embedder.
- If both embedding services fail, it can fall back to cached embeddings.
- If all retrievers fail, the generator can still attempt to answer without context.
- If all generators fail, the system can still return a template response.

This ensures that users receive some response, even if it's not the highest quality, rather than experiencing a complete system outage.



## System Health Monitoring

The system tracks health metrics for each component, including:

1. **State**: The current circuit breaker state (closed, open, half-open)
2. **Failure Rate**: The percentage of requests that have failed
3. **Average Response Time**: The average time taken to process requests

These metrics provide visibility into the system's performance, and help identify which components are experiencing issues.



## Practical Example

Here's a practical example of how the system handles failures:

1. A user submits a query about "circuit breaker patterns".
2. The primary embedder attempts to convert this to an embedding.
3. If it fails and the circuit is still closed, the system tries again with the 'primary embedder.'
4. After several failures (≥40% failure rate across ≥3 samples), the embedder circuit opens.
5. Subsequent embedding requests go directly to the 'secondary embedder.'
6. If the secondary embedder also fails, the system tries the 'cached embedder.'
7. Once an embedding is obtained, the system proceeds to retrieval and generation.
8. Each step follows the same pattern of trying primary components first, then falling back as needed.
9. The user receives a response, potentially of lower quality, if fallbacks were used.
10. After the recovery timeout (10 seconds), the system tests the primary embedder again.

This approach ensures that temporary failures don't cause complete system outages and that the system can recover automatically when components return to normal operation.

