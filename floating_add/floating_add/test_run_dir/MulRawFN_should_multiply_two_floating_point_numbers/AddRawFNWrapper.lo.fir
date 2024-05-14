FIRRTL version 1.1.0
circuit AddRawFNWrapper :
  module AddRawFN :
    input clock : Clock
    input reset : UInt<1>
    input io_a_exp : UInt<8>
    input io_a_sig : UInt<23>
    input io_b_exp : UInt<8>
    input io_b_sig : UInt<23>
    output io_rawOut_exp : UInt<8>
    output io_rawOut_sig : UInt<23>
    input io_asyncResetSignal : AsyncReset

    node _T = eq(io_a_exp, UInt<1>("h0")) @[add.scala 38:21]
    node _T_1 = eq(io_a_sig, UInt<1>("h0")) @[add.scala 38:42]
    node _T_2 = and(_T, _T_1) @[add.scala 38:30]
    node _GEN_0 = mux(_T_2, UInt<1>("h1"), UInt<1>("h0")) @[add.scala 38:52 39:16 41:16]
    node _T_3 = eq(io_b_exp, UInt<1>("h0")) @[add.scala 44:21]
    node _T_4 = eq(io_b_sig, UInt<1>("h0")) @[add.scala 44:42]
    node _T_5 = and(_T_3, _T_4) @[add.scala 44:30]
    node _GEN_1 = mux(_T_5, UInt<1>("h1"), UInt<1>("h0")) @[add.scala 44:52 45:16 47:16]
    node a_iszero = _GEN_0 @[add.scala 36:24]
    node b_iszero = _GEN_1 @[add.scala 37:24]
    node notNaN_isZeroOut = and(a_iszero, b_iszero) @[add.scala 50:37]
    node _sDiffExps_T = cat(UInt<1>("h0"), io_a_exp) @[Cat.scala 33:92]
    node _sDiffExps_T_1 = cat(UInt<1>("h0"), io_b_exp) @[Cat.scala 33:92]
    node _sDiffExps_T_2 = sub(_sDiffExps_T, _sDiffExps_T_1) @[add.scala 57:45]
    node sDiffExps = tail(_sDiffExps_T_2, 1) @[add.scala 57:45]
    reg sDiffExps_reg : UInt<9>, clock with :
      reset => (io_asyncResetSignal, UInt<9>("h0")) @[add.scala 59:32]
    node _T_6 = bits(sDiffExps_reg, 8, 8) @[add.scala 61:24]
    node _T_7 = eq(_T_6, UInt<1>("h1")) @[add.scala 61:35]
    node _modNatAlignDist_T = bits(sDiffExps_reg, 7, 0) @[add.scala 62:42]
    node _modNatAlignDist_T_1 = sub(UInt<1>("h0"), _modNatAlignDist_T) @[add.scala 62:28]
    node _modNatAlignDist_T_2 = tail(_modNatAlignDist_T_1, 1) @[add.scala 62:28]
    node _modNatAlignDist_T_3 = bits(sDiffExps_reg, 7, 0) @[add.scala 67:41]
    node _GEN_2 = mux(_T_7, _modNatAlignDist_T_2, _modNatAlignDist_T_3) @[add.scala 61:49 62:25 67:25]
    node _GEN_3 = mux(_T_7, io_b_exp, io_a_exp) @[add.scala 61:49 63:20 68:20]
    node _GEN_4 = mux(_T_7, io_a_sig, io_b_sig) @[add.scala 61:49 64:19 69:19]
    node _GEN_5 = mux(_T_7, io_b_sig, io_a_sig) @[add.scala 61:49 65:19 70:19]
    node small_sig = _GEN_4 @[add.scala 53:25]
    node pre_shifted_sig_hi = cat(UInt<2>("h1"), small_sig) @[Cat.scala 33:92]
    node _pre_shifted_sig_T = cat(pre_shifted_sig_hi, UInt<23>("h0")) @[Cat.scala 33:92]
    node modNatAlignDist = pad(_GEN_2, 9) @[add.scala 55:31]
    node pre_shifted_sig = dshr(_pre_shifted_sig_T, modNatAlignDist) @[add.scala 73:72]
    reg pre_shifted_sig_reg : UInt<48>, clock with :
      reset => (io_asyncResetSignal, UInt<48>("h0")) @[add.scala 74:38]
    node _shifted_sig_T = gt(modNatAlignDist, UInt<5>("h18")) @[add.scala 76:43]
    node _shifted_sig_T_1 = mux(_shifted_sig_T, UInt<1>("h0"), pre_shifted_sig_reg) @[add.scala 76:26]
    node shifted_sig = bits(_shifted_sig_T_1, 47, 0) @[add.scala 76:88]
    reg shifted_sig_reg : UInt<48>, clock with :
      reset => (io_asyncResetSignal, UInt<48>("h0")) @[add.scala 77:34]
    node large_sig = _GEN_5 @[add.scala 54:25]
    node sig_sum_1_hi = cat(UInt<2>("h1"), large_sig) @[Cat.scala 33:92]
    node sig_sum_1 = cat(sig_sum_1_hi, UInt<23>("h0")) @[Cat.scala 33:92]
    node _sig_sum_T = add(sig_sum_1, shifted_sig_reg) @[add.scala 80:30]
    node _sig_sum_T_1 = tail(_sig_sum_T, 1) @[add.scala 80:30]
    node sig_sum = bits(_sig_sum_T_1, 47, 0) @[add.scala 80:48]
    reg sig_sum_reg : UInt<48>, clock with :
      reset => (io_asyncResetSignal, UInt<48>("h0")) @[add.scala 82:30]
    node _T_8 = eq(notNaN_isZeroOut, UInt<1>("h1")) @[add.scala 87:28]
    node _T_9 = eq(a_iszero, UInt<1>("h1")) @[add.scala 90:27]
    node _fullrawout_sig_T = cat(io_b_sig, UInt<25>("h0")) @[Cat.scala 33:92]
    node _T_10 = eq(b_iszero, UInt<1>("h1")) @[add.scala 93:27]
    node _fullrawout_sig_T_1 = cat(io_a_sig, UInt<25>("h0")) @[Cat.scala 33:92]
    node _T_11 = bits(sig_sum_reg, 47, 47) @[add.scala 96:29]
    node _T_12 = eq(_T_11, UInt<1>("h1")) @[add.scala 96:48]
    node _fullrawout_sig_T_2 = shl(sig_sum, 1) @[add.scala 97:33]
    node common_exp = _GEN_3 @[add.scala 52:26]
    node _fullrawout_exp_T = add(common_exp, UInt<1>("h1")) @[add.scala 98:36]
    node _fullrawout_exp_T_1 = tail(_fullrawout_exp_T, 1) @[add.scala 98:36]
    node _fullrawout_sig_T_3 = shl(sig_sum, 2) @[add.scala 101:33]
    node _GEN_6 = mux(_T_12, _fullrawout_sig_T_2, _fullrawout_sig_T_3) @[add.scala 101:22 96:62 97:22]
    node _GEN_7 = mux(_T_12, _fullrawout_exp_T_1, common_exp) @[add.scala 102:22 96:62 98:22]
    node _GEN_8 = mux(_T_10, _fullrawout_sig_T_1, _GEN_6) @[add.scala 93:36 94:22]
    node _GEN_9 = mux(_T_10, io_a_exp, _GEN_7) @[add.scala 93:36 95:22]
    node _GEN_10 = mux(_T_9, _fullrawout_sig_T, _GEN_8) @[add.scala 90:36 91:22]
    node _GEN_11 = mux(_T_9, io_b_exp, _GEN_9) @[add.scala 90:36 92:22]
    node _GEN_12 = mux(_T_8, UInt<1>("h0"), _GEN_10) @[add.scala 87:37 88:22]
    node _GEN_13 = mux(_T_8, UInt<1>("h0"), _GEN_11) @[add.scala 87:37 89:22]
    reg fullrawout_exp_reg : UInt<8>, clock with :
      reset => (io_asyncResetSignal, UInt<8>("h0")) @[add.scala 106:37]
    reg fullrawout_sig_reg : UInt<48>, clock with :
      reset => (io_asyncResetSignal, UInt<48>("h0")) @[add.scala 107:37]
    node guardBit = bits(fullrawout_sig_reg, 24, 24) @[add.scala 110:23]
    node roundBit = bits(fullrawout_sig_reg, 23, 23) @[add.scala 111:23]
    node _stickyBit_T = bits(fullrawout_sig_reg, 22, 0) @[add.scala 112:24]
    node stickyBit = orr(_stickyBit_T) @[add.scala 112:42]
    node leastSigBitOfResult = bits(fullrawout_sig_reg, 25, 25) @[add.scala 113:34]
    node _roundUp_T = or(roundBit, stickyBit) @[add.scala 116:40]
    node _roundUp_T_1 = eq(roundBit, UInt<1>("h0")) @[add.scala 116:55]
    node _roundUp_T_2 = eq(stickyBit, UInt<1>("h0")) @[add.scala 116:67]
    node _roundUp_T_3 = and(_roundUp_T_1, _roundUp_T_2) @[add.scala 116:65]
    node _roundUp_T_4 = and(_roundUp_T_3, leastSigBitOfResult) @[add.scala 116:78]
    node _roundUp_T_5 = or(_roundUp_T, _roundUp_T_4) @[add.scala 116:52]
    node roundUp = and(guardBit, _roundUp_T_5) @[add.scala 116:28]
    node _preRoundSig_T = bits(fullrawout_sig_reg, 47, 25) @[add.scala 117:40]
    node preRoundSig = cat(UInt<1>("h0"), _preRoundSig_T) @[Cat.scala 33:92]
    node _rawOut_sig_T = add(preRoundSig, UInt<1>("h1")) @[add.scala 119:47]
    node _rawOut_sig_T_1 = tail(_rawOut_sig_T, 1) @[add.scala 119:47]
    node rawOut_sig = mux(roundUp, _rawOut_sig_T_1, preRoundSig) @[add.scala 119:25]
    node _T_13 = bits(rawOut_sig, 23, 23) @[add.scala 121:21]
    node _T_14 = eq(_T_13, UInt<1>("h1")) @[add.scala 121:32]
    node _rawOut_exp_T = add(fullrawout_exp_reg, UInt<1>("h1")) @[add.scala 122:40]
    node _rawOut_exp_T_1 = tail(_rawOut_exp_T, 1) @[add.scala 122:40]
    node _GEN_14 = mux(_T_14, _rawOut_exp_T_1, fullrawout_exp_reg) @[add.scala 121:46 122:18 124:18]
    node _rawOut_sig_reg_T = bits(rawOut_sig, 22, 0) @[add.scala 127:44]
    reg rawOut_sig_reg : UInt<23>, clock with :
      reset => (io_asyncResetSignal, UInt<23>("h0")) @[add.scala 127:33]
    reg rawOut_exp_reg : UInt<8>, clock with :
      reset => (io_asyncResetSignal, UInt<8>("h0")) @[add.scala 128:33]
    node fullrawout_exp = _GEN_13 @[add.scala 84:30]
    node fullrawout_sig = bits(_GEN_12, 47, 0) @[add.scala 85:30]
    node rawOut_exp = _GEN_14 @[add.scala 120:26]
    io_rawOut_exp <= rawOut_exp_reg @[add.scala 132:19]
    io_rawOut_sig <= rawOut_sig_reg @[add.scala 130:19]
    sDiffExps_reg <= sDiffExps @[add.scala 59:{32,32,32}]
    pre_shifted_sig_reg <= pre_shifted_sig @[add.scala 74:{38,38,38}]
    shifted_sig_reg <= shifted_sig @[add.scala 77:{34,34,34}]
    sig_sum_reg <= sig_sum @[add.scala 82:{30,30,30}]
    fullrawout_exp_reg <= fullrawout_exp @[add.scala 106:{37,37,37}]
    fullrawout_sig_reg <= fullrawout_sig @[add.scala 107:{37,37,37}]
    rawOut_sig_reg <= _rawOut_sig_reg_T @[add.scala 127:{33,33,33}]
    rawOut_exp_reg <= rawOut_exp @[add.scala 128:{33,33,33}]

  module AddRawFNWrapper :
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

    inst addRawFN of AddRawFN @[test.scala 20:24]
    node _addRawFN_io_asyncResetSignal_T = asAsyncReset(io_resetDriver) @[test.scala 23:50]
    io_rawOut_exp <= addRawFN.io_rawOut_exp @[test.scala 25:13]
    io_rawOut_sig <= pad(addRawFN.io_rawOut_sig, 25) @[test.scala 25:13]
    addRawFN.clock <= clock
    addRawFN.reset <= reset
    addRawFN.io_a_exp <= io_a_exp @[test.scala 21:17]
    addRawFN.io_a_sig <= io_a_sig @[test.scala 21:17]
    addRawFN.io_b_exp <= io_b_exp @[test.scala 22:17]
    addRawFN.io_b_sig <= io_b_sig @[test.scala 22:17]
    addRawFN.io_asyncResetSignal <= _addRawFN_io_asyncResetSignal_T @[test.scala 23:32]
