# Contributing Guide

Thank you for your interest in contributing to the oTree AI Growth-Risk Experiments project! This guide explains how to contribute effectively.

## Ways to Contribute

| Type | Examples |
|------|----------|
| 🐛 Bug Reports | Issues with unexpected behavior |
| ✨ Feature Requests | New treatment arms, visualizations |
| 📝 Documentation | Improvements, translations, examples |
| 🔧 Code | Bug fixes, new features, tests |
| 🧪 Testing | Running experiments, finding edge cases |

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on [GitHub](https://github.com/ignaciourbina/otree-game) to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/otree-game.git
cd otree-game
```

### 3. Set Up Development Environment

Follow the [Development Setup Guide](./setup.md).

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Examples

```bash
git commit -m "feat(cournot): add extreme curvature treatment arm"
git commit -m "fix(formal_model): correct log utility edge case"
git commit -m "docs(api): add examples for SimpleAIGrowthRiskModel"
git commit -m "test(bots): increase coverage for asymmetric treatments"
```

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Format code
black formal_model/ otree/ simulations/ testing/
isort formal_model/ otree/ simulations/ testing/

# Run tests
python testing/run_ai_growth_risk_bots.py --iterations 3

# Type check (if applicable)
mypy formal_model/ --ignore-missing-imports
```

### 2. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template

### 4. PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Breaking change

## Testing
- [ ] Ran bot tests
- [ ] Added new tests
- [ ] Tested manually

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### 5. Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, PR will be merged

## Code Style

### Python

- **Formatter**: Black (line length 100)
- **Import sorting**: isort
- **Type hints**: Encouraged for public APIs
- **Docstrings**: Google style

```python
def calibrate_ubar_from_v(c0: float, gamma: float, target_v: float = 6.0) -> float:
    """Calibrate utility shift parameter from VSL target.
    
    Args:
        c0: Baseline consumption level.
        gamma: Relative risk aversion coefficient.
        target_v: Target value of v(c0), defaults to 6.0.
    
    Returns:
        The calibrated ubar value.
    
    Example:
        >>> calibrate_ubar_from_v(1.0, 2.0)
        7.0
    """
    if gamma == 1.0:
        return target_v - math.log(c0)
    return (target_v - 1.0 / (1.0 - gamma)) / (c0 ** (gamma - 1.0))
```

### Documentation

- Markdown files in `docs/`
- Clear headings and sections
- Code examples with expected output
- Links to related documentation

## Testing

### Required Tests

| Change Type | Required Tests |
|-------------|----------------|
| Formal model change | Unit tests |
| oTree app change | Bot tests |
| Treatment arm change | Integration tests |
| Documentation | Build verification |

### Running Tests

```bash
# All tests
python -m pytest testing/ -v

# Bot tests only
python testing/run_ai_growth_risk_bots.py --iterations 5

# Specific test file
python -m pytest testing/test_jones_models.py -v
```

## Documentation Contributions

### Updating Existing Docs

1. Find the relevant file in `docs/`
2. Edit the Markdown
3. Verify links work
4. Submit PR

### Adding New Docs

1. Determine the appropriate section
2. Create new `.md` file
3. Add links from parent README
4. Submit PR

### Style Guide

- Use ATX-style headers (`#`, `##`)
- Include code examples
- Add tables for structured data
- Link to related documentation
- Use admonitions sparingly

## Reporting Issues

### Bug Reports

Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (Python version, OS)
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternatives considered
- Mockups (if UI-related)

## Code of Conduct

Please review our [Code of Conduct](../../CODE_OF_CONDUCT.md) before contributing.

## Recognition

Contributors are recognized in:
- Release notes
- CONTRIBUTORS.md (for significant contributions)
- GitHub contributors page

## Questions?

- Open a [Discussion](https://github.com/ignaciourbina/otree-game/discussions)
- Check existing [Issues](https://github.com/ignaciourbina/otree-game/issues)

Thank you for contributing! 🎉
