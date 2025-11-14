# PyPI Publishing Guide

This guide explains how to publish the `govesb` package to PyPI.

## Prerequisites

1. Install required tools:
```bash
pip install build twine
```

2. Create accounts:
   - TestPyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

3. Configure credentials (create `~/.pypirc`):
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Or use environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=your-token-here
```

## Publishing to TestPyPI

1. Build the package:
```bash
./build.sh
```

2. Upload to TestPyPI:
```bash
./upload-test.sh
```

Or manually:
```bash
twine upload --repository testpypi dist/*
```

3. Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ govesb
```

## Publishing to PyPI (Production)

1. Ensure version is updated in `setup.py`

2. Build the package:
```bash
./build.sh
```

3. Upload to PyPI:
```bash
./upload-live.sh
```

Or manually:
```bash
twine upload dist/*
```

4. Verify installation:
```bash
pip install govesb
```

## Version Management

Update the version in `setup.py` before each release:
```python
version='2.1.0',  # Update this
```

Follow semantic versioning:
- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

## Checklist Before Publishing

- [ ] Version updated in `setup.py`
- [ ] README.md is up to date
- [ ] All tests pass (if applicable)
- [ ] Dependencies are correct in `setup.py`
- [ ] Package builds successfully (`./build.sh`)
- [ ] Test installation from TestPyPI works
- [ ] Documentation is complete

## Troubleshooting

### "Package already exists"
- Update the version number in `setup.py`

### "Invalid distribution"
- Clean build artifacts: `rm -rf dist/ build/ *.egg-info`
- Rebuild: `./build.sh`

### Authentication errors
- Verify your PyPI token is correct
- Check `~/.pypirc` configuration
- Use `--verbose` flag for more details: `twine upload --verbose dist/*`

