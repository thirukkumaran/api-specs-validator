<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 10. Roles of an API Gateway

Learn how an API Gateway can greatly enhance your entire API ecosystem.

> **Purpose**: To articulate the advantages of using an API Gateway for streamlining the management of scalability, monitoring, consolidation, and security of your APIs within a single central location.

<br></br>

The standards aim to assist people in the government that builds APIs to:

- understand the concepts of an API Gateway
- centralise and scale API traffic and operations
- simplify the API management process

<br></br>

## 10.1 What is an API Gateway, and why you should use it

An API gateway is sits between client applications (like websites or mobile applications) and backend services, acting as one main entry point for all the incoming requests. Through an API gateway, we can do several things to safeguard and improve backend services by:

- Managing API access control
- Securing backend services from attacks
- Managing the load/traffic and caching of API requests
- Centralizing logging, monitoring, tracing, and analytics

### `ASG 10.1.1` Handling API access control

For any API (or backend service) fronted by an API Gateway, access control mechanisms such as authentication, authorization, and API keys are readily available to determine access to these APIs based on permissions. The API gateway also enables administrators to centrally periodically review access permissions, ensuring that only authenticated and authorized users can interact with specific API versions.

API Gateways can also control access to beta (or future) versions of APIs. Publishers can invite a few existing users to try out beta API programs to see if they work. As API versions are promoted, administrators can adjust access permissions accordingly.

Learn about the best practices and standards for API authentication and authorization [here](/pages/4-security?id=_42-use-of-strong-authentication-and-authorization-mechanisms).

### `ASG 10.1.2` Securing backend services from attacks

As an extension of API access control management, where only valid, authenticated, and secure access is permitted to call APIs, API Gateways are additionally equipped with standardized security policies and capabilities. This includes:

- Encrypting traffic between client applications and backend servers
- Firewall and whitelisting configuration
- Validating input and requests paths/methods of APIs
- Implementing rate-limiting to thwart Denial-of-Service (DoS) attacks

Since these security features are centrally managed, API development teams can leverage on these gateway protection mechanisms and concentrate on their API products, allowing them to remain agile in their API delivery.

For a more comprehensive guide, you can learn more about security standards when it comes to building APIs [here](/pages/4-security).

### `ASG 10.1.3` Managing the load/traffic and caching of API requests

Managing the load/traffic to backend services in API Gateways involves regulating the flow of requests to ensure optimal performance and prevent overload. This includes implementing features such as load balancing, caching, and rate limiting to distribute and control the volume of incoming requests. Additionally, API Gateways may prioritize and route requests based on factors like server availability and response times to maintain efficiency and reliability.

In some cases, API providers can individually control quota plans per client application via an API Gateway. A quota plan is a mechanism for managing and limiting the usage of an API by defining specific limits on the number of requests or the amount of data that a client application can send or receive within a given time period, typically measured in terms of requests per minute, hour, or day. Quota plans help API providers control access to their resources, prevent abuse or misuse, and ensure fair usage among different clients or subscription tiers. When a client application reaches its quota limit, the API gateway may respond with an error or throttle the client's requests until the quota resets.

API Gateways also comes with caching capabilities, which is a useful strategy for API providers when the API responses are consistent over time. Through caching (with a proper cache invalidation strategy), it reduces the number of requests to the upstream API server(s), leading to an overall heathier load management.

### `ASG 10.1.4` Centralizing logging, monitoring, tracing, and analytics

Centralizing logging, monitoring, tracing, and analytics in API Gateways involves aggregating and analyzing data related to API usage, performance, and errors from various sources in a centralized location. This enables developers and administrators to gain insights into how APIs are being used, identify issues or bottlenecks, and optimize performance. It also facilitates tracking requests across distributed systems, diagnosing problems, and ensuring compliance with security and regulatory requirements.

Learn more about monitoring, analytics and KPIs of APIs [here](/pages/7-monitoring).
