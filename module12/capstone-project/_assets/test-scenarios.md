# Jenna HR Assistant - Test Scenarios

The following is a comprehensive set of test scenarios you can use to verify your implementation of the Jenna HR Assistant system. These scenarios cover the key functionality of each part of the system. Each test includes the expected console output to help you confirm that your implementation is working correctly. Use these scenarios to systematically test the various features of your HR assistant.


## 1. Basic Policy Question

- **Input**: "What is our company's policy on remote work?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Policy QA completed in X.XXXs
    
    Jenna:
    Based on our company's remote work policy, here are the key points:
    
    ## Remote Work Policy Overview
    
    • Eligible employees can work from home up to 3 days per week with manager approval
    • Remote work requests must be submitted at least 1 week in advance
    • [Additional policy details will be displayed]
    
    For full details, please refer to the Employee Remote Work Policy document.
    ```
    

### 2. Benefits Question with Sensitive Topic

- **Input**: "What mental health resources are available to employees?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Benefits QA completed in X.XXXs
    
    Jenna:
    Our company offers several mental health resources as part of our Employee Assistance Program (EAP) and wellness benefits:
    
    ## Mental Health Resources
    
    ### Employee Assistance Program (EAP)
    • Free, confidential counseling services (up to 8 sessions per issue per year)
    • 24/7 crisis hotline: 1-800-555-EAP1
    • [Additional mental health resources will be listed]
    
    All services are completely confidential, and your privacy is protected by law.
    ```
    

### 3. Training Record Lookup

- **Input**: "Show me my training record"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Training lookup completed in X.XXXs
    
    Jenna:
    Here's your current training record:
    
    • HR-001: Workplace Ethics & Code of Conduct - Completed (Enrolled: 2024-10-15, 2024-11-05) - Due: 2025-11-05
    • HR-002: Preventing Harassment & Discrimination - Not Started (Enrolled: 2024-11-05, Not completed) - Due: 2025-11-05
    • [Additional training courses will be listed]
    
    A snapshot of your training record has been saved to data/training/snapshots\[EMPLOYEE_ID]_[TIMESTAMP].csv.
    ```
    

## 4. Course Catalog Query

- **Input**: "What courses are available for enrollment?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Training courses completed in X.XXXs
    
    Jenna:
    ## Available Courses
    
    ### Mandatory Courses:
    • HR-001: Workplace Ethics & Code of Conduct (Required, 12-month renewal)
    • HR-002: Preventing Harassment & Discrimination (Required, 12-month renewal)
    • SEC-010: Cyber-Security Awareness Basics (Required, 6-month renewal)
    
    ### Elective Courses:
    • AI-201: Introduction to Machine Learning (Elective)
    • [Additional elective courses will be listed]
    
    To enroll in a course, type "Enroll me in [COURSE-ID]" (e.g., "Enroll me in AI-201").
    ```
    

## 5. Course Enrollment

- **Input**: "Enroll me in SEC-230 and AI-201"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Training enrollment completed in X.XXXs
    
    Jenna:
    You've been successfully enrolled in all 2 courses:
    
    • SEC-230
    • AI-201
    ```
    

## 6. Course Completion Update

- **Input**: "I completed HR-001 and SEC-010 yesterday"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Training update completed in X.XXXs
    
    Jenna:
    Great job! I've marked all 2 courses as completed:
    
    • HR-001
    • SEC-010
    ```
    

## 7. HR Employee Directory Access (Authorized)

- **Input**: "Show employee roster" (as Jane Doe, E002)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR employee directory access completed in X.XXXs
    
    Jenna:
    ## EMPLOYEE DIRECTORY
    
    • E001: Alice Johnson - HR, HR Specialist (Started: 2024-01-15)
    • E002: Jane Doe - HR, HR Specialist (Started: 2024-04-22)
    • [Additional employees will be listed]
    
    This information is confidential and should only be accessed by HR personnel.
    ```
    

## 8. HR Employee Directory Access (Unauthorized)

- **Input**: "Show employee roster" (as any employee other than Jane Doe)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR employee directory access completed in X.XXXs
    
    Jenna:
    Only the HR representative (Jane Doe, E002) can access the employee directory. Please contact HR if you need this information.
    ```
    

## 9. HR Analytics - Course Completion

