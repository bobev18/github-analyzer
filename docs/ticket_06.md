# Ticket #6: Experimental GraphQL API Mode

## Overview
The current "Deep Analysis" mode in the REST API is slow and highly susceptible to rate-limiting because it requires $1 + N$ network requests (where $N$ is the number of repositories). The GitHub GraphQL API (v4) can resolve this by fetching all data in a single request.

## Problem Description
Fetching detailed language stats for 50+ repositories via REST requires 51 separate API calls. This is inefficient and often triggers the 403 Forbidden (Rate Limit Exceeded) error for unauthenticated or base-authenticated users.

## Requirements
- [ ] **Backend Implementation**:
    - Create a new service or function in `github_api.py` that uses the GraphQL endpoint (`https://api.github.com/graphql`).
    - The query should fetch `user { repositories { nodes { name, languages { edges { node { name }, size } } } } }`.
- [ ] **Configuration**:
    - Add a `USE_GRAPHQL_EXPERIMENTAL` flag in the backend configuration.
    - This mode MUST require a valid `GITHUB_TOKEN`, as GraphQL does not support unauthenticated access.
- [ ] **Frontend Integration**:
    - Add an "Experimental: GraphQL" toggle in the UI settings or search options.
- [ ] **Validation**:
    - Compare the speed and accuracy of the GraphQL response against the current sequential REST implementation.

## Benefits
- Reduced latency (single roundtrip).
- Significant reduction in API quota consumption.
- More reliable "Deep Analysis" for heavy GitHub users.

## Priority
Low (Research & Optimization)
