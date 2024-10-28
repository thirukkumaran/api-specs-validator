<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 4. Security and Access Control

Design your APIs with security in mind

> **Purpose:** To clearly define the security standards for consideration for building the APIs.

<br></br>
The standards is intended to help people in the Government building APIs to:

- build secure APIs
- consider different aspects in security, such as authentication, authorization, confidentiality and integrity of data
- build security in depth

<br></br>
<br></br>

## 4.1 Use of Secure Transport Systems

### `ASG 4.1.1` Transport Security

API Communications MUST be exchanged over TLS-based secured connections. This always a strong trust between the client and server and helps to mitigate against MITM attacks and leakage header, and body.

Governing clauses (eg. IM8) which define TLS (eg. minimum versions), protocols and cipher suites must be followed.

If the data is sensitive, do consider the use of [encryption](#asg-442-encryption-of-payload), signing of payload and mechanisms which can prove non-repudiation (eg. JWE).

Additional measures such as IP address white-listing in firewall, can be considered to secure sensitive communication channels.

The use of APEX mandates TLS communication and narrows down the protocols which is allowed in the IM8.

<br></br>

## 4.2 Use of Strong Authentication and Authorization Mechanisms

APIs should be secured so that user applications (consumers) of APIs are easily identifiable, and appropriate authorization be enforced for user applications.

User applications should not have access to APIs or data which they are not authorized for.

Strong **authentication** methods should be used for API requests to prevent unintended API access.

### `ASG 4.2.1` Identification and Authentication

a) API users (eg. application or browser clients) must be identifiable, whether it is a single user (client-to-server API calls), an organization with responsible and identifiable organization administrator (for server-to-server API calls).

This is to provide correct authorization to APIs and misuse to be attributable.
<br></br>

b) API administrators configuring the APIs should be authenticated with 2FA (2nd factor of authentication) when configuring the API (eg. request of API, obtaining API key, specification of JWKS endpoint).

This is to prevent unintended access of API and leakage of API backend information.

Eg. the use of Google's developer's portal mandates a 2FA login.

### `ASG 4.2.2` API Access and Authorization

a) APIs must be secured with access that allows fine-grained API Access to users and organizations. Resources being accessed should be clearly defined and clearly documented in the Description of the API. This prevents unintended leakage of information and users/organizations having unintended functional access to resources secured by the API Publisher.

Avoid crafting APIs such that the query could be `/org/dept/v1/humanresource`, where the query body for name of department staff could be: `{"query":"staff_name"}`

A malicious attacker could change the query to: `{"query":"staff_pay"}` by inference. You can learn more about the example [here](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/).

<br></br>

b) API Keys should be avoided unless for APIs of low sensitivity. Session tokens should also be avoided for API calls, but if Access Tokens need to be used, OAuth2 with OIDC should be used. DPoP could be used to prove ownership of Access Token. JWT Authentication should be used for API calls as it can incorporate confidentiality, integrity and authenticity and can be implemented as one-use tokens. API Keys are inherently easy to be stolen and re-used. Session tokens could also be easily stolen for re-use, unless DPoP is used together.

### `ASG 4.2.3` API Authentication Mechanisms

The recommendations regarding the different security mechanisms are as follows:

- **JWT Authentication**:
  This could be designed as single use JWTs which can corporate authentication and integrity. Client-based signing allows non-repudiation of token.

- **API Keys**:
  This should only only be used be used for APIs with low sensitivity. And even when it is used, the throughput (transaction per second) be throttled to prevent a DDOS attack. Mechanisms specified in Topic 4 (Rate Limiting) should be adopted.

  The API Key should also be rotated according to the recommendations of the governing body. For low sensitivity data, APEX will recommend rotation of API Keys on a monthly basis.

- **Session Tokens**:
  This should be avoided for API calls where possible as this may allow, within the time window, possible leakage of information or execution of unintended functions should the token be compromised. If this has to be used, a scope limitation and/or execution of token expiry should be carried out. An out-of-band temporal key (such as dPoP) exchange could be carried out to verify authenticity of token carrier. OAuth2.1 and OIDC 2.0 are popular protocols used to support this method of Authorization.

