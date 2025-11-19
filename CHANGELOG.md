# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-19

### Added
- **Dashboard UI**: Streamlit-based interface for real-time monitoring.
- **Attack Simulation**: `Villain` module using AES-128 encryption.
- **Disaster Recovery**: `Hero` module for immutable backup restoration.
- **Metrics**: `Analyst` module for calculating Recovery Time Objective (RTO).
- **Safety**: `SafetyEnforcer` with strict sandbox confinement and root guard.
- **CI/CD**: GitHub Actions workflow for automated testing.
- **Documentation**: Comprehensive README, Contributing Guide, and Security Policy.
- **Logging**: Structured logging system replacing console prints.

### Security
- Implemented strict path validation to prevent directory traversal.
- Added root directory blocklist to prevent system damage.
