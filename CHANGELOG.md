# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- Port class to deliver data to/from ImageOperations from WorkFlow

### Changed

## [0.2.0] - 2029-09-25

### Added
- 'ImageOperation' class created to hold an imported image analysis function.
- 'ImageOperationDirectory' class created to import, test and store ImageOperations.
- ImageOperation discovery and import using `importlib`.
- Security testing of imported code for permitted modules using `ast`.
- Functional testing of code prior to import.

### Changed
- Refactored `ImageParcel` to allow default `None` values for `shape` and `mapping`.
- Refactored `ImageOperation` to default input and output dictionaries as {} not None, rearranged code for readability and reduced bloat.

---

## [0.1.0] - 2026-09-06

### Added
- Core backend data structures (`ImageInt`, `ImageFloat`, `ImageBinary`, `ValueInt`, `ValueFloat`).
- `Shape` and `Image` classes supporting 4D arrays (C, Z, Y, X) and transposition.
- Initial `pytest` unit testing for all above classes.