- **Input**: "How many people have completed the HR-001 course?" (as Jane Doe, E002)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR analytics completed in X.XXXs
    
    Jenna:
    ## HR-001 Course Completion Analysis
    
    • Total Enrollments: 21
    • Completed: 8 (38.1%)
    • Not Completed: 13 (61.9%)
    
    ### Employees Who Haven't Completed HR-001:
    • Carlos Rodriguez (E003): Not Started
    • Frank Miller (E006): In Progress
    • [Additional employees will be listed]
    ```
    

## 10. HR Analytics - Department Breakdown

- **Input**: "Show me department breakdown" (as Jane Doe, E002)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR analytics completed in X.XXXs
    
    Jenna:
    ## Department Analysis
    
    Total Employees: 21
    
    • Engineering: 6 employees (28.6%)
    • HR: 3 employees (14.3%)
    • [Additional departments will be listed]
    
    ### Training Completion by Department
    
    **Engineering**:
    • Course Enrollments: 24
    • Completed: 14 (58.3%)
    
    [Additional department training statistics will be listed]
    ```
    

## 11. Bulk Employee Addition

- **Input**: "Add these employees: E022 Robert Chen Engineering Software Engineer, E023 Sarah Kim Marketing Content Strategist" (as Jane Doe, E002)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR bulk employee addition completed in X.XXXs
    
    Jenna:
    ## BULK EMPLOYEE ADDITION SUCCESSFUL
    
    Successfully added 2 out of 2 employees.
    
    ### Successfully Added:
    • E022: Robert Chen
    • E023: Sarah Kim
    
    ## MANDATORY TRAINING ENROLLMENT
    
    ### Robert Chen (E022):
    • Enrolled in HR-001
    • Enrolled in HR-002
    • Enrolled in SEC-010
    
    ### Sarah Kim (E023):
    • Enrolled in HR-001
    • Enrolled in HR-002
    • Enrolled in SEC-010
    ```
    

## 12. Employee Update

- **Input**: "Update employee E021 role to Department Manager" (as Jane Doe, E002)
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    HR employee update completed in X.XXXs
    
    Jenna:
    ## EMPLOYEE UPDATE SUCCESSFUL
    
    Successfully updated employee E021.
    
    ### Updated Information:
    • Employee ID: E021
    • Name: Emma Jackson
    • Department: Research
    • Role: Department Manager
    • Start Date: 2025-04-29
    ```
    

## 13. Comparative Policy Question

- **Input**: "What's the difference between PTO and sick leave?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    Original query: 'What's the difference between PTO and sick leave?'
    Expanded query: 'What's the difference between PTO and sick leave? paid time off vacation leave holiday sick sick leave illness medical health'
    
    Detected comparative question about: pto, sick
    
    Retrieved X documents for query: 'What's the difference between PTO and sick leave?'
    [Document retrieval details will be shown]
    
    Comparative query detected, returning all documents
    
    Using specialized comparative question prompt
    
    Policy QA completed in X.XXXs
    
    Jenna:
    # PTO vs. Sick Leave: Key Differences
    
    ## Paid Time Off (PTO)
    • Purpose: For vacation, personal days, and general time off
    • Allocation: X days per year, accrued at X days per month
    • Approval: Requires manager approval at least X days in advance
    • [Additional PTO details will be shown]
    
    ## Sick Leave
    • Purpose: Specifically for illness, medical appointments, and health-related absences
    • Allocation: X days per year, separate from PTO
    • Approval: No advance approval needed for unexpected illness
    • [Additional sick leave details will be shown]
    
    ## Key Differences
    • [Comparison points between the two policies will be listed]
    
    According to our Employee PTO Policy and Sample Company Sick Leave Policy documents, these benefits are tracked and managed separately.
    ```
    

## 14. Relationship Question

- **Input**: "Does maternity leave count against my PTO balance?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    [Document retrieval details will be shown]
    
    Using specialized comparative question prompt
    
    Policy QA completed in X.XXXs
    
    Jenna:
    No, maternity leave does NOT count against your PTO balance. According to our Parental Leave Company Policy, maternity leave is a separate benefit that provides [X] weeks of paid leave following childbirth or adoption.
    
    This is completely separate from your PTO balance, which remains intact during your maternity leave. You will continue to accrue PTO while on maternity leave as stated in section [X] of the policy.
    
    [Additional details about maternity leave will be shown]
    ```
    

## 15. Follow-up Question Sequence

