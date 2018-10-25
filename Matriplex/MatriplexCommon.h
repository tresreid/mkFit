#ifndef MatriplexCommon_H
#define MatriplexCommon_H

#include <cmath>
#include <cstring>
#include <stdexcept>

// Use intrinsics version of code when available, done via CPP flags.
// #define  MPLEX_USE_INTRINSICS

//==============================================================================
// Intrinsics -- preamble
//==============================================================================

#include "immintrin.h"

#define mod(X, Y)  ((X) % (Y))

#if defined(MPLEX_USE_INTRINSICS)

  #if defined(__MIC__) || defined(__AVX__) || defined(__AVX512F__)

    #define MPLEX_INTRINSICS

  #endif

  #if defined(__MIC__) || defined(__AVX512F__)

    typedef __m512 IntrVec_t;
    #define MPLEX_INTRINSICS_WIDTH_BYTES  64
    #define MPLEX_INTRINSICS_WIDTH_BITS  512
    #define MIC_INTRINSICS

    #define LD(a, i)      _mm512_load_ps(&a[i*N+n])
    #define ST(a, i, r)   _mm512_store_ps(&a[i*N+n], r)
    #define ADD(a, b)     _mm512_add_ps(a, b) 
    #define MUL(a, b)     _mm512_mul_ps(a, b)
    #define FMA(a, b, v)  _mm512_fmadd_ps(a, b, v)

  #elif defined(__AVX__)

    typedef __m256 IntrVec_t;
    #define MPLEX_INTRINSICS_WIDTH_BYTES  32
    #define MPLEX_INTRINSICS_WIDTH_BITS  256
    #define AVX_INTRINSICS

    #define LD(a, i)      _mm256_load_ps(&a[i*N+n])
    #define ST(a, i, r)   _mm256_store_ps(&a[i*N+n], r)
    #define ADD(a, b)     _mm256_add_ps(a, b) 
    #define MUL(a, b)     _mm256_mul_ps(a, b)
    // #define FMA(a, b, v)  { __m256 temp = _mm256_mul_ps(a, b); v = _mm256_add_ps(temp, v); }
    inline __m256 FMA(const __m256 &a, const __m256 &b, const __m256 &v)
    {
      __m256 temp = _mm256_mul_ps(a, b); return _mm256_add_ps(temp, v);
    }

  #endif

#endif

//==============================================================================
// Intrinsics -- postamble
//==============================================================================

// #ifdef MPLEX_INTRINSICS

// #undef LD(a, i)
// #undef ADD(a, b)
// #undef MUL(a, b)
// #undef FMA(a, b, v)
// #undef ST(a, i, r)

// #undef MPLEX_INTRINSICS

// #endif
 
#ifndef HACK_SIZE
#define HACK_SIZE 100
#endif

namespace Matriplex
{
   typedef int idx_t;

   constexpr idx_t hacked_size = HACK_SIZE;
   constexpr idx_t h0 = mod(0,hacked_size);
   constexpr idx_t h1 = mod(1,hacked_size);
   constexpr idx_t h2 = mod(2,hacked_size);
   constexpr idx_t h3 = mod(3,hacked_size);
   constexpr idx_t h4 = mod(4,hacked_size);
   constexpr idx_t h5 = mod(5,hacked_size);
   constexpr idx_t h6 = mod(6,hacked_size);
   constexpr idx_t h7 = mod(7,hacked_size);
   constexpr idx_t h8 = mod(8,hacked_size);
   constexpr idx_t h9 = mod(9,hacked_size);
   constexpr idx_t h10 = mod(10,hacked_size);
   constexpr idx_t h11 = mod(11,hacked_size);
   constexpr idx_t h12 = mod(12,hacked_size);
   constexpr idx_t h13 = mod(13,hacked_size);
   constexpr idx_t h14 = mod(14,hacked_size);
   constexpr idx_t h15 = mod(15,hacked_size);
   constexpr idx_t h16 = mod(16,hacked_size);
   constexpr idx_t h17 = mod(17,hacked_size);
   constexpr idx_t h18 = mod(18,hacked_size);
   constexpr idx_t h19 = mod(19,hacked_size);
   constexpr idx_t h20 = mod(20,hacked_size);
   constexpr idx_t h21 = mod(21,hacked_size);
   constexpr idx_t h22 = mod(22,hacked_size);
   constexpr idx_t h23 = mod(23,hacked_size);
   constexpr idx_t h24 = mod(24,hacked_size);
   constexpr idx_t h25 = mod(25,hacked_size);
   constexpr idx_t h26 = mod(26,hacked_size);
   constexpr idx_t h27 = mod(27,hacked_size);
   constexpr idx_t h28 = mod(28,hacked_size);
   constexpr idx_t h29 = mod(29,hacked_size);
   constexpr idx_t h30 = mod(30,hacked_size);
   constexpr idx_t h31 = mod(31,hacked_size);
   constexpr idx_t h32 = mod(32,hacked_size);
   constexpr idx_t h33 = mod(33,hacked_size);
   constexpr idx_t h34 = mod(34,hacked_size);
   constexpr idx_t h35 = mod(35,hacked_size);
   constexpr idx_t h36 = mod(36,hacked_size);
   constexpr idx_t h37 = mod(37,hacked_size);
   constexpr idx_t h38 = mod(38,hacked_size);
   constexpr idx_t h39 = mod(39,hacked_size);

   inline void align_check(const char* pref, void *adr)
   {
      printf("%s 0x%llx  -  modulo 64 = %lld\n", pref, (long long unsigned)adr, (long long)adr%64);
   }
}

#endif