- **OAuth2**:
  If a session Access Token has to be used, the latest version of OAuth2 should be used. Scopes should be well-defined when using this and scopes should follow the format `<organization>.<resource>:<function>`, in lowerCamelCased. For example eg. cpf-payroll.labourSurvey:update or apex.newConsumer:create. This is to allow a logical and clear definition of scopes for readability and granular permissions definition.

- **OIDC2.0**:
  This should be incorporated with OAuth2 as the authentication mechanism (as Identity Provider).

- **DPoP (Demonstrated Proof of Possession)**:
  Where possible, this should be incorporated in the OAuth2 Access Token, to constraint the use of Access Token to the intended audience only.

Regular key rotation often is to ensure freshness of the key and limit damage should private keys be compromised. The recommended key rotation for JWT keys is 3 months while that of API Keys is 1 month.

<br></br>

## 4.3 API and Browser Security

APIs should have exacting definitions, such that [headers](#asg-431-use-of-headers), requests, responses, [content-type](#asg-435-api-content-type-validation) and [cookies](#asg-436-cors-implementation) are carefully designed.

Validation of headers, query parameters, resource, method and content-type should also be carried out.

Cookies and data must be secured using mechanisms such as [CORS](#asg-436-cors-implementation) and CSRF protection.

[Sensitive information](#asg-443-sensitive-information) should be exchanged in the http payload and utilize [encryption](#asg-442-encryption-of-payload).

### `ASG 4.3.1` Use of Headers

Headers should be used for meta-data and authorization headers. Sensitive data should not be placed into headers, but into the message body of the API request and considered for encryption.

While headers have traditionallyHeaders should generally treated as case-agnostic, with custom headers in lower case following the convention `x-{organization}-{resource}`, such as x-cft-jwt.

### `ASG 4.3.2` API Header and Query Parameter Validation

API access should be validated against allowed headers, and query parameters. Unintended headers should be dropped to prevent malware transmission.

Header and query parameters should also be checked for maximum records and maximum size to prevent attacks like buffer overflow.

Erroneous requests should throw appropriate semantic error (ie. 415 Unsupported Media Type), incorrect Content-Type (ie. 405 Media-Type Error) or incorrect headers/parameters (ie. 400 Client Error).

Using an API Gateway protects backend servers from unintended headers and query parameters.

### `ASG 4.3.3` API Resource Validation

API `key:value` pairs in payload, query parameters and headers should have the string values validated via regex in the backend server to prevent Server-Side Request Forgery (SSRF) exploits.

Keys should be validated to be authorized for the user as well. (Read: [here](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/) and [here](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/))

The resource being validated should be checked for authorization and if the user is authorized to access any said resources. Mapping objects granularly by API resources can be a way of mapping authorization to user application.

Request and return content-types should also be validated.

Using a full-featured API Gateway helps in enforcing resource to user authorization by API authorization by application and also Content-Type validation.

### `ASG 4.3.4` API Method Validation

API methods should be well-defined and functions (eg. GET, DELETE) to permissions well defined for users. This can prevent unintended functional leak (eg. a user authorized for GET does DELETE to a resource instead).

Use APEX can help in enforcing validation to resource method by specifying resources to a granular method function eg. {resource} as get-staff and delete-staff.

### `ASG 4.3.5` API Content-Type Validation

API request and response Content-Types should be clearly defined and unexpected Content-Type headers and payload be rejected.

Use of an API Gateway enforces Content-Type validation in payload.

### `ASG 4.3.6` CORS Implementation

API data, and cookies should be secured by implementing CORS by configuring specific domains. This also prevent other sniffing and data exfiltration related attacks.
<br></br>

## 4.4 Sensitive Data, Signing and Encryption

### `ASG 4.4.1` Signing and Integrity

It is recommended to have API requests signed, ensuring message integrity. This is to prevent payload tampering by any intermediary parties.

### `ASG 4.4.2` Encryption of Payload

It is recommended to have API requests with sensitive payload encrypted, ensuring message confidentiality. This can be achieved by utilizing a modern encryption scheme such as JWE and public encryption keys in JWKS endpoints.

Using JWE also has the added benefits of integrity, non-repudiation of payload and only authorizing the correct party to read the payload.

### `ASG 4.4.3` Sensitive Information

Sensitive information must not to be included in headers, URLs, query parameters. These could end-up being logged in certain devices such as DNS, proxy and WAF servers.

<br></br>

## External References

a. [OWASP API Security Top 10](https://owasp.org/API-Security)
