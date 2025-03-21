# Contributing Guidelines

## Pre-commit Hooks

This project enforces code quality through pre-commit hooks. Before making any commits, please ensure you have installed and activated the pre-commit hooks by following these steps:

1. **Install pre-commit:**
   Run the following command to install pre-commit:
   ```
   pip install pre-commit
   ```

2. **Install the pre-commit hooks:**
   In your repository, run:
   ```
   pre-commit install
   ```

3. **Run all hooks manually:**
   To run all pre-commit hooks on all files, use:
   ```
   pre-commit run --all-files
   ```

## Continuous Integration

This repository uses GitHub Actions to automatically run the following on each push and pull request:
- Code formatting (Black, isort)
- Linting (flake8)
- Pre-commit checks
- Unit and end-to-end tests

If any checks fail, the commit or pull request will be blocked until the issues are resolved.

## Setup Script

For convenience, there is a setup script that installs the pre-commit hooks automatically. You can run it with:
```
bash setup_precommit.sh
```

Happy coding!
