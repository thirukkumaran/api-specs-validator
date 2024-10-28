<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 5. Quality Assurance and Testing

Build APIs that meet quality standards

> **Purpose**: To clearly set standards for assuring API quality using established testing practices and tools.

<br></br>
The standards is intended to help people in the Government building APIs to:

- ensure that APIs are tested for functionality and security regularly
- ensure that APIs meet industry standards (eg. OWASP) for compliance
- ensure that APIs are tested and scaled to user and traffic needs

<br></br>

Quality assurance and testing is crucial to ensure that your APIs perform optimally, are secure, resilient, reliable and are in line with the industry’s best practices.

Be sure to include the mentioned API testing in your organization's CI/CD pipelines to have the confidence that your APIs are ready for production. At a minimum, conduct these tests before deploying your APIs, and terminate your pipelines should any of these tests fail.

<br></br>
<br></br>

## 5.1 API Linting Enforcement

API Linting involves analyzing your API code and artefacts to identify and rectify issues early in the development process, especially if incorporated as part of **CI/CD**. This ensures consistency, adherence to coding standards, and helps prevent common errors.

### `ASG 5.1.1` Adopt an API Linting tool

Choose a reliable API Linting tool compatible with your programming language and framework. [Spectral](https://stoplight.io/open-source/spectral) is an open-source API style guide enforcer and linter that we recommend.

### `ASG 5.1.2` Configure linting rules and its severity

Review and configure the linting tool to your project or organization requirements with regards to coding standards, formatting rules, and any specific guidelines that your APIs should have.

There should also be a clear distinction in severity for linting rule violations. The most severe ones, like exposing sensitive information in a public API, must be flagged and block the release in the pipeline. The less severe violations may generate warnings to the developers about areas where their APIs deviate from best practices.

### `ASG 5.1.3` Integrate API Linting into your CI/CD process

Integrate the linting process into your (CI/CD) pipeline(s). This ensures that code or any API artefacts are automatically checked during the development lifecycle.

### `ASG 5.1.4` Review your API Linting rules periodically

As your organization grows and creates more APIs, it is recommended to have regular code reviews for your API Linters. This helps address linting issues (like outdated rulesets) and opportunities together, especially as new business cases emerge.

<br></br>

## 5.2 API Contract Testing

It is important to ensure **quality assurance** as APIs progress from version to version. This is as any unintended or unexpected changes across versions can break an end-user's application.

### `ASG 5.2.1` Validating API Contract

Ensure that API Contract and functionality work from version to version and is able to perform the required functionality and return the success/error codes reliably. This should also be validated with load and large load.

<br></br>

## 5.3 OWASP API Security Top 10 Testing

Scan the APIs for security compliance, (eg. OWASP API Security Top 10), periodically and ideally incorporating into the CI/CD pipeline.

### `ASG 5.3.1` Validating OWASP API Security with security tools

The **[OWASP API Security Top 10](https://owasp.org/www-project-api-security/)** is a list of the most critical security risks to API. Performing OWASP testing on your APIs helps identify and address potential **security** **vulnerabilities**.

Utilize security testing tools such as OWASP ZAP or Burp Suite to check your API for vulnerabilities. Make sure to validate these tools with your internal security teams or experts to ensure if there is comprehensive coverage.

Since these tests focus on security, it's crucial to terminate any API deployments immediately if there's a failure.

<br></br>

## 5.4 Performance Testing

Performance testing assesses how well your API functions under different conditions to ensure it can handle [expected loads](#asg-541-define-and-review-performance-metrics). Essentially, it checks if your API's infrastructure is prepared to reliably handle varying levels or peaks of user activity.

### `ASG 5.4.1` Define and Review Performance Metrics

Identify key performance metrics such as response time, throughput, and server error rates. These metrics serve as good benchmarks on setting rate-limits to your production APIs to safeguard against overuse. Overtime, you can review these metrics through analytics of your API or anticipate heavier load/usage due to specific anticipated events.

### `ASG 5.4.2` Adopt Performance Testing Tools

You API development team should adopt performance testing tools like Apache JMeter, Gatling, or Locust for simulating realistic user loads and measuring performance according to defined metrics (ASG 5.3.1). As your performance metrics evolve and change overtime, your selected tooling should be ready to conduct “retests” to validate the new metrics.

### `ASG 5.4.3` Conducting Load & Stress Testing

Conduct load testing to evaluate your API's performance under **normal** and **expected** **load** **conditions**.

During API development, performance in a production environment is often overlooked as it is initially created in a local development setting. However by having load testing as part of your testing suite, you will be able to identify performance bottlenecks, assess response times and ensures the API meets expected performance metrics under typical usage in production.

For better clarity and confidence of your API, perform stress testing to determine the limits of your API by subjecting it to loads **beyond its capacity**. Stress testing validates if your API can withstand high traffic, unexpected usage spikes, and many concurrent queries without crashing or drastically slowing down.

### `ASG 5.4.4` When to Conduct Stress Testing?

Load Testing should be part of your regular CI/CD process, or at the very least, when there are [major/minor changes](https://semver.org/) your to APIs, or when there are major events in the organization which will expect a spike in API usage.

Generally, you should consider conducting stress testing when there are major underlying changes to your infrastructure that hosts your APIs as these tests could be costly when done frequently.
