# PROPOSAL: Migrate to Standalone Component Architecture

## Overview
This ticket proposes refactoring the frontend from a module-based architecture (`AppModule`) to the modern **Standalone Component** architecture introduced in Angular 14 and made the default in v17+.

## Justification

> [!NOTE]
> Standalone components offer a more streamlined developer experience by removing the "middleman" of NgModules.

1. **Reduced Boilerplate**: Standalone components eliminate the need for `AppModule`. All dependencies (like `CommonModule`, `FormsModule`, and `HttpClientModule`) are imported directly into the component that needs them.
2. **Modern Compliance**: Angular CLI (as of v17) generates standalone applications by default. Using this architecture ensures the project is aligned with current best practices and official documentation.
3. **Better Tree-Shaking**: The Angular compiler can more effectively remove unused code when dependencies are scoped to individual components rather than a global module.
4. **Improved Developer Workflow**: It is easier to reason about a component's dependencies when they are listed in its own metadata, rather than hunting through one or more module files.
5. **Future Proofing**: While NgModules are still supported, the Angular team is moving towards a component-centric model for features like signal-based components and improved hydration.

## Proposed Strategy
1. Add `standalone: true` to `AppComponent`.
2. Move global imports from `AppModule` to the `imports` array of `AppComponent`.
3. Update `main.ts` to use `bootstrapApplication(AppComponent, appConfig)`.
4. Delete `app.module.ts`.

## Risks & Mitigation
- **Risk**: Potential confusion if the team is used to the module pattern.
- **Mitigation**: Standard documentation for Angular 17+ is now primarily standalone-first, making it the easier pattern to learn for new joiners.
