# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
## Evaluation Questions

### 1. One thing the AI agent got wrong

The AI agent initially suggested using a `SimpleTestCase` for the tenant isolation test.

I detected the issue because the test needed to create database records using Django models. `SimpleTestCase` does not provide database support, so I changed the test class to Django's `TestCase`.

After the change, all five tests passed successfully.

### 2. Part of the code I am least confident about

The part I am least confident about is reference normalization for unusual or malformed record references.

The current implementation removes non-alphanumeric characters and converts references to lowercase. This works for the supplied dataset, but real-world data may contain more complex reference formats that require additional business rules.

### 3. What I would fix first with a second day

With another day, I would improve tenant security by adding authentication and server-side authorization instead of relying only on the `org_id` query parameter.

I would also add more ingestion tests for malformed CSV rows, currency values, blank values, and unusual record references.

## What Was Built

- CSV ingestion for System A, System B, and locations
- Raw value storage
- Reference normalization
- Missing, orphan, duplicate, and value mismatch detection
- Organization and location filtering
- Reason filtering
- Value sorting
- React discrepancy dashboard
- Automated comparator and tenant isolation tests

## What Was Deliberately Not Built

- User login and authentication
- Production-grade role-based authorization
- Multi-database tenant separation
- Pagination for large datasets
- Background processing for very large CSV files
- Exporting discrepancies to CSV
- Production deployment configuration