<br></br>

![API Standards and Governance logo](../assets/logo+title.png ":size=250")

# 6. Versioning, Compatibility and Change Management

Adopting Best Practices in API Versioning

> **Purpose:** To clearly define the versioning number standards and best practices in managing API versioning changes.

<br></br>
The standards is intended to help people in the Government building APIs to:

- use a standardized version numbering scheme
- manage version changes with a user-centric approach

<br></br>
<br></br>

## 6.1 Version Numbering Standard

### `ASG 6.1.1` Standardized Versioning

API error messages should adopt a standardized versioning strategy, such as the [Semantic Version numbering](https://semver.org), where in version x.y.z,

    z refers to a minor version change due to bug fix, and is backward compatible

    y refers to a minor version change due to feature release, but is backward compatible

    x refers to a major version change which may not be backward compatible

This allows API consumers to be informed if API changes are breaking changes and if resources are necessary to modify the client application.

Typical version changes are backward compatible and only minor version number changes occur. Do update version changes into the API documentation, if possible.

<br></br>

## 6.2 User-centric Versioning

### `ASG 6.2.1` Practise User-centric Versioning

Adapt user-centric versioning, meaning API version changes should be carefully managed and breaking changes avoided over the lifetime of the API as much as possible.

Be aware of users of your APIs and communicate version changes to users in advance.

[Breaking changes](#asg-622-deprecation-of-major-version) may require code changes for your users/user applications. If this is unavoidable, communication to users is required as to the changes to API and what action is required from the users.

Do also communicate the intended deprecation date of the older version, where possible, attaching [headers](#asg-623-deprecation-headers) with the response, with the API response progressing to 410 (Gone) or 404 (Resource not found) after it is deprecated.

<br></br>

### `ASG 6.2.2` Deprecation of Major Version

API changes across major versions are not to be taken lightly and may cause functionality breakages in the Client Application. Also, APIs and resources that should not be accessed should be retired through a proper lifecycle management.

The process of Major Version API deprecation should generally follow these steps:

a. New Backend Version is available and function in the Backend Server via a new URL `https://xxxxx/v2/xxxxx` where v2 is the new version and v1 is the legacy version.

b. A deprecation date of the older version (eg. v1) is planned where there is communication to end-users of API of this date. This is the date where Clients should begin to start using/migrating to the new version of the API (v2). A header should provide the deprecation information during this time period.

c. Monitor soon-to-be-deprecated APIs and remind users to migrate to the new version.

d. At the end of deprecation date is the retirement date where the older version (v1) is no longer available as a backend service and the server should throw errors (such as 404 Not Found or 410 Gone).
<br></br>

### `ASG 6.2.3` Deprecation Headers

[Deprecation](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-deprecation-header-03) or [Sunset](https://www.rfc-editor.org/rfc/rfc8594.html) headers should be attached to response headers for APIs marked for deprecation.

The use of APEX will allow compliance of this.

<br></br>
<br></br>

## External Reference

a. OWASP API Standards [2023:4](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) Unrestricted Resource Consumption

b. [Deprecating headers - IETF Draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-deprecation-header-03)

c. [Sunset headers - Rfc 8594](https://www.rfc-editor.org/rfc/rfc8594.html)

d. [Semantic Version numbering](https://semver.org)
