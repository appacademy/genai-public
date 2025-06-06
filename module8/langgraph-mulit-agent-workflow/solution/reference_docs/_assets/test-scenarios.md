# Test Scenarios for Customer Service Inquiry System

To get you started with interacting with the application, this document provides five distinct test scenarios you can use to evaluate the Customer Service Inquiry System. Each scenario is designed to test different aspects of the system based on the context data available in SaaS Solutions Inc.'s knowledge base. Review the "context" documents to get ideas for additional scenarios you can use to interact with the system. Additionally, be sure to read the transcript of the Demo and the example chat session transcript to get a feel for how you can communicate with the application.



## Context Documents

- Customer Support and Company Information - [general_context.md](general_context.md) 
- Urgent Support and Emergency Procedures - [priority_context.md](priority_context.md) 
- Billing and Subscription Guidelines - [billing_context.md](billing_context.md) 
- Product Features and Subscription Tiers - [product_context.md](product_context.md) 
- Technical Support and System Access -  [technical_context.md](technical_context.md)



## Transcripts

- Demo Transcript -  [demo.md](demo.md) 
- Example Chat Session -  [example-chat-session.md](example-chat-session.md) 



## Scenario 1: Billing Inquiry - Double Charge Issue

```
I was charged twice for my Pro subscription on April 1st, and I need a refund for the duplicate charge. My transaction IDs are TX-45678 and TX-45679 for $25 each. [Name: Alex Rivera, Email: alex.r@example.com, Context: Been a customer for 2 years]
```

**Expected Behavior:** 
- Should be classified as a billing inquiry
- Response should reference the company's refund policy (5-7 business days)
- Should acknowledge the Pro plan pricing ($25/month)
- Should mention expedited handling for duplicate charges (1-3 business days)
- Should include personalized greeting with the name "Alex Rivera"
- Should acknowledge the additional context about being a customer for 2 years



## Scenario 2: Technical Support - Account Lockout

```
I'm locked out of my account after trying to reset my password multiple times. I'm using Chrome browser and have 2FA enabled, but I'm not receiving the authentication codes. I have an urgent presentation to clients tomorrow and need access ASAP! [Name: Jordan Smith, Email: jsmith@company.org, Context: Enterprise tier]
```

**Expected Behavior:** 
- Should be classified as a technical inquiry
- May be assigned high priority due to urgency language
- Response should reference browser compatibility (Chrome supported)
- Should include 2FA troubleshooting steps
- Should acknowledge Enterprise tier status for expedited support
- Should mention account lockout procedures and identity verification
- Should include personalized greeting with the name "Jordan Smith"
- Should acknowledge the Enterprise tier context



## Scenario 3: Product Inquiry - Tier Comparison

```
I'm currently on the Basic plan but considering upgrading to either Pro or Enterprise. Can you explain the main differences in storage limits, user counts, and API access between the tiers? Also, do you offer any discounts for annual billing? [Name: Taylor Wong, Context: Small startup with 7 team members]
```

**Expected Behavior:** 
- Should be classified as a product inquiry
- Response should detail the tier differences:
  - Basic (10GB storage, 5 users, 100 API requests/hour)
  - Pro (50GB storage, 25 users, 1,000 API requests/hour)
  - Enterprise (500GB storage, unlimited users, 10,000 API requests/hour)
- Should mention the 15% annual billing discount
- Should note that their 7 team members exceed Basic tier limits (5 users)
- Should include personalized greeting with the name "Taylor Wong"
- Should acknowledge the context about being a small startup with 7 team members



## Scenario 4: General Inquiry - Finding Documentation

```
Where can I find comprehensive documentation about using your platform? I'm specifically looking for information about your privacy policy and security practices for a compliance review our company is conducting. [Name: Morgan Chen, Email: mchen@enterprise.com, Context: New account admin]
```

**Expected Behavior:** 
- Should be classified as a general inquiry
- Response should direct to knowledge base at support.ourcompany.com
- Should mention privacy policy at www.ourcompany.com/privacy
- Should reference security practices (encryption, SOC 2 compliance, etc.)
- Should acknowledge their context as a new account admin
- Should include personalized greeting with the name "Morgan Chen"
- Should provide specific links to documentation resources



## Scenario 5: Priority/Emergency - Data Loss Issue

```
EMERGENCY! All our client data has disappeared from our account dashboard and we're showing $0 balance. We have over 50 users affected and critical client meetings tomorrow. This is a major business impact situation! [Name: Sam Johnson, Email: sjohnson@megacorp.com, Context: Enterprise customer since 2020]
```

**Expected Behavior:** 
- Should be classified as an urgent/priority issue
- May be classified as technical or billing (either is reasonable)
- Response should acknowledge the severe impact and urgency
- Should reference emergency response protocols
- Should mention regular status updates (every 30 minutes)
- Should note incident manager assignment
- Should provide the emergency contact number (1-800-555-9999)
- Should include personalized greeting with the name "Sam Johnson"
- Should acknowledge the context about being an Enterprise customer since 2020



## Testing Instructions

1. Run the application using `python app.py`
2. Copy and paste each scenario exactly as written, including the bracketed user information
3. Evaluate the response against the expected behavior criteria
4. Pay special attention to:
   - Classification accuracy
   - Personalization elements
   - Appropriate policy references
   - Correct tier-specific information
   - Emma G.'s signature format

These test scenarios cover the full range of inquiry types and will demonstrate the application's ability to properly classify, route, and respond to different customer needs while incorporating personalization based on the user information provided.
