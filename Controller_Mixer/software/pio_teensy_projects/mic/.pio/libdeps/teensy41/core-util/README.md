# mbed utilities library

Implementation of various generic data structures and algorithms used in mbed.

# Configuration
Some parameters of the core-util library can be configured in yotta.  Currently, core-util supports configuring two things: the argument storage size of FunctionPointerBind and whether or not FunctionPointer checks its arguments before calling

## Configuring the storage size for FunctionPointerBind's bound arguments
In some cases it may be necessary to increase FunctionPointerBind's argument size.  In others, for memory optimization, it may be necessary to decrease the size of FunctionPointerBind's bound arguments.  If either of these are necessary, adding a new key with yotta config will allow this configuration: ```"util": {"functionPointer":{"arg-storage" : <bytes>}}```.

## Configuring whether or not FunctionPointer checks its arguments before calling
For debug purposes, it is possible to have FunctionPointer check its arguments before being called.   If it checks its arguments, it will use a ```CORE_UTIL_ASSERT```.  Checks can be disabled with: ```"util": {"functionPointer":{"disable-null-check" : true}}```

# Atomic operations
This module provides three atomic primitives:

* ```atomic_cas```
* ```atomic_incr```
* ```atomic_decr```

The most versatile API is ```atomic_cas``` which provides the facility to implement any other atomic API. The base versions of ```atomic_incr``` and ```atomic_decr``` are implemented using ```atomic_cas```.

## Writing atomic operations
It is possible to implement all atomic operations using ```atomic_cas``` and this API is portable across platforms. When writing a new atomic operation, best practice is to implement it using existing atomic operations, which are cross-platform. If an optimization is needed, then it should be a specialization of the portable implementation, which compiles for a specific target.

### Example of writing an atomic operation
To illustrate how to write an atomic operation, consider ```atomic_add```. The signature of ```atomic_add``` will be:

```C++
/**
 * atomic_add
 * Add a non-atomic value to an atomic variable and store the result back to the atomic variable.
 * @param[in,out] ptr The atomic variable
 * @param[in] val The non-atomic value
 *
 * @return the value of the atomic variable after the addition
 */
template <typename T>
T atomic_add(T * ptr, T val);
```

The first implementation for this API is the generic, portable implementation:

```C++
template <typename T>
T atomic_add(T * ptr, T val)
{
    T oldValue = *ptr;
    T newValue;
    do {
        newValue = oldValue + val;
    //This compares oldValue to *ptr, and updates oldValue if *ptr has changed
    } while (!atomic_cas(ptr, &oldValue, newValue));
    return newValue;
}
```

If a more optimized version is required, the next step is to provide a template specialization which is conditionally selected, based on the processor. The specialization must be declared in the ```atomic_ops.h``` header, and the implementation must be defined in the ```atomic_ops.cpp``` source file.

Here is an example implementation:

```C++
#if (__CORTEX_M >= 0x03)
template<>
uint32_t atomic_add(uint32_t * ptr, uint32_t val)
{
    uint32_t newValue;
    do {
        newValue = __LDREXW(ptr) + val;
    } while (__STREXW(newValue, ptr));
    return newValue;
}
#endif
```
