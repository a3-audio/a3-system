# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Fixed
- A race condition in `PoolAllocator::alloc()`


## [1.6.0] 2016-03-07
### Fixed
- Tests updated to use greentea client

## [1.5.4] 2016-03-04
### Fixed
- comment out assert in the critical section

## [1.5.3] 2016-03-02
### Fixed
- CriticalSectionLock to use the C based solution within the clas

### Added
- C critical section for nrf51 targets
- C critical section for posix targets

## [1.5.2] 2016-03-01
### Fixed
- Allocators aligned to 8
- nrf51 critical section - fixes use with the softdevice disabled

## [1.5.1] 2016-02-29
### Release
- mbed-drivers update dependency to 1.0.0

## [1.5.0] 2016-02-26
### Added
- C re-entrant critical section

## [1.4.0] 2016-02-24
### Fixed
- sbrk - align + set to minimum size negative sizes
- Test function pointer - set baud rate removal

## [1.3.0] 2016-02-15
### Added
- Add support for uninitialized data sections

## [1.2.0] 2016-02-01
### Release
- mbed-drivers update dependency to ~0.12.0

## [1.1.5] 2016-01-27
### Added
- Array, binaryHeap and pool allocators - forbid copying

## [1.1.4] 2016-01-20
### Fixed
- Newline termination for runtime errors

## [1.1.3] 2016-01-19
### Added
- Optimized specializations of atomic ops

## [1.1.3] 2016-01-19
### Fixed
- Add missing template specialization prototypes

## [1.1.1] 2016-01-14
### Fixed
- Shared pointer - API documentation

## [1.1.0] - 2016-01-11
### Fixed
- Function pointer - fix arguments (all types of arguments, including references)

### Changed
- core-util.h rename to assert.h

[Unreleased]: https://github.com/ARMmbed/core-util/compare/HEAD...v1.6.0
[1.6.0]: https://github.com/ARMmbed/core-util/compare/v1.5.4..v1.6.0
[1.5.4]: https://github.com/ARMmbed/core-util/compare/v1.5.3...v1.5.4
[1.5.3]: https://github.com/ARMmbed/core-util/compare/v1.5.2...v1.5.3
[1.5.2]: https://github.com/ARMmbed/core-util/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/ARMmbed/core-util/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/ARMmbed/core-util/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/ARMmbed/core-util/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/ARMmbed/core-util/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ARMmbed/core-util/compare/v1.1.5...v1.2.0
[1.1.5]: https://github.com/ARMmbed/core-util/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/ARMmbed/core-util/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/ARMmbed/core-util/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/ARMmbed/core-util/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/ARMmbed/core-util/compare/v1.1.1...v1.1.1
[1.1.0]: https://github.com/ARMmbed/core-util/compare/v1.1.0...v1.0.0
