/* mbed Microcontroller Library
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
#ifndef MBED_FUNCTIONPOINTERBASE_H
#define MBED_FUNCTIONPOINTERBASE_H

#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>

#include "core-util/assert.h"
namespace mbed {
namespace util {

#define MBED_STATIC_ASSERT(MBED_STATIC_ASSERT_FAILED,MSG)\
    switch(0){\
        case 0:case (MBED_STATIC_ASSERT_FAILED): \
        break;}

template<typename R>
class FunctionPointerBind;

template<typename R>
class FunctionPointerBase {
public:
    inline operator bool(void) const {
        return (_membercaller != NULL) && (_object != NULL);
    }

    bool operator==(const FunctionPointerBase& other) const {
        return ((_object == other._object) && (memcmp(_member, other._member, sizeof(_member)) == 0));
    }

    bool operator!=(const FunctionPointerBase& other) const {
        return !(*this == other);
    }

    /**
     * Clears the current function pointer assignment
     * After clear(), this instance will point to nothing (NULL)
     */
    virtual void clear() {
        _membercaller = NULL;
        _object = NULL;
        memset(_member, 0, sizeof(_member));
    }

    /**
     * Calls the member pointed to by object::member or (function)object
     * @param arg
     * @return
     */
    inline R call(void* arg) {
#ifndef YOTTA_CFG_UTIL_FUNCTIONPOINTER_DISABLE_NULL_CHECK
        CORE_UTIL_ASSERT((_membercaller != NULL) && (_object != NULL));
#endif
        return _membercaller(_object, _member, arg);
    }

    FunctionPointerBase():_object(NULL), _membercaller(NULL) {
        memset(_member, 0, sizeof(_member));
    }
    FunctionPointerBase(const FunctionPointerBase<R> & fp) {
        copy(&fp);
    }
    virtual ~FunctionPointerBase() {

    }
protected:
    struct ArgOps {
        void (*copy_args)(void *, void *);
        void (*destructor)(void *);
    };

    // Forward declaration of an unknown class 
    class UnknownClass;
    // Forward declaration of an unknown member function to this an unknown class
    // this kind of declaration is authorized by the standard (see 8.3.3/2 of C++ 03 standard).  
    // As a result, the compiler will allocate for UnknownFunctionMember_t the biggest size 
    // and biggest alignment possible for member function. 
    // This type can be used inside unions, it will help to provide the storage 
    // with the proper size and alignment guarantees 
    typedef void (UnknownClass::*UnknownFunctionMember_t)();

    union { 
        char _member[sizeof(UnknownFunctionMember_t)];
        UnknownFunctionMember_t _alignementAndSizeGuarantees;
    };

    void * _object; // object Pointer/function pointer
    R (*_membercaller)(void *, char *, void *);
    static const struct ArgOps _nullops;

protected:

    void copy(const FunctionPointerBase<R> * fp) {
        _object = fp->_object;
        memcpy (_member, fp->_member, sizeof(_member));
        _membercaller = fp->_membercaller;
    }

    template <typename S>
    void * pre_bind(FunctionPointerBind<R> & fp, S * argStruct, const struct FunctionPointerBase<R>::ArgOps *ops)
    {
        MBED_STATIC_ASSERT(sizeof(S) <= sizeof(fp._storage), ERROR: Arguments too large for FunctionPointerBind internal storage)
        (void) argStruct;
        fp._ops = ops;
        return (void*)fp._storage;
    }
private:
    static void _null_copy_args(void *dest , void* src) {(void) dest; (void) src;}
    static void _null_destructor(void *args) {(void) args;}

};
template<typename R>
const struct FunctionPointerBase<R>::ArgOps FunctionPointerBase<R>::_nullops = {
    FunctionPointerBase<R>::_null_copy_args,
    FunctionPointerBase<R>::_null_destructor
};

} /* namespace util */
} /* namespace mbed */
#endif
