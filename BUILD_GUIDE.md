To build the package, run:

### Install tool build

```bash
pip install --upgrade build twine
```

### Build package

```bash
python -m build
```

### Publish package

```bash
python -m twine upload dist/* __token__ -p your-pypi-token
```
