/*
 * PackageLicenseDeclared: Apache-2.0
 * Copyright (c) 2015 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "ualloc/ualloc.h"
#include "core-util/sbrk.h"
#include "string.h"

extern void* dlmalloc(size_t);
extern void  dlfree(void*);
extern void* dlcalloc(size_t, size_t);
extern void* dlrealloc(void*, size_t);

extern int printf(const char *, ...);

extern void * volatile mbed_sbrk_ptr;

/*****************************************************************************************
UALLOC_DEBUG_LOG is effectively reserved for tracing memory allocations
Tracing must be enabled via "yotta config":
{
    "debug": {
        "options": {
            "memory-trace": true
        }
    }
}
[TODO]: ualloc_debug_level probably needs better control with "yotta config"
*****************************************************************************************/
#ifdef YOTTA_CFG_DEBUG_OPTIONS_MEMORY_TRACE
const UAllocDebug_t ualloc_debug_level = UALLOC_DEBUG_LOG;
#else
const UAllocDebug_t ualloc_debug_level = UALLOC_DEBUG_NONE;
#endif

// Debug characters
const char ua_chars[] = "NFEWIL";

/*****************************************************************************************
The purpose of "prevent_tracing" below is twofold:

1. prevent infinite loops (mbed_ualloc_internal -> ualloc_debug -> printf ->
   mbed_ualloc_internal -> ualloc_debug -> printf...)
2. prevent a possible scenario when an interrupt occurs while ualloc_debug
   is printing debug information and the interrupt also calls 'mbed_ualloc' or
   another memory operation that would result in ualloc_debug being called,
   which would in turn result in garbled output. By using "prevent_tracing",
   the output is kept consistent, but the memory operation invoked in the
   interrupt handler is not logged.

1 above can be prevented by using a logging function that doesn't allocate memory.
2 above can be prevented by queueing log messages instead of logging them immediately.
*****************************************************************************************/
static volatile int prevent_tracing = 0;

#define ualloc_debug(ADBG_LEVEL, fmt, ...) do {                              \
    if (ADBG_LEVEL <= ualloc_debug_level && ADBG_LEVEL < UALLOC_DEBUG_MAX) { \
        printf("UAL:%c " fmt, ua_chars[ADBG_LEVEL], __VA_ARGS__);            \
    }                                                                        \
} while (0)

/**
 * Helper function that identifies the caller of a function
 *
 * @return Address of the calling function
 */
#if defined(__ARMCC_VERSION)
    #define caller_addr() __builtin_return_address(0)
#elif defined(__GNUC__)
    #define caller_addr() __builtin_extract_return_addr(__builtin_return_address(0))
#else
    #define caller_addr() (NULL)
#endif

static void * mbed_ualloc_internal(size_t bytes, UAllocTraits_t traits, void *caller)
{
    void * ptr = NULL;
    if (UALLOC_TEST_TRAITS(traits.flags, UALLOC_TRAITS_NEVER_FREE)) {
        ptr = mbed_krbs(bytes);
        // krbs uses the same semantics as sbrk, so translate a -1 to NULL.
        if (ptr == (void*)-1) {
            ptr = NULL;
        }
        if ((ptr != NULL) && UALLOC_TEST_TRAITS(traits.flags, UALLOC_TRAITS_ZERO_FILL)) {
            memset(ptr, 0, bytes);
        }
    } else if (UALLOC_TEST_TRAITS(traits.flags, UALLOC_TRAITS_ZERO_FILL)) {
        ptr = dlcalloc(1, bytes);
    } else if (!(traits.flags & ~UALLOC_TRAITS_BITMASK)) {
        ptr = dlmalloc(bytes);
    } else if (traits.flags & UALLOC_RESERVED_MASK) {
        ualloc_debug(UALLOC_DEBUG_ERROR, "ua c:%p reserved: %lx\n", caller,
            traits.flags & UALLOC_RESERVED_MASK);
    }

    if(ptr == NULL) {
        ualloc_debug(UALLOC_DEBUG_WARNING, "ua c:%p fail\n", caller);
    }

    return ptr;
}

void *mbed_ualloc(size_t bytes, UAllocTraits_t traits)
{
    void *caller = (void*)caller_addr();
    void *p = mbed_ualloc_internal(bytes, traits, caller);
    if (!prevent_tracing) {
        prevent_tracing = 1;
        ualloc_debug(UALLOC_DEBUG_LOG, "ua c:%p s:%u m:%p\n", caller, (unsigned)bytes, p);
        prevent_tracing = 0;
    }
    return p;
}

static void * mbed_urealloc_internal(void * ptr, size_t bytes, UAllocTraits_t traits, void *caller)
{
    void *newptr = NULL;
    if (ptr == NULL) {
        return mbed_ualloc(bytes, traits);
    }
    if(traits.flags & ~UALLOC_TRAITS_BITMASK) {
        // Traits not supported in urealloc yet
        ualloc_debug(UALLOC_DEBUG_ERROR, "ur c:%p fail\n", caller);
        return NULL;
    }
    uintptr_t ptr_tmp = (uintptr_t) ptr;
    if ((ptr_tmp < (uintptr_t) mbed_sbrk_ptr) &&
            (ptr_tmp >= (uintptr_t)&__mbed_sbrk_start)) {
        newptr = dlrealloc(ptr, bytes);
    } else {
        ualloc_debug(UALLOC_DEBUG_ERROR, "ur c:%p m:%p non-heap realloc\n", caller, ptr);
    }

    if(newptr == NULL) {
        ualloc_debug(UALLOC_DEBUG_WARNING, "ur c:%p p:%p fail\n", caller, ptr);
    }
    return newptr;
}

void * mbed_urealloc(void * ptr, size_t bytes, UAllocTraits_t traits)
{
    void *caller = (void*)caller_addr();
    void *p = mbed_urealloc_internal(ptr, bytes, traits, caller);
    if (!prevent_tracing) {
        prevent_tracing = 1;
        ualloc_debug(UALLOC_DEBUG_LOG, "ur c:%p s:%u p:%p m:%p\n", caller, (unsigned)bytes, ptr, p);
        prevent_tracing = 0;
    }
    return p;
}

static void mbed_ufree_internal(void * ptr, void *caller)
{
    uintptr_t ptr_tmp = (uintptr_t) ptr;
    if ((ptr_tmp < (uintptr_t) mbed_sbrk_ptr) &&
            (ptr_tmp >= (uintptr_t)&__mbed_sbrk_start)) {
        dlfree(ptr);
    } else {
        ualloc_debug(UALLOC_DEBUG_WARNING, "uf c:%p m:%p non-heap free\n", caller, ptr);
    }
}

void mbed_ufree(void *ptr)
{
    void *caller = (void*)caller_addr();
    mbed_ufree_internal(ptr, caller);
    if (!prevent_tracing) {
        prevent_tracing = 1;
        ualloc_debug(UALLOC_DEBUG_LOG, "uf c:%p m:%p\n", caller, ptr);
        prevent_tracing = 0;
    }
}

