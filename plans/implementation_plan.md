# Fix Blank Page Issue in CareBridge Dashboard

## Goal Description
The frontend currently displays a blank page when navigating to `http://localhost:3000/static/`. The goal is to identify and resolve the root cause so that the dashboard renders correctly, with all routes and components functioning as intended.

## Proposed Changes

### App.tsx Refactor
- Replace the complex `<Routes>` block with a minimal routing setup to verify routing works.
- Gradually re‑introduce original routes once the basic setup is confirmed.
- Ensure `Layout` correctly renders its `children`.

### Layout Component Review
- Verify that `Layout` does not swallow children or apply CSS that hides content.
- Check for any conditional rendering that could result in an empty UI.

### Page Component Audits
- Inspect each page component (`Dashboard`, `Messages`, `Appointments`, `Monitoring`, `PatientDetails`) for runtime errors or missing imports (e.g., icons `TrendingUp`, `Users`, `Bell`).
- Add missing imports and remove unused variables to avoid silent failures.

### Vite Base Path & Router Basename
- Confirm `vite.config.ts` base is `/static/` and that `BrowserRouter` uses `basename={import.meta.env.BASE_URL}`.
- If needed, hard‑code `basename="/static/"` temporarily for debugging.

### Dependency Checks
- Ensure all required packages are installed (`react-router-dom`, `lucide-react`, etc.).
- Run `npm install` and verify no missing modules.

### Verification Steps
1. Start the Vite dev server (`npm run dev`).
2. Open `http://localhost:3000/static/` and confirm the test route renders.
3. Incrementally add original routes and page components, checking the UI after each addition.
4. Capture screenshots and console logs after each step.
5. Once the full dashboard loads, run the test suite (`npm test`).

## Verification Plan
### Automated Tests
- Run existing unit/integration tests to ensure no regressions.
- Add a simple Cypress test that visits the root URL and checks for the presence of the "Dashboard" heading.

### Manual Verification
- Manually navigate to each route (`/staff/dashboard`, `/staff/messages`, etc.) and verify content displays.
- Confirm no 404 or console errors.

---
*This plan is intended for review before implementation.*
