# Development

Docker is the preferred development and test environment for this repo.

## Build Dev Image
```
docker build -t fastmllp-dev .
```

## Lint and Test
```
docker run --rm -v "$PWD":/app -w /app fastmllp-dev ruff check .
docker run --rm -v "$PWD":/app -w /app fastmllp-dev pytest -q
```

## Interactive Shell
```
docker run --rm -it -v "$PWD":/app -w /app fastmllp-dev bash
```

## Release Process
1. Update version in `pyproject.toml`.
2. Update `CHANGELOG.md` (move entries from `[Unreleased]` into the new version).
3. Commit the changes.
4. Tag the release as `vX.Y.Z` (must match `pyproject.toml`).
5. Push the tag to trigger the GitHub Actions release workflow.

The release workflow builds sdist/wheel and creates a GitHub Release with the
artifacts.
