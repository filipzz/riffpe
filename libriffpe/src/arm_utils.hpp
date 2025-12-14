#pragma once

#include <arm_neon.h>
#include <arm_acle.h>

namespace riffpe
{
    namespace crypto
    {
        /** This helper inline queries CPU capabilites for AES NEON (AESE, AESMC, ...) support */
        // FIXME: currently only checks feature flags; no cross-platform solution found yet.
        inline bool has_armneon()
        {
            #if !defined(__ARM_FEATURE_AES) || !defined(__ARM_NEON__)
            return false;
            #else
            return __ARM_NEON__ && __ARM_FEATURE_AES;
            #endif
        }
    }
}
