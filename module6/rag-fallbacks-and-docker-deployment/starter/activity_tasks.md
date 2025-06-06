## Activity Tasks

### Task 1: RAG Component Implementation (30 minutes)

1. **Required Reading**: Review the `_assets/rag-resilience-patterns-explained.md` document to understand the architecture and resilience patterns used in the system. Get a feel for the Circuit Breaker pattern and the three core components that form the foundation of our RAG system:
   - **Embedders**: Convert text to vector representations
   - **Retrievers**: Find relevant documents using embeddings
   - **Generators**: Create text responses using queries and context

2. **Implement the Embedder Components**:
   - Open `components/embedders.py` in your code editor
   - Follow the TODOs to implement:
     - The `PrimaryEmbedder` class (Task 1a) - Initialize with configurable failure rate, implement the embed method to generate normalized embedding vectors, and implement the dimension property
     - The `SecondaryEmbedder` class (Task 1b) - Implement failure simulation and processing time handling
     - The `CachedEmbedder` class (Task 1c) - Implement the cache mechanism for embeddings using key-based storage

3. **Implement the Retriever Components**:
   - Open `components/retrievers.py` in your code editor
   - Follow the TODOs to implement:
     - The `PrimaryRetriever` class (Task 1d) - Initialize the document store, implement failure simulation, and create the document retrieval logic
     - The `ReducedRetriever` class (Task 1e) - Modify the max_docs calculation to limit results to at most min(top_k, 2)
     - The `NoRetriever` class (Task 1f) - Implement the fallback retriever that always returns an empty list

4. **Implement the Generator Components**:
   - Open `components/generators.py` in your code editor
   - Follow the TODOs to implement:
     - The `PrimaryGenerator` class (Task 1g) - Implement failure simulation, processing time, and contextual response generation
     - The `FallbackGenerator` class (Task 1h) - Create simpler responses for both context and no-context cases
     - The `TemplateGenerator` class (Task 1i) - Complete the template-based fallback generator

### Task 2: Circuit Breaker Implementation (30 minutes)

1. Understand the Circuit Breaker pattern in `core/circuit_breaker.py`:
   - Study the three circuit states: CLOSED (normal), OPEN (failing), and HALF_OPEN (testing recovery)
   - Examine how the CircuitBreaker monitors component health via the ComponentStatus class
   - Identify how failures are tracked and how they influence circuit state transitions

2. Implement the **recovery timeout check** in the execute method:
   - Replace the placeholder condition to check if enough time has passed since the circuit opened
   - Use the recovery_timeout property and last_state_change_time to determine if a recovery attempt should be made
   - When the timeout has elapsed, transition the circuit from OPEN to HALF_OPEN state

3. Implement the **circuit opening logic** in the exception handling section:
   - Replace the placeholder condition to detect when a circuit should open
   - Check if:
     - There are sufficient samples (total_calls >= min_samples)
     - The failure rate exceeds the threshold (status.get_failure_rate() >= failure_threshold)
     - The current state is CLOSED
   - If all conditions are met, transition to the OPEN state

4. Test the circuit breaker behavior by executing the application and observing how:
   - Circuits open after consecutive failures
   - Recovery is attempted after the timeout period
   - Circuits return to the CLOSED state if recovery succeeds

### Task 3: Fallback Strategy Development (30 minutes)

1. Examine the fallback chain architecture in `core/strategy.py`:
   - Understand how the FallbackStrategy class organizes fallback options
   - Study the relationship between ComponentType enums and component instances

2. Complete the **FallbackStrategy initialization** in `core/strategy.py`:
   - Initialize the fallback_chains dictionary with ComponentType keys
   - Map each component type to its corresponding list of implementations
   - Use ComponentType.EMBEDDER, ComponentType.RETRIEVER, and ComponentType.GENERATOR as keys
   - Assign the constructor parameters (embedders, retrievers, generators) as values

3. Implement the **final fallback mechanism** in the `get_embedding` method in `system.py`:
   - Complete the empty fallback return statement in try_fallback_embedder
   - Create a zero vector with the same dimension as the primary embedder
   - Use embedders[0].dimension to determine the correct size

4. Complete the **RAG pipeline** in the query method in `system.py`:
   - Implement Step 1: Call self.get_embedding with the user_query
   - Implement Step 2: Call self.get_relevant_documents with the embedding and top_k=3
   - Implement Step 3: Call self.generate_response with the query and retrieved documents
   - Return the generated response to the user

5. Test the complete fallback strategy by executing the application and observing:
   - How primary services fail and trigger fallbacks
   - The degradation in quality as fallbacks are used
   - The system's ability to continue functioning despite multiple failures
