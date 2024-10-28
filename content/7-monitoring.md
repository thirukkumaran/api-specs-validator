<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 7. Monitoring, Analytics, and Key Performance Indicators

Monitor your APIs for performance optimization and for detecting fraudulent activity

> **Purpose**: To clearly set standards for API efficacy via defining metrics, monitoring mechanisms, and analytics to track API health, performance and usage.

<br></br>
The standards is intended to help people in the Government building APIs to:

- ensure that logging to implemented to monitor API performance and for fraud detection
- ensure that there is ample logging for APIs as this may mean service or experience degradation for client applications

<br></br>

## 7.1 Monitoring

API Monitoring is a critical function in API governance. The objective is to provide real-time visibility on your overall health, reliability and usability of your APIs as it is being actively consumed in production client applications.

Today, you can choose widely used monitoring tools like:

- Kibana
- Grafana
- Datadog
- New Relic

### `ASG 7.1.1` Identifying Key Monitoring Metrics

Recommended below are monitoring metrics to give your API teams clear and useful datapoints to observe how well and reliable are your APIs:

- **Latency/Response Time:** Measure the time it takes for the API to respond to requests. Breaking down the total response time between each API chain will be beneficial to identify areas for optimisation
- **Error Rates:** Identify and investigate errors in API responses. High error rates may indicate issues with the API, such as bugs, connectivity problems, or incorrect client requests.
- **Uptime/Downtime:** Ensure continuous availability and detect downtime promptly.
- **Traffic Volume:** Monitor the volume of incoming requests.
- **Resource Utilization:** Monitors resource consumption (relating to CPU, memory and disk usage) to ensure optimal performance and informs scaling decisions.
- **Security Anomalies:** Metrics related to security events, such as failed login attempts, unauthorized access, or attempted code/script injections.

<br></br>

### `ASG 7.1.2` Handling API Logging

API logs play a critical role in the monitoring process, providing a detailed record of activities and interactions within each API call. These logs capture important information such as requests, responses, errors, timestamps, transaction IDs and various other metadata to describe the API call as it happens.

As a good rule of thumb, in order to achieve (minimally) the key monitoring metrics above, your logs should include the following details:

- **Timestamp:** Each log entry is timestamped, allowing for a chronological view of API activities. This is crucial for analyzing the sequence of events and identifying patterns over time.
- **Status Codes:** HTTP status codes are logged, indicating the outcome of each API request. Monitoring these codes provides insights into the success or failure of requests.
- **API Pathname and Version:** The actual API path that is being invoked. This detail is useful as you can filter logs by pathname, allowing for a collective observation of patterns associated with a particular API over time.
- **Error Responses:** API logs capture error messages and details when issues occur. Monitoring these error logs helps quickly identify and address any issues affecting the API's functionality.

!> However, it is crucial to note that logging every detail isn't necessary. In fact, certain information must **be deliberately excluded from logs**, achieved through either omission or data redaction.

**Details that must be excluded/redacted**:

- Personal Identifiable Information (PII) data of requests body
- Sensitive Business data of request body
- Security headers (like API keys, tokens, or any other authentication credentials)

<br></br>

## 7.2 Key Performance Indicators (KPI)

Expanding on monitoring, we should also measure the API's Key Performance Indicators (KPIs). These are specific metrics that assess how well the API program or strategy is performing and if it's meeting the organization's goals.

### `ASG 7.2.1` Identifying Key Performance Indicators

KPIs are different from monitoring metrics because they aren't fixed or predictable. Each API aims to achieve specific business goals, which have their own unique ways of measuring success. You can use the concepts below as a starting point for crafting your API KPIs, but ultimately, it's up to your API Product team or stakeholders to decide which measurements are meaningful for defining the API's success.

- **API Usage Volume by User:** By adding up how many times each type of user makes API calls, you can see how different groups of users use the API and with what kind of consumption volume/rate. Additionally, you can create a customer segmentation map to group users based on their demographics.
- **API Consumer Sentiments:** Gathering feedback from your consumers helps assess how effectively your API meets their needs. Using a rating scale can organize feedback into positive and negative categories and what to prioritize on for future releases.
- **API Stakeholder Sentiments or Organization Data Points:** The organization's API stakeholders provide valuable feedback on whether the API aligns with its intended strategy. They offer insights from various data points they manage, such as profits, expenses, or even process duration changes/improvements.

<br></br>

## 7.3 Alerts

### `ASG 7.3.1` Implementing Alerts

Set up alerts based on predefined thresholds from the above metrics as monitoring is actively happening. Through alerts, you will receive real-time notifications when key metrics breach acceptable limits, and allow your API development team to assess and rectify any issues quickly. As such, alerts empower teams to **proactively** address issues rather than reactively responding to user complaints.

It is recommended to integrate these alert(s) to your API development teams’ communication channels as part of your monitoring stack, such as:

- Slack
- Microsoft Teams
- Email Addresses

In addition to setting up alerts, your API development or support team should proactively devise incident response plans or contingency plans in advance. This preparation is crucial to promptly execute the necessary actions in response to alerts as they occur. You can decide to share these alerts with your users to notify them of unexpected API outages, or you might use a different channel to inform them separately.
