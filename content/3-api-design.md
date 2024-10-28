<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 3. API Design Standards and Best Practices

Design and build APIs in a scalable and secure manner

> **Purpose:** To clearly define the standards into each aspect of the API design and implementation, as well as rationale into the design standards and possibly examples to the design.

<br></br>
These standards is intended to help people in the Government building APIs to:

- save time and effort
- adopt an API-first approach
- plan and design APIs thoughtfully and securely
- adopt a testing based implementation to speed up development
- discover the APIs you need and other APIs to foster innovation

<br></br>
The standards are intended to provide some of the best practices into planning, designing and implementing your APIs. This document is followed by guidances for [securing](/pages/4-security.md), [testing](/pages/5-testing.md), [versioning](/pages/6-versioning.md) and [monitoring](/pages/7-monitoring.md) APIs.

<br></br>
Consistency in API definition across Agencies improves developer experience and allows APIs to be more intuitive and reduces lead-time to understanding and consumption of APIs.

<br></br>
<br></br>

## 3.1 General API Standards

### `ASG 3.1.1` Plan your APIs

Identify the users of your APIs and understand their use cases. Prepare API specifications and run this through with users for feedback.

Ensure that APIs are not duplicated, and if it is similar to another API, do consider to combine with or fold the new resource(s) into the existing API.

Do consider the data classification of the resource(s) and that the access to resource is authenticated appropriately and has the correct authorization checks in place.

### `ASG 3.1.2` Clear and Concise Use of Wording Paths, Headers, Queries

The use of clear and concise terms for defining object relating to API (eg. use of path - personal-address), or action-object (eg as get-personal-address). Ambiguous use of English (eg. use of header - do-not-hardcode: false), and double-negatives should be avoided.

Paths should reference nouns and universal terms rather than department names or policy names which could change in the future.

### `ASG 3.1.3` API Specification, Standardized Naming Conventions

The API should be designed and documented with openAPI specifications as much as possible.

Naming and Caps conventions should be standardized for readability, such as:

- URL using lower-cased kebab-case conventions
- JSON key names follow a standardized convention such as lowercase underscore_linked
- header names using lower kebab-case (in line with HTTP/2 standards) starting with organiation header (eg. x-cpf-overwrite-header)
- OAuth scopes using **organization:object:action** names, which are lowercase, underscored_linked and separated by colons, such as **cpf:header_name:read**.

### `ASG 3.1.4` REST API and JSON

