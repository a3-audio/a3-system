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

#ifndef __MBED_ALLOC_UALLOC_H
#define __MBED_ALLOC_UALLOC_H

#include <stdint.h>
#include <stddef.h>
typedef struct UAllocTraitsExt UAllocTraitsExt_t;

#define UALLOC_TRAITS_BITMASK        1
#define UALLOC_TRAITS_NEVER_FREE    (1<<1 | (UALLOC_TRAITS_BITMASK))
#define UALLOC_TRAITS_ZERO_FILL     (1<<2 | (UALLOC_TRAITS_BITMASK))

#define UALLOC_RESERVED_MASK        ((~0UL) ^ (UALLOC_TRAITS_NEVER_FREE | UALLOC_TRAITS_ZERO_FILL))

#define UALLOC_TEST_TRAITS(x,T)\
    (!( (T) ^ ( (T) & (x) ) ))

#ifdef __cplusplus
extern "C"{
#endif
typedef enum {
    UALLOC_DEBUG_NONE = 0,
    UALLOC_DEBUG_FATAL,
    UALLOC_DEBUG_ERROR,
    UALLOC_DEBUG_WARNING,
    UALLOC_DEBUG_INFO,
    UALLOC_DEBUG_LOG,
    UALLOC_DEBUG_MAX
} UAllocDebug_t;

typedef union UAllocTraits {
    uint32_t flags;
    UAllocTraitsExt_t *extended;
} UAllocTraits_t;

/**
 * Allocate memory with traits
 *
 * ualloc allocates memory with traits. Traits are a way of specifying additional behaviour to the allocator.
 * Currently, ualloc supports a limited number of traits:
 * * UALLOC_TRAITS_NEVER_FREE: Allocate memory with krbs, which is interrupt-safe
 * * UALLOC_TRAITS_ZERO_FILL:  memset the returned memory to 0.
 * These traits can be used on their own or together.
 *
 * @param[in] bytes the number of bytes to allocates
 * @param[in] traits the traits to apply to the allocated memory
 * @return a pointer to the allocated memory on success, or NULL on failure.
 */
void * mbed_ualloc(size_t bytes, UAllocTraits_t);
/**
 * Reallocate the supplied memory
 *
 * If the supplied pointer is NULL, call ualloc instead
 * NOTE: If 0 is supplied as the number of bytes, this is passed through to the underlying allocator (dlmalloc) which
 * will invoke free.
 *
 * Traits are not currently supported in urealloc, since the semantics of handling zero-fill and never-free in realloc
 * are unclear.
 *
 * @param[in] ptr the pointer to reallocate
 * @param[in] bytes the new size for ptr
 * @param[in] traits the traits to apply to the new region (NOTE: Currently unsupported, must be 0)
 * @return the reallocated pointer
 */
void * mbed_urealloc(void * ptr, size_t bytes, UAllocTraits_t);
/**
 * ufree is a passthrough to the underlying free implementation.
 * ufree calls dlfree.
 *
 * @param[in] the pointer to free
 */
void mbed_ufree(void * ptr);

#ifdef __cplusplus
}
#endif

#endif // __MBED_ALLOC_UALLOC_H
