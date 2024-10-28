<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 8. Lifecycle Management

Understand each stage of an API's life from its inception to its eventual conclusion.

> **Purpose**: To clearly define the standards aimed to streamline API development and deployment processes using appropriate lifecycle stages

<br></br>
The standards aim to assist people in the government that builds APIs to:

- understand the concept of lifecycle management
- plan scheduling and resourcing needed for lifecycle management
- design for user experience, listen to the user

<br></br>

## 8.1 The Lifecycle Stages of API Publishing

Your API progresses through stages from planning, to deployment and eventually to retirement, requiring different workflows to manage them effectively. Take for example, the API that you are managing could have multiple versions:

- `v1.0` -- _retired early this year_
- `v1.1` -- _deprecated and marked for retirement in the next month_
- `v2.0` -- _stable and live_
- `v2.1` -- _in beta testing with selected agencies/partners_
- `v3.0` -- _in the planning/design phase with the product team_

<br></br>

Generally, a complete lifecycle of publishing an API will follow the following stages sequentially:

<br></br>

### `ASG 8.1.1` Plan

The **plan** stage of the API lifecycle involves initial planning and strategising for the development and deployment of an API. This phase includes:

- identifying business objectives
- defining the API's scope and functionality
- determining target audiences and use cases
- establishing key performance indicators (KPIs) to measure success [`ASG 7.2.1`](/pages/8-monitoring?id=asg-721-identifying-key-performance-indicators)

Additionally, the **plan** stage involves conducting market research, assessing technical feasibility, and aligning the API strategy with organizational goals and resources.

For additional context on planning your APIs, refer to [`ASG 3.1.1`](/pages/3-api-design?id=asg-311-plan-your-apis).

> **References to the governance model clauses:**
>
> 1. [`ASG 3.1.1` Plan your APIs](/pages/3-api-design?id=asg-311-plan-your-apis)
> 1. [`ASG 7.2.1` Identifying Key Performance Indicators](/pages/7-monitoring?id=asg-721-identifying-key-performance-indicators)

<br></br>

### `ASG 8.1.2` Design

The **design** stage of the API lifecycle focuses on conceptualizing and defining the structure, functionality, and behavior of the API. This phase involves outlining the API's endpoints, data formats, authentication methods, and other technical specifications based on the identified requirements and use cases.

Additionally, the **design** phase includes:

- creating API documentation [`ASG 3.1.6`](/pages/3-api-design?id=asg-316-api-documentation)
- defining error handling mechanisms
- establishing versioning strategies [`ASG 6.1.1`](/pages/6-versioning?id=asg-611-semantic-versioning) [`ASG 6.2.1`](/pages/6-versioning?id=asg-621-practise-user-centric-versioning)

The **design** stage aims to ensure that the API meets the needs of its intended users, maximizes usability, and lays the groundwork for efficient development and implementation in subsequent stages of the lifecycle.

You may read [**chapter 3**](/pages/3-api-design) to explore the different standards and clauses that promote good API design.

**Consider User Experience as part of the API design**

Do design the return payload for an optimal API experience:

- a reasonable size [`ASG 3.3.1`](/pages/3-api-design?id=asg-331-rate-limiting-apis-by-maximum-transaction-rate-and-size)
- acceptable response time [`ASG 3.3.3`](/pages/3-api-design?id=asg-333-specifying-api-time-limits)

Do consider and determine an acceptable response time threshold (eg. 3-5 seconds), with user feedback, which a transactional response will be acceptable to the end user. Optimize transactional logic to achieve this performance beyond production traffic load, to be tested using load tests.

> **References to the governance model chapters and clauses:**
>
> 1. [Chapter 3: API design](/pages/3-api-design)
> 1. [`ASG 3.1.6` API documentation](/pages/3-api-design?id=asg-316-api-documentation)
> 1. [`ASG 3.3.1` Rate limiting APIs by maximum transaction rate and size](/pages/3-api-design?id=asg-331-rate-limiting-apis-by-maximum-transaction-rate-and-size)
> 1. [`ASG 3.3.3` Specifying API time limits](/pages/3-api-design?id=asg-333-specifying-api-time-limits)