The API should be designed to be as a modern interface in REST API, adopting [JSON](https://datatracker.ietf.org/doc/html/rfc7159) standards in its request and response payload, as much as possible.

Where complex data structures be defined for the API resource, do consider using graphQL.

XML APIs should generally be replaced with simpler REST API definitions.

### `ASG 3.1.5` Date and Time Standards

Date and Time specifications should follow the ISO8601 standard, which is defaulted to local Singapore (UTC+8) time, unless otherwise stated.

### `ASG 3.1.6` API Documentation

APIs shall be documented in a standardised format (such as openAPI specifications).

The documentation should be housed in a central location such as Gitlab, Documentation portal or on the API Marketplace.

The documentation shall minimally contain at least the following information:

- function of the API
- specifications as to the use of the API
- [version changes](/pages/6-versioning)

The specifications are to include at least one support email address, methods, parameters, error codes, request, and response content-types.

The documentation is recommended to have the following information:

- sample request and response examples to sandbox environment
- maintenance schedule of API (if available)
- [rate limits](#asg-331-rate-limiting-apis-by-maximum-transaction-rate-and-size) of the API
- [availability, latency](/pages/7-monitoring?id=asg-711-identifying-key-monitoring-metrics)

The sample request and response examples cited should be tested regularly using a CI/CD pipeline.

```
Examples of Request and Response

Request:
GET /cpf-medisave/account/v1/balance/abcde-1234-5678-9012-fgabc
Content-Type: application/json
Authorization: Bearer xxxxx

Response:
200 HTTP/2
Content-Type: application/json
{
    "balance": "$1000.00"
}

Request:
curl -v -H "Content-Type: application/json" -H "Authorization: Bearer xxxxx" 
  https://api.<domain>/cpf-medisave/account/v1/balance/abcde-1234-5678-9012-fgabc

Response:
{
    "balance": "$1000.00"
}
```

### `ASG 3.1.7` API Request and Response

APIs must only be requested and responded to only with the content-type(s) stated in the API documentation. Where the response refers to a resource which could be referenced by an API, do consider to respond with the URL of the resource URL.

API response should also be precise and concise where possible and not provide too much information, and also support filtering.

```
Example of imprecise response:
GET /humanresource/data/v2/personnel/982b4-234d-213f-a8d99
{
    "first_name": "Alice",
    "last_name": "Wong",
    "years_of_service": "5",
    "department": "Sales",
    "department_sales_target": "$500,000",
    "department_sharepoint": "https://xxx"
    "department_strategy": "https://yyy"
}

Example of precise response:
GET /humanresource/data/v2/personnel/982b4-234d-213f-a8d99
{
    "first_name": "Alice",
    "last_name": "Wong",
    "years_of_service": "5",
    "department": "Sales"
}


Example of response with filtering:
GET /humanresource/data/v2/personnel/982b4-234d-213f-a8d99&filter=years_of_service
{
    "years_of_service": "5"
}
```

### `ASG 3.1.8` When Not to use APIs

API use should not be employed in the following scenarios(s):

- large file transfer (>10 Megabytes)

<br></br>

## 3.2 API Specifications

### `ASG 3.2.1` Path Segments

Use **kebab-case** for path segments and words should be in lower case and in English where possible. The Path structure should be clearly defined in a standardized format.

This promotes usability and reduces the need to read documentation. The path should be defined clearly as such:

```
URL:  

https://api.<domain>/<organization>/<object>/v<major version>/<resource>/
  {optional: path parameters}
```

For path with sub-resource(s) the URL should look like this:

```
URL with 2 levels of resource/sub-resources:  

https://api.<domain>/<organization>/<object>/v<major version>/
  <resource>/{optional: path parameters}/<sub-resource>/
  {optional: path paramfeters}
```

The level of resource/sub-resource (in total) should not exceed 3 levels.

### `ASG 3.2.2` Query Parameters

Query parameters should be lowerCamelCased. This is to allow readability and distinction from the path.

Query parameters should define filter or fine-tune API resources and NOT define an action.

```
Query parameters should be for filtering :  ?filter=address

Query parameters should not define action:  ?action=submit
```

### `ASG 3.2.3` Sensitive Information

Avoid the use of directly identifiable or sensitive information such as NRIC or other IDs in the URI (ie. path and query parameters). Paths and query parameters may be cached or logged in systems or network devices outside of control of the client and publisher server. Instead, use a represented ID (eg. UUIDv4 format) and only have sensitive ID information in the payload. Do consider encryption if the information is of high sensitivity.

### `ASG 3.2.4` Payload Encoding

The content body should be encoded using UTF-8 for standardization.

### `ASG 3.2.5` Methods Definition

Methods should correspond to the CRUD definitions where possible such that, POST is to create and replace resource, PATCH is to update resource, DELETE is to delete resource and GET is to get information about the resource.

<br></br>

## 3.3 Rate Limiting

### `ASG 3.3.1` Rate Limiting APIs by Maximum Transaction Rate and Size

Maximum transaction per second per API and application should be limited and also [appropriate rate limiting headers](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers) should be returned to inform the user Application of the API transactions remaining per time block.

For optimal user experience, response payload should be no larger than 100KB. Do consider pagination or return of file (such in CSV format) in gzip format for data intensive return.

AWS also caps a payload size of 10MB, and does transaction rate limiting by time.

### `ASG 3.3.2` Specifying Parameters Limits

Add a proper limit for length of strings and arrays in the OpenAPI specifications that is enforced. This can be achieved by specifying explicit parameter length in the OpenAPI specifications. This will help prevent backend server attacks such as buffer overflow. [Reference (a)](#external-reference)

### `ASG 3.3.3` Specifying API Time Limits

Rate limiting per API to a maximum transaction time must be enforced. This should be configured in the API Gateway or backend server. The Backend transactions should ideally not exceed 3-5 seconds. This will help prevent backend server resource overload, and DDOS.

Long running APIs of more than 10 seconds should be converted to asynchronous APIs and fronted by job trigger and job completion poll APIs instead (preferred), or have callback webhooks. [Reference (a)](#external-reference)

<br></br>

## 3.4 HTTP Status Codes

### `ASG 3.4.1` Status Codes and Semantic Error Codes

It is recommended to follow the [standard HTTP response status codes](https://datatracker.ietf.org/doc/html/rfc7231#section-6) in response to the API request. While that is so, it is also recommended to adopt semantic error codes to reduce ambiguity and lower troubleshooting time.

Error messages must not include technical or trace details to the client as this may expose information about the backend server.

Error messages should ideally be of JSON format and have fields giving information about the error (and by extension how to fix the error), as well as a transaction or correlation ID.

```
{
    "error": "Invalid URL",
    "name": "Bad Request",
    "status_code": "404",
    "correlation_id": "12345-1234-1234-1234-12345"
}
```

Custom status codes with documentation could help the developer to troubleshoot without having to study application logs. Steps to fix the error could be included in the documentation as well.

### `ASG 3.4.2` API Response Status Codes

It is recommended to define the API with at least the below error codes to be conformant to industry linting and OWASP standards.

- success (eg. 200)
- authorization (eg. 400, 403)
- unknown URL (404)
- method not allowed (405)
- rate limits exceeded (429)
- server error (eg. 500)
- server timeout error (504),

<br></br>

## External Reference

a. OWASP API Standards [2023:4](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) Unrestricted Resource Consumption
