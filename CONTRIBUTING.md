# Contributing to Low-Latency AI Agent Platform

We welcome contributions to the Low-Latency AI Agent Platform! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Rust 1.70+
- Python 3.8+
- OpenAI API key (for testing)

### Development Setup

1. **Fork the repository**:
   ```bash
   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/your-username/low_latency_ai_agent_platform.git
   cd low_latency_ai_agent_platform
   ```

2. **Set up development environment**:
   ```bash
   # Rust development
   cd rust-core
   cargo build
   cargo test

   # Python development
   cd ../python-agent
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Test Your Changes

```bash
# Rust tests
cd rust-core
cargo test
cargo clippy
cargo fmt --check

# Python tests
cd python-agent
python -m pytest

# Integration tests
cd demo
python rust_backend_demo.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: Add your feature description

- Detailed description of changes
- Reference relevant issues if any
- Include performance impact if applicable"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with a clear description of your changes.

## Code Style Guidelines

### Rust Code

- Use `cargo fmt` for formatting
- Use `cargo clippy` for linting
- Add comprehensive documentation comments
- Follow Rust naming conventions
- Include error handling with `anyhow::Result`

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings for all public functions and classes
- Handle exceptions properly
- Use async/await for I/O operations

### Documentation

- Update README.md for user-facing changes
- Add inline documentation for new features
- Include examples in docstrings
- Update API documentation

## Testing Guidelines

### Unit Tests

- Write unit tests for all new functionality
- Test both success and error cases
- Use descriptive test names
- Mock external dependencies when appropriate

### Integration Tests

- Test tool execution end-to-end
- Verify API endpoints work correctly
- Test error handling paths
- Include performance benchmarks for significant changes

### Performance Testing

- Run benchmarks before and after performance changes
- Document any performance regressions or improvements
- Use the existing benchmark suite in `demo/`

## Areas for Contribution

### High Priority

- [ ] Additional tool implementations (Database, Memory, etc.)
- [ ] gRPC communication support
- [ ] Parallel tool execution
- [ ] Advanced caching strategies
- [ ] Configuration file support

### Medium Priority

- [ ] Web dashboard for monitoring
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Prometheus metrics integration
- [ ] Comprehensive test suite

### Low Priority

- [ ] Tool marketplace
- [ ] Distributed execution
- [ ] Advanced AI reasoning patterns
- [ ] CLI interface
- [ ] GUI interface

## Submitting Changes

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Performance Impact
- [ ] No performance impact
- [ ] Performance improvement (describe)
- [ ] Performance regression (describe)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Code Review Process

1. **Self-Review**: Review your own code before submitting
2. **Peer Review**: Another contributor will review your changes
3. **Testing**: Ensure all tests pass
4. **Documentation**: Verify documentation is up to date
5. **Merge**: Once approved, your changes will be merged

## Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check the project documentation first
- **Examples**: Look at existing code for patterns

## Release Process

Releases are managed by project maintainers:

1. **Version bump**: Update version numbers
2. **Changelog**: Update CHANGELOG.md
3. **Tag**: Create git tag with version number
4. **Release**: Create GitHub release with notes

## Community Guidelines

- Be respectful and constructive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Low-Latency AI Agent Platform!
