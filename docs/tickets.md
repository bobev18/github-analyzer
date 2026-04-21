# Pending Improvements & Gaps

## [x] Ticket #1: Implement Repository Pagination
**Description**: The backend currently only fetches the first 30 repositories for any user.
**Requirement**: Modify `github_api.py` to handle pagination by checking the `Link` header or iterating until no more repos are returned. This ensures that "Most Used Language" and "Technology Stack" are accurate for users with many repos.

## [x] Ticket #2: Add "No Followers" Meaningful Message
**Description**: The UI shows `0 Followers` in a badge, but the problem definition requires a "meaningful message" for users with no followers.
**Requirement**: Implement a message state in the frontend (e.g., in the bio or a dedicated alert) that explicitly states "This user does not have any followers" when the count is zero.

## [x] Ticket #3: Deep Technology Analysis (Optional Enhancement)
**Description**: Currently, only the primary language of each repo is counted as a "technology."
**Requirement**: To fully satisfy the "list of all technologies" requirement, iterate through repos and fetch the results from the `/languages` endpoint. Note: This will increase API consumption, so it should be used judiciously.

## [x] Ticket #4: Explicit GitHub Token Configuration
**Description**: The backend automatically uses `GITHUB_TOKEN` if present in `.env`.
**Requirement**: Introduce a configuration check (e.g., `GITHUB_AUTH_ENABLED` boolean) to allow developers to explicitly disable authentication for testing rate-limiting behavior or "guest" mode.

## [ ] Ticket #5: Resolve missing dependencies
*See standalone ticket definition in [ticket_05.md](file:///d:/gits/github-analyzer/docs/ticket_05.md)*

## [ ] Ticket #6: Experimental GraphQL API Mode
*See standalone ticket definition in [ticket_06.md](file:///d:/gits/github-analyzer/docs/ticket_06.md)*

