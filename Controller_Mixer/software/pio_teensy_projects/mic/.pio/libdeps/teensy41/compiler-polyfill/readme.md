## compiler-polyfill

A [yotta](http://github.com/ARMmbed/yotta) module to smooth over some of the
differences between compilers.

### API

#### Attributes
##### `__packed`
Pack a structure, preventing any padding from being added between fields.

```C
#include "compiler-polyfill/attributes.h"

struct foo{
   char x;
   int y;
} __packed;
```

##### `__align(N)`
Declare a type to be aligned on an N-byte boundary.

```C
#include "compiler-polyfill/attributes.h"

struct bar{
   int x;
} __align(16);
```

##### `__unused`
Declare a function argument to be unused, suppressing compiler warnings.

```C
#include "compiler-polyfill/attributes.h"

void foo(int __unused arg){
    
}
```

##### `__weak`
Mark a function as being weak.

**Note:** weak functions are not friendly to making code re-usable, as they can
only be overridden once (and if they are multiply overridden the linker will
emit no warning). You should not normally use weak symbols as part of the API
to re-usable yotta modules.

```C
#include "compiler-polyfill/attributes.h"

void __weak foo() {
    // a weak implementation of foo that can be overriden by a definition
    // without  __weak
}
```

##### `__deprecated`
Mark a function declaration as deprecated, if it used then a warning will be
issued by the compiler.

```C
#include "compiler-polyfill/attributes.h"

void foo(int arg) __deprecated;
```

##### `__deprecated_message("message string")`
Mark a function declaration as deprecated, if it used then a warning will be
issued by the compiler possibly including the provided message. Note that not
all compilers are able to display the message.

```C
#include "compiler-polyfill/attributes.h"

void foo(int arg) __deprecated_message("don't foo any more, bar instead");
```