- **Sequence**:
    1. Ask: "What is our bereavement leave policy?"
    2. Then ask: "How do I request it?"
- **Expected Console Output for Second Question**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    Detected follow-up question. Including previous context.
    
    Using specialized follow-up question prompt
    
    Policy QA completed in X.XXXs
    
    Jenna:
    To request bereavement leave, you need to follow these steps:
    
    1. Notify your manager as soon as possible about your need for bereavement leave
    2. Submit a formal request through the HR portal under "Leave Requests"
    3. [Additional request steps will be listed]
    
    According to our Bereavement Leave Company Policy, you may be asked to provide documentation such as an obituary or funeral program upon your return.
    ```
    

## 16. Sensitive Topic Handling

- **Input**: "What resources do we have for employees with substance abuse issues?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    [Document retrieval details will be shown]
    
    Substance abuse query detected, returning all documents
    
    Using specialized sensitive topic prompt
    
    Policy QA completed in X.XXXs
    
    Jenna:
    Our company offers several confidential resources to support employees dealing with substance abuse issues:
    
    ## Support Resources
    
    ### Employee Assistance Program (EAP)
    • Free, confidential counseling services (up to X sessions)
    • 24/7 confidential helpline: [phone number]
    • Access to specialized addiction counselors and treatment referrals
    
    ### Health Insurance Coverage
    • Coverage for rehabilitation programs and addiction treatment
    • [Additional coverage details will be listed]
    
    All requests for help are kept strictly confidential. Seeking assistance will not negatively impact your employment status, and early intervention is encouraged.
    
    According to our Substance Abuse Company Policy and Employee Assistance Program documents, the company is committed to supporting employees seeking help.
    ```
    

## 17. Mandatory Training Enrollment

- **Input**: "Sign me up for all mandatory courses"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Mandatory training enrollment completed in X.XXXs
    
    Jenna:
    I've processed your mandatory training enrollment:
    
    • Enrolled in HR-001
    • Enrolled in HR-002
    • Enrolled in SEC-010
    ```
    

## 18. Fallback for Non-HR Queries

- **Input**: "What's the weather like today?"
- **Expected Console Output**:
    
    ```javascript
    Intent classification completed in X.XXXs
    Fallback completed in X.XXXs
    
    Jenna:
    I'm sorry, I can only help with HR-related questions and tasks. I can assist with policies, benefits, or training - what would you like to know? Type 'help' to see what I can do.
    ```
    

## 19. Multi-Turn Conversation with Topic Switch

- **Sequence**:
    1. Ask: "What is our company's policy on remote work?"
    2. Then ask: "How many days per week can I work remotely?"
    3. Then switch topics: "Tell me about our health insurance benefits"
- **Expected Console Output for Third Question**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    [Document retrieval details will be shown]
    
    Health benefit query detected, returning all documents
    
    Using standard QA prompt
    
    Benefits QA completed in X.XXXs
    
    Jenna:
    Our company offers a comprehensive health insurance package that includes:
    
    ## Health Insurance Benefits
    
    • Medical coverage through [Provider Name]
    • Dental and vision plans
    • Prescription drug coverage
    • [Additional health benefits will be listed]
    
    According to our Employee Benefits and Perks document, the company covers 80% of the premium costs for employees and 50% for dependents.
    
    [Additional details about enrollment, coverage options, etc. will be shown]
    ```
    

## 20. Mixed Intent Conversation

- **Sequence**:
    1. Ask: "What courses are available for enrollment?"
    2. Then ask: "Enroll me in SEC-230"
    3. Then ask: "What is our company's PTO policy?"
- **Expected Console Output for Third Question**:
    
    ```javascript
    Intent classification completed in X.XXXs
    
    [Document retrieval details will be shown]
    
    PTO query detected, returning all documents
    
    Using standard QA prompt
    
    Policy QA completed in X.XXXs
    
    Jenna:
    According to our PTO policy:
    
    ## PTO Policy Highlights
    
    • Full-time employees receive X days of PTO per year
    • PTO accrues at a rate of X days per month
    • Unused PTO [details about rollover or expiration]
    • Requests must be submitted at least X business days in advance
    • [Additional PTO policy details will be shown]
    
    For more information, please refer to the Employee PTO Policy document.
    ```
    

These 20 test scenarios cover the essential functionality of the Jenna HR Assistant system and provide clear expectations for the console output that students should see when testing their implementations.