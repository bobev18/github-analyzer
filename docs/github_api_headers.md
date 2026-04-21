# GitHub API Media Types

The GitHub API uses custom media types in the `Accept` header to allow consumers to choose the format and version of the data they wish to receive. This ensures stability and allows for explicit versioning of API requests.

## Versioning via Media Types
Specifying the version in the `Accept` header is a core part of GitHub's [Media Types documentation](https://docs.github.com/en/rest/using-the-rest-api/get-started-with-the-rest-api?apiVersion=2022-11-28#media-types). By using a specific media type, the application "pins" the API version. This prevents the application from breaking if GitHub eventually changes the default version of their REST API.

## String Breakdown: `application/vnd.github.v3+json`

- **`application/`**: The standard top-level media type for data.
- **`vnd.github`**: Indicates a **v**e**nd**or-specific type belonging to GitHub (`vnd` is the standard prefix for vendor-defined types).
- **`.v3`**: Explicitly requests **Version 3** of the REST API.
- **`+json`**: Specifies that the response body should be formatted as **JSON**.

Using this header is the recommended best practice for all integrations with the GitHub REST API to ensure long-term compatibility.
