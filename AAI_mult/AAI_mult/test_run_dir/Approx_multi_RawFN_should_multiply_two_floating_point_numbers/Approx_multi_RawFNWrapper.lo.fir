FIRRTL version 1.1.0
circuit Approx_multi_RawFNWrapper :
  module Approx_multi_RawFN :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<8>
    input io_a_sig : UInt<23>
    input io_b_exp : UInt<8>
    input io_b_sig : UInt<23>
    input io_asyncResetSignal : AsyncReset
    output io_rawOut_exp : UInt<8>
    output io_rawOut_sig : UInt<23>

    node _T = eq(io_a_exp, UInt<1>("h0")) @[approx_multi.scala 36:21]
    node _T_1 = eq(io_a_sig, UInt<1>("h0")) @[approx_multi.scala 36:42]
    node _T_2 = and(_T, _T_1) @[approx_multi.scala 36:30]
    node _GEN_0 = mux(_T_2, UInt<1>("h1"), UInt<1>("h0")) @[approx_multi.scala 36:52 37:16 39:16]
    node _T_3 = eq(io_b_exp, UInt<1>("h0")) @[approx_multi.scala 42:21]
    node _T_4 = eq(io_b_sig, UInt<1>("h0")) @[approx_multi.scala 42:42]
    node _T_5 = and(_T_3, _T_4) @[approx_multi.scala 42:30]
    node _GEN_1 = mux(_T_5, UInt<1>("h1"), UInt<1>("h0")) @[approx_multi.scala 42:52 43:16 45:16]
    node a_iszero = _GEN_0 @[approx_multi.scala 34:24]
    node b_iszero = _GEN_1 @[approx_multi.scala 35:24]
    node notNaN_isZeroOut = or(a_iszero, b_iszero) @[approx_multi.scala 48:37]
    node _rawOut_exp_T = sub(io_a_exp, UInt<7>("h7f")) @[approx_multi.scala 51:31]
    node _rawOut_exp_T_1 = tail(_rawOut_exp_T, 1) @[approx_multi.scala 51:31]
    node _rawOut_exp_T_2 = add(_rawOut_exp_T_1, io_b_exp) @[approx_multi.scala 51:40]
    node rawOut_exp = tail(_rawOut_exp_T_2, 1) @[approx_multi.scala 51:40]
    node _rawOut_sig_T = cat(UInt<1>("h0"), io_a_sig) @[Cat.scala 33:92]
    node _rawOut_sig_T_1 = cat(UInt<1>("h0"), io_b_sig) @[Cat.scala 33:92]
    node _rawOut_sig_T_2 = add(_rawOut_sig_T, _rawOut_sig_T_1) @[approx_multi.scala 52:47]
    node _rawOut_sig_T_3 = tail(_rawOut_sig_T_2, 1) @[approx_multi.scala 52:47]
    node rawOut_sig = bits(_rawOut_sig_T_3, 23, 0) @[approx_multi.scala 52:75]
    reg rawOut_exp_reg : UInt<8>, clock with :
      reset => (io_asyncResetSignal, UInt<8>("h0")) @[approx_multi.scala 54:33]
    reg rawOut_sig_reg : UInt<24>, clock with :
      reset => (io_asyncResetSignal, UInt<24>("h0")) @[approx_multi.scala 55:33]
    node _T_6 = eq(notNaN_isZeroOut, UInt<1>("h1")) @[approx_multi.scala 57:28]
    node _T_7 = bits(rawOut_sig_reg, 23, 23) @[approx_multi.scala 60:32]
    node _T_8 = eq(_T_7, UInt<1>("h1")) @[approx_multi.scala 60:43]
    node _io_rawOut_exp_T = add(rawOut_exp_reg, UInt<1>("h1")) @[approx_multi.scala 61:41]
    node _io_rawOut_exp_T_1 = tail(_io_rawOut_exp_T, 1) @[approx_multi.scala 61:41]
    node _io_rawOut_sig_T = bits(rawOut_sig_reg, 22, 0) @[approx_multi.scala 65:40]
    node _GEN_2 = mux(_T_8, _io_rawOut_exp_T_1, rawOut_exp_reg) @[approx_multi.scala 60:52 61:23 64:23]
    node _GEN_3 = mux(_T_8, rawOut_sig_reg, _io_rawOut_sig_T) @[approx_multi.scala 60:52 62:23 65:23]
    node _GEN_4 = mux(_T_6, UInt<1>("h0"), _GEN_2) @[approx_multi.scala 57:37 58:23]
    node _GEN_5 = mux(_T_6, UInt<1>("h0"), _GEN_3) @[approx_multi.scala 57:37 59:23]
    io_rawOut_exp <= _GEN_4
    io_rawOut_sig <= bits(_GEN_5, 22, 0)
    rawOut_exp_reg <= rawOut_exp @[approx_multi.scala 54:{33,33,33}]
    rawOut_sig_reg <= rawOut_sig @[approx_multi.scala 55:{33,33,33}]

  module Approx_multi_RawFNWrapper :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<8>
    input io_a_sig : UInt<23>
    input io_b_exp : UInt<8>
    input io_b_sig : UInt<23>
    output io_rawOut_exp : UInt<8>
    output io_rawOut_sig : UInt<25>
    input io_resetDriver : UInt<1>
    input io_asyncResetSignal : AsyncReset

    inst Approx_multi_RawFN of Approx_multi_RawFN @[test.scala 19:34]
    node _Approx_multi_RawFN_io_asyncResetSignal_T = asAsyncReset(io_resetDriver) @[test.scala 23:60]
    io_rawOut_exp <= Approx_multi_RawFN.io_rawOut_exp @[test.scala 24:13]
    io_rawOut_sig <= pad(Approx_multi_RawFN.io_rawOut_sig, 25) @[test.scala 24:13]
    Approx_multi_RawFN.clock <= clock
    Approx_multi_RawFN.reset <= reset
    Approx_multi_RawFN.io_a_exp <= io_a_exp @[test.scala 21:27]
    Approx_multi_RawFN.io_a_sig <= io_a_sig @[test.scala 21:27]
    Approx_multi_RawFN.io_b_exp <= io_b_exp @[test.scala 22:27]
    Approx_multi_RawFN.io_b_sig <= io_b_sig @[test.scala 22:27]
    Approx_multi_RawFN.io_asyncResetSignal <= _Approx_multi_RawFN_io_asyncResetSignal_T @[test.scala 23:42]
