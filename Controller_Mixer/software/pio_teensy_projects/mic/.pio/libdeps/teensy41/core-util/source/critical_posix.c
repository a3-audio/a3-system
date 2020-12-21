/*
 * Copyright (c) 2015-2016, ARM Limited, All Rights Reserved
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#if defined(TARGET_LIKE_POSIX)

// It's probably a better idea to define _POSIX_SOURCE in the target description
#ifndef _POSIX_SOURCE
#define _POSIX_SOURCE
#endif

#include <stdint.h>
#include <assert.h>
#include <unistd.h>
#include <signal.h>

// Module include
#include "core-util/critical.h"

static volatile unsigned irq_nesting_depth;
static sigset_t old_sig_set;

void core_util_critical_section_enter() {
    if (++irq_nesting_depth > 1) {
        return;
    }

    int rc;
    sigset_t full_set;
    rc = sigfillset(&full_set);
    assert(rc == 0);
    rc = sigprocmask(SIG_BLOCK, &full_set, &old_sig_set);
    assert(rc == 0);
}

void core_util_critical_section_exit() {
    assert(irq_nesting_depth > 0);
    if (--irq_nesting_depth == 0) {
        int rc = sigprocmask(SIG_SETMASK, &old_sig_set, NULL);
        assert(rc == 0);
    }
}

#endif // defined(TARGET_LIKE_POSIX)