<br></br>

### `ASG 8.1.3` Build

The **build** stage of the API lifecycle involves the development work in the creation of the API based on the design specifications established in the previous stages, turning the API design into a **working**, **well-tested** and **secure** API product. Generally, the **build** phase includes the 3 cross-functional sub-phases:

#### `ASG 8.1.3a` Develop

Here, developers create the code for the API endpoints to bring the design to life. Beyond writing the code, the development work also involves:

- implementing authentication mechanisms
- handling data validation
- integrating with backend systems or databases as necessary

**Consideration for handling large chunks of data**

Consider caching large pools of data with CDN or similar supporting technology ([Read references _a_ and _b_](#external-references)) and allow periodic update of data to maintain the freshness of data. This will save time in large data retrieval from database(s).

Do provide a backend service for service owners or schedule batch jobs to update the cached data periodically.

#### `ASG 8.1.3b` Test

The **test** sub-phase of the **build** stage within the API lifecycle involves rigorously evaluating the API's functionality, performance, and reliability.

This phase includes various types of testing, such as:

- unit testing to examine individual components
- integration testing to assess how different parts work together [`ASG 5.2.1`](/pages/5-testing?id=asg-521-validating-api-contract)
- performance testing to measure the API's responsiveness under various conditions [`ASG 5.4.3`](/pages/5-testing?id=asg-543-conducting-load-amp-stress-testing)
- testing for security vulnerabilities [`ASG 5.3.1`](/pages/5-testing?id=asg-531-validating-owasp-api-security-with-security-tools)

Additionally, it involves ensuring compliance with specifications and requirements. The **test** stage aims to identify and address any issues or weaknesses in the API before it is deployed, ensuring a high level of quality and reliability.

You may read [**chapter 5**](/pages/5-testing) to get a deeper understanding on API testing implementation standards, tools and concepts.

#### `ASG 8.1.3c` Secure

The **secure** sub-phase of the **build** stage within the API lifecycle focuses on implementing and maintaining robust security measures to protect the API from unauthorized access, data breaches, and other cyber threats. Generally, this phase involves:

- identifying security requirements
- implementing authentication and authorization mechanisms [`ASG 4.2.2`](/pages/4-security?id=asg-422-api-access-and-authorization)
- encrypting data transmissions [`ASG 4.4.2`](/pages/4-security?id=asg-442-encryption-of-payload)
- continuously reviewing security protocols to address emerging threats

You may read [**chapter 4**](/pages/4-security) to get a deeper understanding on API security implementation standards, tools and concepts.

> **References to the governance model chapters and clauses:**
>
> 1. [Chapter 5: Quality assurance and testing](/pages/5-testing)
> 1. [Chapter 4: Security and access control](/pages/4-security)
> 1. [`ASG 5.2.1` Validating API Contract](/pages/5-testing?id=asg-521-validating-api-contract)
> 1. [`ASG 5.4.3` Conducting load & stress testing](/pages/5-testing?id=asg-543-conducting-load-amp-stress-testing)
> 1. [`ASG 5.3.1` Validating OWASP API Security](/pages/5-testing?id=asg-531-validating-owasp-api-security-with-security-tools)
> 1. [`ASG 4.2.2` API access and authorization](/pages/4-security?id=asg-422-api-access-and-authorization)
> 1. [`ASG 4.4.2` Encryption of payload](/pages/4-security?id=asg-442-encryption-of-payload)

<br></br>

### `ASG 8.1.4` Deploy

There are a series of activities that you will need to manage when you are ready to deploy a stable, live version of your API.

**Adding documentation with each API deployment**

Your API documentation is where API Consumers will get majority of (if not all) the information they would require to begin integrating their consumer applications with your API. Each time you deploy or update documentation, it acts as a clear changelog for API consumers. They can refer to it to understand the expected changes they need to be aware of.

Use an API specification tool to automatically generate and update references to your API Server’s requests and responses. In the same specification, you should also include a getting started guide for your API Consumers.

For REST APIs, popular API Gateways supports uploading and displaying the OpenAPI Specification document. This enables consumers to explore, evaluate, and try out APIs. You can learn more about API documentation in [`ASG 3.1.6`](/pages/3-api-design?id=asg-316-api-documentation).

**Deploying a sandbox API for your stable API**

For discovery and testing, it's crucial to differentiate between _production_ APIs and _sandbox_ APIs to avoid contaminating production databases with test data. The sandbox replicates your stable API, allowing developers to submit requests and receive responses that realistically mimic the live system.

Deploying a _sandbox_ API also allows consumers to evaluate their need for the stable API before prematurely requesting access to it. You can host or upload these _sandbox_ APIs, wherever you prefer, with the goal of enabling potential users to easily find and interact with them.

> **References to the governance model clauses:**
>
> 1. [`ASG 3.1.6` API documentation](/pages/3-api-design?id=asg-316-api-documentation)

<br></br>

### `ASG 8.1.5` Monitor

During the monitor stage of the API lifecycle, you track and oversee the API's health, performance, usage, and security. This ensures it meets SLAs, maintains performance, detects issues promptly, and assesses overall health within its infrastructure.

[**Chapter 7**](/pages/7-monitoring) covers concepts deeper about monitoring, including tools, metrics, and techniques.

> **References to the governance model chapters:**
>
> 1. [Chapter 7: Monitoring, Analytics, and Performance](/pages/7-monitoring)

<br></br>

### `ASG 8.1.6` Distribute

After thoroughly developing, testing, and refining your API, the next focus for your team should be making it discoverable for consumption.

**Managing access to your API**

In most cases, there will need to be a controlled (and frequently reviewed) list of API consumers that can transact with your deployed API. Managing access to APIs is necessary to control and regulate how consumers interact with and utilize the API. This ensures security, prevents unauthorized usage, and allows your organization to monitor and track API usage for various purposes such as analytics, compliance, and resource allocation. Proper access management also helps protect sensitive data or organization capability, maintain service reliability, and enforce usage policies. In essence, managing access to APIs is crucial for maintaining a secure, efficient, and controlled environment for both API providers and consumers.

Maintaining a controlled list of users makes upgrading versions easier. You can quickly identify and notify these users of changes and actions they need to take.

Most full-featured API Gateways currently supports the management of user access to your APIs and provide identifiable attributes of each API call through its inbound security mechanism. It also allows you to automatically propagate version updates of your APIs to the existing users of it.

You can also visit clause [`ASG 9.1.1`](/pages/9-community?id=asg-911-list-apis-unto-api-marketplace-api-catalog) to learn about distributing your APIs on an API Marketplace or Catalog to reach more users.

> **References to the governance model clauses:**
>
> 1. [`ASG 9.1.1` List APIs unto API Marketplace / API Catalog](/pages/9-community?id=asg-911-list-apis-unto-api-marketplace-api-catalog)

<br></br>

### `ASG 8.1.7` Deprecate/Retire

Over time, older APIs become outdated because they're replaced by newer, improved versions. As we manage concurrently deployed APIs, older APIs should be deprecated and eventually retired when:

- a new major version of the (or alternative) API is deployed and stable
- a version of API poses vulnerabilities or security risks
- the API is no longer able to deliver its intended value

When deprecating a version of your API, be aware that some of your users might have limited resources to manage updates on time, and as such, require sufficient time for transition. It is important to note that abruptly removing an API or offering inadequate support or transition time can greatly affect the services using it.

A planned process for deprecation and retirement should include the following phases that can be found in [`ASG 6.2.2`](/pages/6-versioning?id=asg-622-deprecation-of-major-version) and in [`ASG 6.2.3`](/pages/6-versioning?id=asg-623-deprecation-headers).

> **References to the governance model clauses:**
>
> 1. [`ASG 6.2.2` Deprecation of major version](/pages/6-versioning?id=asg-622-deprecation-of-major-version)
> 1. [`ASG 6.2.3` Deprecation headers](/pages/6-versioning?id=asg-623-deprecation-headers)

<br></br>

## External References

a. [use of memcached for web caching](https://www.dragonflydb.io/guides/memcached)

b. [use of memcached in facebook for key-value store and pre-computed results to achieve microseconds retrieval](https://research.facebook.com/publications/scaling-memcache-at-facebook/)
