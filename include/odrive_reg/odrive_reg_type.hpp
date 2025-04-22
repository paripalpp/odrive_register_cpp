#pragma once
#include <typeinfo>
#include <cstdint>
#include <cstddef>

namespace odrive_reg
{
    enum class OdriveRegType
    {
        Bool,
        UInt8,
        UInt16,
        UInt32,
        UInt64,
        Int32,
        Int64,
        Float,
        Function,
        EndpointRef,
    };

    template <uint32_t Id, OdriveRegType Type, bool Readable, bool Writable>
    struct OdriveReg
    {
        static constexpr uint32_t id = Id;
        static constexpr OdriveRegType type = Type;
        static constexpr bool readable = Readable;
        static constexpr bool writable = Writable;

        using value_type = typename std::conditional<Type == OdriveRegType::Bool, bool,
            typename std::conditional<Type == OdriveRegType::UInt8, uint8_t,
            typename std::conditional<Type == OdriveRegType::UInt16, uint16_t,
            typename std::conditional<Type == OdriveRegType::UInt32, uint32_t,
            typename std::conditional<Type == OdriveRegType::UInt64, uint64_t,
            typename std::conditional<Type == OdriveRegType::Int32, int32_t,
            typename std::conditional<Type == OdriveRegType::Int64, int64_t,
            typename std::conditional<Type == OdriveRegType::Float, float,
            void>::type>::type>::type>::type>::type>::type>::type>::type;

        static constexpr size_t size = sizeof(value_type);
    };
}
