#include <riffpe/AESEngine.hpp>

#if RIFFPE_HAVE_AESNI
#include "x86_utils.hpp"
#include "AESEngineAESNI.hpp"
#endif // RIFFPE_HAVE_AESNI

#include "AESEngineGeneric.hpp"

namespace riffpe
{
    namespace crypto
    {
        AESEngine* AESEngine::engine_factory()
        {
            #if RIFFPE_HAVE_AESNI
            // Check for runtime support and return an instance of AESEngineAESNI
            if(has_aesni())
                return new AESEngineAESNI();
            #endif // RIFFPE_HAVE_AESNI

            // Default: return a new AESEngineGeneric
            return new AESEngineGeneric();
        }
    } // namespace crypto
    
} // namespace riffpe
