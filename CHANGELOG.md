# Changelog

All notable changes to this project will be documented in this file. The format
is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Utilities for manipulating the CSS style of Streamlit buttons.

## [0.1.1] - 2023-08-15

### Fixed

- Refactored the `release` workflow that was not working properly.

### Changed

- Removed the `close` trigger of the `CI` workflow to prevent duplication.
- Changed the paths of the `CI` workflow to only trigger when necessary.
- Changed package classifiers (added several and removed the old ones).
- Added two new URLs to the project metadata.

## [0.1.0] - 2023-08-14

### Added

- The `session_state` decorator for easy interaction with Streamlit apps state.
- Initial release of the package.
