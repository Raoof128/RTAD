# Contributing to RTAD

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the Ransomware Resilience & RTO Dashboard. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🛠️ Development Setup

1.  **Fork the repository** and clone it locally.
2.  **Install dependencies**:
    ```bash
    make install
    ```
3.  **Run the app**:
    ```bash
    make run
    ```

## 🧪 Testing

We use `unittest` for testing. Please ensure all tests pass before submitting a PR.

```bash
make test
```

## 🎨 Code Style

*   **Type Hints**: All functions must have Python type hints.
*   **Docstrings**: All public functions and classes must have docstrings.
*   **Formatting**: We follow PEP 8. Please run `black .` before committing if possible.
*   **Logging**: Use the provided `utils.logger` instead of `print()`.

## 📝 Pull Request Process

1.  Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2.  Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3.  Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4.  You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.
