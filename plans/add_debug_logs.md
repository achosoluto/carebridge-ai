# Add Debug Logs Plan

## Goal
Insert console logs into `Layout.tsx` and each top‑level page component (`Dashboard`, `Messages`, `Appointments`, `Monitoring`, `PatientDetails`) to determine why the UI is not rendering.

## Steps
1. **Layout Debugging**
   - Open `src/components/Layout.tsx`.
   - Add `console.log('Layout children:', children);` just before the return statement.
   - Optionally log `location.pathname` to see the current route.
2. **Page Component Debugging**
   - For each page file (`src/pages/Dashboard.tsx`, `src/pages/Messages.tsx`, `src/pages/Appointments.tsx`, `src/pages/Monitoring.tsx`, `src/pages/PatientDetails.tsx`):
     - Insert `console.log('Rendering <ComponentName>');` at the top of the component function.
3. **Error Boundary (optional)**
   - Wrap the `<Layout>` children in a simple error boundary that logs any caught errors.
4. **Run the dev server** (already running) and refresh the browser.
5. **Capture console output** via the browser sub‑agent and verify which logs appear.
6. **Analyze** which component (if any) is not being instantiated.

## Expected Outcome
- The console should show logs from `Layout` and each page component that is rendered.
- If a component does not log, it indicates that the route is not reaching it.
- Any runtime errors will be visible in the console.

## Next Actions
- Based on the logs, adjust imports, fix missing exports, or correct any CSS that hides content.
- Once the cause is identified, the executing coder‑agent can apply the necessary code changes.
