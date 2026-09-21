# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dynamic plugin discovery using AST scanning and `importlib`.
- Template Method pattern in `ImageOperation` for centralized pre/post execution validation.

### Changed
- Refactored `ImageParcel` to allow default `None` values for `shape` and `mapping`.
- Refactored `ImageOperation` to default input and output dictionaries as {} not None, rearranged code for readability and reduced bloat.

---

## [0.1.0] - 2026-09-06

### Added
- Core backend data structures (`ImageInt`, `ImageFloat`, `ImageBinary`, `ValueInt`, `ValueFloat`).
- `Shape` and `Image` classes supporting 4D arrays (C, Z, Y, X) and transposition.
- Initial `pytest` unit testing for all above classes.