# Frontend-Backend Data Contracts

## Current Strategy: Implicit Contracts

The frontend currently utilizes implicit contracts when communicating with the backend API. Data received from the backend is stored in the `data` property of components using the TypeScript `any` type, and UI components access nested properties (e.g., `data.is_partial`) directly.

## Rationale

While explicit TypeScript interfaces are considered best practice for ensuring type safety and preventing runtime errors, the current approach was chosen for the following reasons:

1. **Monorepo Structure**: Both the FastAPI backend and Angular frontend reside in a single repository. Developers working on the API have direct visibility into the frontend requirements and vice versa.
2. **Scope Management**: For the initial project scope, maintaining a duplicated set of interfaces in the frontend that mirror Pydantic models in the backend was deemed an unnecessary overhead.
3. **Development Velocity**: Avoiding strict typing for API responses allows for rapid iteration on the data model without requiring simultaneous updates to multiple frontend type definitions during early-stage development.

## Future Considerations

If the project scope expands or the following conditions occur, a transition to explicit contracts is recommended:
- The backend and frontend are moved to separate repositories.
- The development team size increases, requiring more formal API documentation.
- The complexity of the data models leads to an increase in "silent" UI failures due to property renaming.

In such cases, tools like `OpenAPI` (Swagger) could be used to automatically generate TypeScript interfaces from the FastAPI backend models.
