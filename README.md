# GitHub User Analyzer

A web application that retrieves and displays GitHub user data using the GitHub REST API.

## Core Functionality

- **User Retrieval**: Fetches user profile data, follower counts, and repository lists.
- **Technology Analysis**:
    - **Standard Mode**: Extracts primary language and technology data from the user's profile metadata.
    - **Deep Mode**: Iterates through individual repositories to calculate primary language counts.
- **Error Handling**: Provides status messages for non-existent users, empty repository lists, or missing follower data.
- **Rate Limit Management**: Detects API rate limiting and provides partial results where applicable.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Uvicorn.
- **Frontend**: Angular 21, TypeScript, Vanilla CSS.
- **Dependency Management**: `uv` (Backend), `npm` (Frontend).
- **Authentication**: Supports GitHub Personal Access Tokens via `.env`.
- **Configuration**: Shared configuration via `project.json`.

## Setup and Installation

### Backend

1. Navigate to the `backend` directory.
2. Sync dependencies:
   ```bash
   uv sync
   ```
3. (Optional) Configure `.env`:
   ```env
   GITHUB_TOKEN=your_token
   ```
4. Start the server:
   ```bash
   uv run python -m uvicorn main:app --reload
   ```

### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the application:
   ```bash
   ng serve
   ```

## Testing

### Backend
Run the test suite using `pytest`:
```bash
uv run pytest
```

### Frontend
Run unit tests using the Angular CLI:
```bash
ng test
```

## Directory Structure

- `backend/`: FastAPI source code and API integration.
- `frontend/`: Angular application and source components.
- `docs/`: Technical documentation and project history.
- `PROBLEM_DEFINITION.md`: Project requirements and specifications.

## License

Refer to the project's license documentation for details.
