# Development Guidelines

This project contains a FastAPI backend and a React frontend packaged together with Docker.

## Local Setup
1. Install Python 3.11 and Node.js 18 or newer.
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   yarn install
   cd ..
   ```
5. Create `.env` files in both `backend/` and `frontend/` as described in `README.md`.
6. Run the services for development:
   ```bash
   ./scripts/update-and-start.sh
   ```

## Testing
- Run backend unit tests using `pytest` from the repository root:
  ```bash
  pytest -q
  ```
- Execute React tests from `frontend/`:
  ```bash
  cd frontend
  yarn test
  ```
- You can also run `backend_test.py` to hit the API endpoints:
  ```bash
  python backend_test.py
  ```

## Linting and Formatting
- Format Python code with [black](https://github.com/psf/black):
  ```bash
  black .
  ```
- Lint Python code with flake8 and perform type checking with mypy:
  ```bash
  flake8
  mypy backend
  ```

## Pull Request Checklist
1. Ensure all tests pass and linters show no errors.
2. Provide clear, concise commit messages.
3. Summarize any major changes in the pull request description.
4. Update documentation (including this file) if setup or usage changes.

These instructions apply to the whole repository.
