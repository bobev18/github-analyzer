# Ticket #5: Resolve Missing Dependencies

## Overview
The application currently imports and uses several libraries that are not explicitly defined in the dependency management files (`requirements.txt` for backend and `package.json` for frontend). This can lead to "module not found" errors in fresh environments.

## Problem Description
1.  **Backend**: `backend/github_api.py` (line 3) imports `load_dotenv` from `dotenv`. However, `python-dotenv` is missing from the root `requirements.txt`.
2.  **Frontend**: `frontend/src/app/app.component.ts` (line 5) imports `Chart` from `chart.js`. This is not a standard Angular library and needs to be explicitly added to `package.json`.

## Requirements
- [ ] **Backend**: Add `python-dotenv` to the root `requirements.txt` file.
- [ ] **Frontend**: Execute `npm install chart.js` in the `frontend/` directory to add it to the project dependencies.
- [ ] **Verification**: Ensure the backend starts correctly without manual dependency installation and the frontend chart renders as expected.

## Priority
Medium (Blocking for new developers)
