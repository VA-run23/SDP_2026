# Google API Design Standards

## 1. Resource-Oriented Design (AIP-121)
- **Nouns over Verbs**: The fundamental building blocks are individually-named resources (nouns) rather than actions.
- **Resource Hierarchy**: Model the API as a tree of resources. For example, a `publisher` has a collection of `books`.

## 2. Resource Naming (AIP-122)
- **Plural Collections**: Collection identifiers must be the plural form of the noun (e.g., use `/users`, not `/user`).
- **CamelCase**: Collection identifiers must use `camelCase` and start with a lower-cased letter.
- **Resource IDs**: Individual resource IDs should be strings and, if user-specified, should be lowercase alphanumeric with hyphens (e.g., `my-resource-id`).
- **Separator**: Use the `/` character to separate name segments.

## 3. Standard Methods (AIP-131 - AIP-135)
- **Get**: Retrieves a single resource. The HTTP verb must be `GET`. The URL should contain a single variable field called `name`.
- **List**: Retrieves a collection of resources. The HTTP verb must be `GET`.
- **Create**: Creates a new resource. The HTTP verb must be `POST`.
- **Update**: Modifies an existing resource. The HTTP verb must be `PATCH` (preferred) or `PUT`.
- **Delete**: Removes a resource. The HTTP verb must be `DELETE`.

## 4. General Naming Conventions (AIP-190)
- **American English**: Use correct American English (e.g., `color`, not `colour`).
- **Snake_case**: Use `snake_case` for field names in JSON request and response bodies to maintain consistency with modern development practices.
- **Avoid Abbreviations**: Use straightforward, intuitive names. Avoid cryptic abbreviations.

## 5. Error Handling (AIP-193)
- **Standard Status Codes**: Use standard HTTP status codes (e.g., `404 Not Found`, `429 Too Many Requests`).