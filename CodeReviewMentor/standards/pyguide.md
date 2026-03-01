# Google Python Style Guide: Core Rules

## Naming Conventions
- **Modules**: `lower_with_under.py`
- **Classes**: `CapWords`
- **Functions/Methods/Variables**: `lower_with_under`
- **Constants**: `CAPS_WITH_UNDER`

## Formatting
- **Indentation**: Use 4 spaces per level; never use tabs
- **Line Length**: Maximum 80 characters
- **Semicolons**: Do not use to terminate lines or join statements

## Programming Practices
- **Imports**: Use `import x` for packages/modules only. Avoid `from x import y` for individual functions/classes
- **Exceptions**: Use built-in exception classes; never use catch-all `except:` statements
- **Type Annotations**: Strongly encouraged for public APIs and complex logic
- **Docstrings**: Required for all modules, classes, and non-trivial functions