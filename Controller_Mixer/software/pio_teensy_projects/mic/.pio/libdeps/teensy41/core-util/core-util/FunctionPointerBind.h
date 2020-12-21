/* mbed Microcontroller Library
 * Copyright (c) 2006-2015 ARM Limited
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

#ifndef MBED_FUNCTIONPOINTERBIND_H__
#define MBED_FUNCTIONPOINTERBIND_H__

#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <assert.h>
#include "core-util/FunctionPointerBase.h"


#ifdef YOTTA_CFG_UTIL_FUNCTIONPOINTER_ARG_STORAGE
#define EVENT_STORAGE_SIZE (YOTTA_CFG_UTIL_FUNCTIONPOINTER_ARG_STORAGE)
#else
#define EVENT_STORAGE_SIZE 32
#endif

#define MBED_STATIC_ASSERT(MBED_STATIC_ASSERT_FAILED,MSG)\
    switch(0){\
        case 0:case (MBED_STATIC_ASSERT_FAILED): \
        break;}

namespace mbed {
namespace util {

template <typename R>
class FunctionPointerBase;

template<typename R>
class FunctionPointerBind : public FunctionPointerBase<R> {
friend FunctionPointerBase<R>;
public:
    // Call the Event
    inline R call() {
        return FunctionPointerBase<R>::call(static_cast<void *>(_storage));
    }
    FunctionPointerBind():
        FunctionPointerBase<R>(),
        _ops(&FunctionPointerBase<R>::_nullops)
    {}

    FunctionPointerBind(const FunctionPointerBase<R> & fp) :
        FunctionPointerBase<R>(fp)
    {}

    FunctionPointerBind(const FunctionPointerBind<R> & fp):
        FunctionPointerBase<R>(),
        _ops(&FunctionPointerBase<R>::_nullops) {
        *this = fp;
    }

    virtual ~FunctionPointerBind() {
        _ops->destructor(_storage);
    }

    FunctionPointerBind<R> & operator=(const FunctionPointerBind<R>& rhs) {
        if (_ops != &FunctionPointerBase<R>::_nullops) {
            _ops->destructor(_storage);
        }
        FunctionPointerBase<R>::copy(&rhs);
        _ops = rhs._ops;
        _ops->copy_args(_storage, (void *)rhs._storage);
        return *this;
    }

    /**
     * Clears the current binding, making this instance unbound
     */
    virtual void clear() {
        if (_ops != &FunctionPointerBase<R>::_nullops) {
            _ops->destructor(_storage);
        }
        _ops = &FunctionPointerBase<R>::_nullops;
        FunctionPointerBase<R>::clear();
    }

    R operator()() {
        return call();
    }

protected:
    const struct FunctionPointerBase<R>::ArgOps * _ops;
    uint32_t _storage[(EVENT_STORAGE_SIZE+sizeof(uint32_t)-1)/sizeof(uint32_t)];
};

} /* namespace util */
} /* namespace mbed */

#endif // MBED_FUNCTIONPOINTERBIND_H__
