FIRRTL version 1.1.0
circuit MulRawFNWrapper :
  module MulFullRawFN :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<11>
    input io_a_sig : UInt<52>
    input io_b_exp : UInt<11>
    input io_b_sig : UInt<52>
    input io_asyncResetSignal : AsyncReset
    output io_rawOut_exp : UInt<11>
    output io_rawOut_sig : UInt<106>

    node _T = eq(io_a_exp, UInt<1>("h0")) @[multi.scala 36:21]
    node _T_1 = eq(io_a_sig, UInt<1>("h0")) @[multi.scala 36:42]
    node _T_2 = and(_T, _T_1) @[multi.scala 36:30]
    node _GEN_0 = mux(_T_2, UInt<1>("h1"), UInt<1>("h0")) @[multi.scala 36:52 37:16 39:16]
    node _T_3 = eq(io_b_exp, UInt<1>("h0")) @[multi.scala 42:21]
    node _T_4 = eq(io_b_sig, UInt<1>("h0")) @[multi.scala 42:42]
    node _T_5 = and(_T_3, _T_4) @[multi.scala 42:30]
    node _GEN_1 = mux(_T_5, UInt<1>("h1"), UInt<1>("h0")) @[multi.scala 42:52 43:16 45:16]
    node a_iszero = _GEN_0 @[multi.scala 34:24]
    node b_iszero = _GEN_1 @[multi.scala 35:24]
    node notNaN_isZeroOut = or(a_iszero, b_iszero) @[multi.scala 48:37]
    node _common_expOut_T = add(io_a_exp, io_b_exp) @[multi.scala 51:34]
    node _common_expOut_T_1 = tail(_common_expOut_T, 1) @[multi.scala 51:34]
    node _common_expOut_T_2 = sub(_common_expOut_T_1, UInt<10>("h3ff")) @[multi.scala 51:45]
    node common_expOut = tail(_common_expOut_T_2, 1) @[multi.scala 51:45]
    node _common_sigOut_T = cat(UInt<1>("h1"), io_a_sig) @[Cat.scala 33:92]
    node _common_sigOut_T_1 = cat(UInt<1>("h1"), io_b_sig) @[Cat.scala 33:92]
    node _common_sigOut_T_2 = mul(_common_sigOut_T, _common_sigOut_T_1) @[multi.scala 53:49]
    node common_sigOut = bits(_common_sigOut_T_2, 105, 0) @[multi.scala 53:74]
    reg common_expOut_reg : UInt<11>, clock with :
      reset => (io_asyncResetSignal, UInt<11>("h0")) @[multi.scala 57:36]
    reg common_sigOut_reg : UInt<106>, clock with :
      reset => (io_asyncResetSignal, UInt<106>("h0")) @[multi.scala 58:36]
    node _T_6 = eq(notNaN_isZeroOut, UInt<1>("h1")) @[multi.scala 65:28]
    node _T_7 = bits(common_sigOut, 105, 105) @[multi.scala 68:31]
    node _T_8 = eq(_T_7, UInt<1>("h1")) @[multi.scala 68:54]
    node _io_rawOut_exp_T = add(common_expOut_reg, UInt<1>("h1")) @[multi.scala 69:44]
    node _io_rawOut_exp_T_1 = tail(_io_rawOut_exp_T, 1) @[multi.scala 69:44]
    node _io_rawOut_sig_T = shl(common_sigOut_reg, 1) @[multi.scala 70:44]
    node _io_rawOut_sig_T_1 = shl(common_sigOut_reg, 2) @[multi.scala 73:44]
    node _GEN_2 = mux(_T_8, _io_rawOut_exp_T_1, common_expOut_reg) @[multi.scala 68:63 69:23 72:23]
    node _GEN_3 = mux(_T_8, _io_rawOut_sig_T, _io_rawOut_sig_T_1) @[multi.scala 68:63 70:23 73:23]
    node _GEN_4 = mux(_T_6, UInt<1>("h0"), _GEN_2) @[multi.scala 65:37 66:23]
    node _GEN_5 = mux(_T_6, UInt<1>("h0"), _GEN_3) @[multi.scala 65:37 67:23]
    io_rawOut_exp <= _GEN_4
    io_rawOut_sig <= bits(_GEN_5, 105, 0)
    common_expOut_reg <= common_expOut @[multi.scala 57:{36,36,36}]
    common_sigOut_reg <= common_sigOut @[multi.scala 58:{36,36,36}]

  module MulRawFN :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<11>
    input io_a_sig : UInt<52>
    input io_b_exp : UInt<11>
    input io_b_sig : UInt<52>
    input io_asyncResetSignal : AsyncReset
    output io_rawOut_exp : UInt<11>
    output io_rawOut_sig : UInt<52>

    inst mulFullRaw of MulFullRawFN @[multi.scala 89:28]
    node guardBit = bits(mulFullRaw.io_rawOut_sig, 53, 53) @[multi.scala 101:23]
    node roundBit = bits(mulFullRaw.io_rawOut_sig, 52, 52) @[multi.scala 102:23]
    node _stickyBit_T = bits(mulFullRaw.io_rawOut_sig, 51, 0) @[multi.scala 103:24]
    node stickyBit = orr(_stickyBit_T) @[multi.scala 103:42]
    node leastSigBitOfResult = bits(mulFullRaw.io_rawOut_sig, 54, 54) @[multi.scala 104:34]
    node _roundUp_T = or(roundBit, stickyBit) @[multi.scala 107:40]
    node _roundUp_T_1 = eq(roundBit, UInt<1>("h0")) @[multi.scala 107:55]
    node _roundUp_T_2 = eq(stickyBit, UInt<1>("h0")) @[multi.scala 107:67]
    node _roundUp_T_3 = and(_roundUp_T_1, _roundUp_T_2) @[multi.scala 107:65]
    node _roundUp_T_4 = and(_roundUp_T_3, leastSigBitOfResult) @[multi.scala 107:78]
    node _roundUp_T_5 = or(_roundUp_T, _roundUp_T_4) @[multi.scala 107:52]
    node roundUp = and(guardBit, _roundUp_T_5) @[multi.scala 107:28]
    node _preRoundSig_T = bits(mulFullRaw.io_rawOut_sig, 105, 54) @[multi.scala 115:40]
    node preRoundSig = cat(UInt<1>("h0"), _preRoundSig_T) @[Cat.scala 33:92]
    node _rawOut_sig_T = add(preRoundSig, UInt<1>("h1")) @[multi.scala 117:47]
    node _rawOut_sig_T_1 = tail(_rawOut_sig_T, 1) @[multi.scala 117:47]
    node rawOut_sig = mux(roundUp, _rawOut_sig_T_1, preRoundSig) @[multi.scala 117:25]
    node _T = bits(rawOut_sig, 52, 52) @[multi.scala 119:21]
    node _T_1 = eq(_T, UInt<1>("h1")) @[multi.scala 119:32]
    node _rawOut_exp_T = add(mulFullRaw.io_rawOut_exp, UInt<1>("h1")) @[multi.scala 120:25]
    node _rawOut_exp_T_1 = tail(_rawOut_exp_T, 1) @[multi.scala 120:25]
    node _GEN_0 = mux(_T_1, _rawOut_exp_T_1, mulFullRaw.io_rawOut_exp) @[multi.scala 119:46 120:18 122:18]
    node _rawOut_sig_reg_T = bits(rawOut_sig, 51, 0) @[multi.scala 125:44]
    reg rawOut_sig_reg : UInt<52>, clock with :
      reset => (io_asyncResetSignal, UInt<52>("h0")) @[multi.scala 125:33]
    reg rawOut_exp_reg : UInt<11>, clock with :
      reset => (io_asyncResetSignal, UInt<11>("h0")) @[multi.scala 126:33]
    node rawOut_exp = _GEN_0 @[multi.scala 118:26]
    io_rawOut_exp <= rawOut_exp_reg @[multi.scala 128:19]
    io_rawOut_sig <= rawOut_sig_reg @[multi.scala 129:19]
    mulFullRaw.clock <= clock
    mulFullRaw.reset <= reset
    mulFullRaw.io_a_exp <= io_a_exp @[multi.scala 91:21]
    mulFullRaw.io_a_sig <= io_a_sig @[multi.scala 91:21]
    mulFullRaw.io_b_exp <= io_b_exp @[multi.scala 92:21]
    mulFullRaw.io_b_sig <= io_b_sig @[multi.scala 92:21]
    mulFullRaw.io_asyncResetSignal <= io_asyncResetSignal @[multi.scala 93:36]
    rawOut_sig_reg <= _rawOut_sig_reg_T @[multi.scala 125:{33,33,33}]
    rawOut_exp_reg <= rawOut_exp @[multi.scala 126:{33,33,33}]

  module MulRawFNWrapper :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<11>
    input io_a_sig : UInt<52>
    input io_b_exp : UInt<11>
    input io_b_sig : UInt<52>
    input io_resetDriver : UInt<1>
    input io_asyncResetSignal : AsyncReset
    output io_rawOut_exp : UInt<11>
    output io_rawOut_sig : UInt<54>

    inst mulRawFN of MulRawFN @[test.scala 20:24]
    node _mulRawFN_io_asyncResetSignal_T = asAsyncReset(io_resetDriver) @[test.scala 23:50]
    io_rawOut_exp <= mulRawFN.io_rawOut_exp @[test.scala 25:13]
    io_rawOut_sig <= pad(mulRawFN.io_rawOut_sig, 54) @[test.scala 25:13]
    mulRawFN.clock <= clock
    mulRawFN.reset <= reset
    mulRawFN.io_a_exp <= io_a_exp @[test.scala 21:17]
    mulRawFN.io_a_sig <= io_a_sig @[test.scala 21:17]
    mulRawFN.io_b_exp <= io_b_exp @[test.scala 22:17]
    mulRawFN.io_b_sig <= io_b_sig @[test.scala 22:17]
    mulRawFN.io_asyncResetSignal <= _mulRawFN_io_asyncResetSignal_T @[test.scala 23:32]
