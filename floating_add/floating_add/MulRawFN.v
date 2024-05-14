module MulFullRawFN(
  input         io_a_isNaN,
  input         io_a_isInf,
  input         io_a_isZero,
  input  [9:0]  io_a_sExp,
  input  [22:0] io_a_sig,
  input         io_b_isNaN,
  input         io_b_isInf,
  input         io_b_isZero,
  input  [9:0]  io_b_sExp,
  input  [22:0] io_b_sig,
  output        io_invalidExc,
  output        io_rawOut_isNaN,
  output        io_rawOut_isInf,
  output        io_rawOut_isZero,
  output [9:0]  io_rawOut_sExp,
  output [47:0] io_rawOut_sig
);
  wire  notSigNaN_invalidExc = io_a_isInf & io_b_isZero | io_a_isZero & io_b_isInf; // @[multi.scala 34:60]
  wire  notNaN_isZeroOut = io_a_isZero | io_b_isZero; // @[multi.scala 36:40]
  wire [9:0] _common_sExpOut_T_2 = $signed(io_a_sExp) + $signed(io_b_sExp); // @[multi.scala 39:36]
  wire [9:0] common_sExpOut = $signed(_common_sExpOut_T_2) - 10'shff; // @[multi.scala 39:48]
  wire [23:0] _common_sigOut_T = {1'h1,io_a_sig}; // @[Cat.scala 33:92]
  wire [23:0] _common_sigOut_T_1 = {1'h1,io_b_sig}; // @[Cat.scala 33:92]
  wire [47:0] common_sigOut = _common_sigOut_T * _common_sigOut_T_1; // @[multi.scala 41:49]
  wire  _io_invalidExc_T_12 = io_a_isNaN & ~io_a_isInf & ~io_a_isZero & io_a_sExp[8:0] == 9'h1ff & ~io_a_sig[22] &
    io_a_sig[21:0] != 22'h0; // @[add.scala 18:124]
  wire  _io_invalidExc_T_25 = io_b_isNaN & ~io_b_isInf & ~io_b_isZero & io_b_sExp[8:0] == 9'h1ff & ~io_b_sig[22] &
    io_b_sig[21:0] != 22'h0; // @[add.scala 18:124]
  wire [9:0] _io_rawOut_sExp_T_2 = $signed(common_sExpOut) + 10'sh1; // @[multi.scala 57:42]
  wire [48:0] _io_rawOut_sig_T = {common_sigOut, 1'h0}; // @[multi.scala 58:40]
  wire [9:0] _GEN_0 = common_sigOut[47] ? $signed(_io_rawOut_sExp_T_2) : $signed(common_sExpOut); // @[multi.scala 56:60 57:24 60:24]
  wire [48:0] _GEN_1 = common_sigOut[47] ? _io_rawOut_sig_T : {{1'd0}, common_sigOut}; // @[multi.scala 56:60 58:23 61:23]
  wire [48:0] _GEN_3 = notNaN_isZeroOut ? 49'h0 : _GEN_1; // @[multi.scala 51:29 55:23]
  assign io_invalidExc = _io_invalidExc_T_12 | _io_invalidExc_T_25 | notSigNaN_invalidExc; // @[multi.scala 45:99]
  assign io_rawOut_isNaN = io_a_isNaN | io_b_isNaN; // @[multi.scala 49:35]
  assign io_rawOut_isInf = io_a_isInf | io_b_isInf; // @[multi.scala 35:38]
  assign io_rawOut_isZero = io_a_isZero | io_b_isZero; // @[multi.scala 36:40]
  assign io_rawOut_sExp = notNaN_isZeroOut ? $signed(10'sh0) : $signed(_GEN_0); // @[multi.scala 51:29 54:24]
  assign io_rawOut_sig = _GEN_3[47:0];
endmodule
module MulRawFN(
  input         io_a_isNaN,
  input         io_a_isInf,
  input         io_a_isZero,
  input  [9:0]  io_a_sExp,
  input  [22:0] io_a_sig,
  input         io_b_isNaN,
  input         io_b_isInf,
  input         io_b_isZero,
  input  [9:0]  io_b_sExp,
  input  [22:0] io_b_sig,
  output        io_invalidExc,
  output        io_rawOut_isNaN,
  output        io_rawOut_isInf,
  output        io_rawOut_isZero,
  output [9:0]  io_rawOut_sExp,
  output [22:0] io_rawOut_sig
);
  wire  mulFullRaw_io_a_isNaN; // @[multi.scala 74:28]
  wire  mulFullRaw_io_a_isInf; // @[multi.scala 74:28]
  wire  mulFullRaw_io_a_isZero; // @[multi.scala 74:28]
  wire [9:0] mulFullRaw_io_a_sExp; // @[multi.scala 74:28]
  wire [22:0] mulFullRaw_io_a_sig; // @[multi.scala 74:28]
  wire  mulFullRaw_io_b_isNaN; // @[multi.scala 74:28]
  wire  mulFullRaw_io_b_isInf; // @[multi.scala 74:28]
  wire  mulFullRaw_io_b_isZero; // @[multi.scala 74:28]
  wire [9:0] mulFullRaw_io_b_sExp; // @[multi.scala 74:28]
  wire [22:0] mulFullRaw_io_b_sig; // @[multi.scala 74:28]
  wire  mulFullRaw_io_invalidExc; // @[multi.scala 74:28]
  wire  mulFullRaw_io_rawOut_isNaN; // @[multi.scala 74:28]
  wire  mulFullRaw_io_rawOut_isInf; // @[multi.scala 74:28]
  wire  mulFullRaw_io_rawOut_isZero; // @[multi.scala 74:28]
  wire [9:0] mulFullRaw_io_rawOut_sExp; // @[multi.scala 74:28]
  wire [47:0] mulFullRaw_io_rawOut_sig; // @[multi.scala 74:28]
  wire  roundBit = mulFullRaw_io_rawOut_sig[23]; // @[multi.scala 87:23]
  wire  stickyBit = |mulFullRaw_io_rawOut_sig[22:0]; // @[multi.scala 88:42]
  wire  roundUp = roundBit & (mulFullRaw_io_rawOut_sig[24] | stickyBit); // @[multi.scala 89:28]
  wire [22:0] _io_rawOut_sig_T_2 = mulFullRaw_io_rawOut_sig[47:25] + 23'h1; // @[multi.scala 90:71]
  MulFullRawFN mulFullRaw ( // @[multi.scala 74:28]
    .io_a_isNaN(mulFullRaw_io_a_isNaN),
    .io_a_isInf(mulFullRaw_io_a_isInf),
    .io_a_isZero(mulFullRaw_io_a_isZero),
    .io_a_sExp(mulFullRaw_io_a_sExp),
    .io_a_sig(mulFullRaw_io_a_sig),
    .io_b_isNaN(mulFullRaw_io_b_isNaN),
    .io_b_isInf(mulFullRaw_io_b_isInf),
    .io_b_isZero(mulFullRaw_io_b_isZero),
    .io_b_sExp(mulFullRaw_io_b_sExp),
    .io_b_sig(mulFullRaw_io_b_sig),
    .io_invalidExc(mulFullRaw_io_invalidExc),
    .io_rawOut_isNaN(mulFullRaw_io_rawOut_isNaN),
    .io_rawOut_isInf(mulFullRaw_io_rawOut_isInf),
    .io_rawOut_isZero(mulFullRaw_io_rawOut_isZero),
    .io_rawOut_sExp(mulFullRaw_io_rawOut_sExp),
    .io_rawOut_sig(mulFullRaw_io_rawOut_sig)
  );
  assign io_invalidExc = mulFullRaw_io_invalidExc; // @[multi.scala 79:19]
  assign io_rawOut_isNaN = mulFullRaw_io_rawOut_isNaN; // @[multi.scala 80:15]
  assign io_rawOut_isInf = mulFullRaw_io_rawOut_isInf; // @[multi.scala 80:15]
  assign io_rawOut_isZero = mulFullRaw_io_rawOut_isZero; // @[multi.scala 80:15]
  assign io_rawOut_sExp = mulFullRaw_io_rawOut_sExp; // @[multi.scala 80:15]
  assign io_rawOut_sig = roundUp ? _io_rawOut_sig_T_2 : mulFullRaw_io_rawOut_sig[47:25]; // @[multi.scala 90:25]
  assign mulFullRaw_io_a_isNaN = io_a_isNaN; // @[multi.scala 76:21]
  assign mulFullRaw_io_a_isInf = io_a_isInf; // @[multi.scala 76:21]
  assign mulFullRaw_io_a_isZero = io_a_isZero; // @[multi.scala 76:21]
  assign mulFullRaw_io_a_sExp = io_a_sExp; // @[multi.scala 76:21]
  assign mulFullRaw_io_a_sig = io_a_sig; // @[multi.scala 76:21]
  assign mulFullRaw_io_b_isNaN = io_b_isNaN; // @[multi.scala 77:21]
  assign mulFullRaw_io_b_isInf = io_b_isInf; // @[multi.scala 77:21]
  assign mulFullRaw_io_b_isZero = io_b_isZero; // @[multi.scala 77:21]
  assign mulFullRaw_io_b_sExp = io_b_sExp; // @[multi.scala 77:21]
  assign mulFullRaw_io_b_sig = io_b_sig; // @[multi.scala 77:21]
endmodule
