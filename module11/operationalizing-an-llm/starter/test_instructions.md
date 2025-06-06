# Testing the Complete System

This file provides instructions for testing your implementation of the LLM middleware system. Follow these steps to verify that all components work together correctly and handle failure scenarios gracefully.

## TODO: Test normal operation

1. Run the application without any special parameters:
   ```bash
   python main.py
   ```

2. Observe the successful primary model response
   - Check the console output for the LLM's response
   - Verify the response is coherent and relevant to the prompt

3. Check the response metadata
   - Confirm that `fallback_used` is set to `false`
   - Verify that the correct model name is shown in `model_used`

4. Verify performance metrics are being logged
   - Look for latency measurements in the console output
   - Check token usage statistics
   - Confirm that anomaly scores are calculated and displayed

## TODO: Test fallback scenarios

1. Test the first fallback mechanism:
   ```bash
   python main.py --test_force_first_fallback_fail
   ```
   
   - Verify the system correctly falls back to the secondary model
   - Check that `fallback_level: 1` appears in the response metadata
   - Confirm that appropriate warning logs are generated

2. Test the complete fallback chain:
   ```bash
   python main.py --test_force_all_models_fail
   ```
   
   - Verify the rule-based fallback is triggered
   - Check that `fallback_level: 2` appears in the response metadata
   - Confirm that the rule-based response is appropriate for the prompt

3. Verify all fallback levels are properly logged
   - Look for warning messages indicating fallback activation
   - Check that each fallback level is clearly indicated in the logs
   - Confirm that original error information is preserved

## TODO: Analyze overall system behavior

1. Review the generated logs in `llm_app.log`
   - Open the log file and examine its contents
   - Look for structured log entries with consistent formatting
   - Verify that log levels are used appropriately (INFO, WARNING, ERROR)

2. Check that request_id is consistent throughout each request's lifecycle
   - Find a specific request_id in the logs
   - Trace it through the entire request processing flow
   - Confirm that all log entries for the same request share the same ID

3. Examine the performance statistics at the end of the run
   - Look for the summary statistics displayed after all tests
   - Check metrics like average latency, token usage, and anomaly counts
   - Compare statistics across different test runs

4. Verify the fallback_rate reflects how often fallbacks were used
   - Check that the fallback_rate increases when forcing fallbacks
   - Confirm that the rate matches the expected value based on your tests
   - Verify that high_anomaly_count is incremented for anomalous responses

## Additional Testing Tips

- Try modifying the prompt to test different types of requests
- Experiment with different parameter values (temperature, max_tokens)
- Test the system under high load by running multiple requests in quick succession
- Check memory usage during extended test runs to identify potential leaks
