module MulFullRawFN(
  input         clock,
  input         io_a_isNaN,
  input         io_a_isInf,
  input         io_a_isZero,
  input  [8:0]  io_a_exp,
  input  [22:0] io_a_sig,
  input         io_b_isNaN,
  input         io_b_isInf,
  input         io_b_isZero,
  input  [8:0]  io_b_exp,
  input  [22:0] io_b_sig,
  output        io_invalidExc,
  output        io_rawOut_isNaN,
  output        io_rawOut_isInf,
  output        io_rawOut_isZero,
  output [8:0]  io_rawOut_exp,
  output [47:0] io_rawOut_sig
);
`ifdef RANDOMIZE_REG_INIT
  reg [31:0] _RAND_0;
  reg [63:0] _RAND_1;
`endif // RANDOMIZE_REG_INIT
  wire  notSigNaN_invalidExc = io_a_isInf & io_b_isZero | io_a_isZero & io_b_isInf; // @[multi.scala 34:60]
  wire  notNaN_isZeroOut = io_a_isZero | io_b_isZero; // @[multi.scala 36:40]
  wire [8:0] _common_expOut_T_1 = io_a_exp + io_b_exp; // @[multi.scala 39:34]
  wire [23:0] _common_sigOut_T = {1'h1,io_a_sig}; // @[Cat.scala 33:92]
  wire [23:0] _common_sigOut_T_1 = {1'h1,io_b_sig}; // @[Cat.scala 33:92]
  wire [47:0] common_sigOut = _common_sigOut_T * _common_sigOut_T_1; // @[multi.scala 41:49]
  reg [8:0] common_expOut_reg; // @[multi.scala 45:36]
  reg [47:0] common_sigOut_reg; // @[multi.scala 46:36]
  wire  _io_invalidExc_T_11 = io_a_isNaN & ~io_a_isInf & ~io_a_isZero & io_a_exp == 9'h1ff & ~io_a_sig[22] & io_a_sig[21
    :0] != 22'h0; // @[multi.scala 19:106]
  wire  _io_invalidExc_T_23 = io_b_isNaN & ~io_b_isInf & ~io_b_isZero & io_b_exp == 9'h1ff & ~io_b_sig[22] & io_b_sig[21
    :0] != 22'h0; // @[multi.scala 19:106]
  wire [8:0] _io_rawOut_exp_T_1 = common_expOut_reg + 9'h1; // @[multi.scala 59:44]
  wire [48:0] _io_rawOut_sig_T = {common_sigOut_reg, 1'h0}; // @[multi.scala 60:44]
  wire [49:0] _io_rawOut_sig_T_1 = {common_sigOut_reg, 2'h0}; // @[multi.scala 63:44]
  wire [8:0] _GEN_0 = common_sigOut[47] ? _io_rawOut_exp_T_1 : common_expOut_reg; // @[multi.scala 58:63 59:23 62:23]
  wire [49:0] _GEN_1 = common_sigOut[47] ? {{1'd0}, _io_rawOut_sig_T} : _io_rawOut_sig_T_1; // @[multi.scala 58:63 60:23 63:23]
  wire [49:0] _GEN_3 = notNaN_isZeroOut ? 50'h0 : _GEN_1; // @[multi.scala 55:29 57:23]
  assign io_invalidExc = _io_invalidExc_T_11 | _io_invalidExc_T_23 | notSigNaN_invalidExc; // @[multi.scala 49:99]
  assign io_rawOut_isNaN = io_a_isNaN | io_b_isNaN; // @[multi.scala 53:35]
  assign io_rawOut_isInf = io_a_isInf | io_b_isInf; // @[multi.scala 35:38]
  assign io_rawOut_isZero = io_a_isZero | io_b_isZero; // @[multi.scala 36:40]
  assign io_rawOut_exp = notNaN_isZeroOut ? 9'h0 : _GEN_0; // @[multi.scala 55:29 56:23]
  assign io_rawOut_sig = _GEN_3[47:0];
  always @(posedge clock) begin
    common_expOut_reg <= _common_expOut_T_1 - 9'hff; // @[multi.scala 39:45]
    common_sigOut_reg <= _common_sigOut_T * _common_sigOut_T_1; // @[multi.scala 41:49]
  end
// Register and memory initialization
`ifdef RANDOMIZE_GARBAGE_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_INVALID_ASSIGN
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_REG_INIT
`define RANDOMIZE
`endif
`ifdef RANDOMIZE_MEM_INIT
`define RANDOMIZE
`endif
`ifndef RANDOM
`define RANDOM $random
`endif
`ifdef RANDOMIZE_MEM_INIT
  integer initvar;
`endif
`ifndef SYNTHESIS
`ifdef FIRRTL_BEFORE_INITIAL
`FIRRTL_BEFORE_INITIAL
`endif
initial begin
  `ifdef RANDOMIZE
    `ifdef INIT_RANDOM
      `INIT_RANDOM
    `endif
    `ifndef VERILATOR
      `ifdef RANDOMIZE_DELAY
        #`RANDOMIZE_DELAY begin end
      `else
        #0.002 begin end
      `endif
    `endif
`ifdef RANDOMIZE_REG_INIT
  _RAND_0 = {1{`RANDOM}};
  common_expOut_reg = _RAND_0[8:0];
  _RAND_1 = {2{`RANDOM}};
  common_sigOut_reg = _RAND_1[47:0];
`endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
end // initial
`ifdef FIRRTL_AFTER_INITIAL
`FIRRTL_AFTER_INITIAL
`endif
`endif // SYNTHESIS
endmodule
module MulRawFN(
  input         clock,
  input         reset,
  input         io_a_isNaN,
  input         io_a_isInf,
  input         io_a_isZero,
  input  [8:0]  io_a_exp,
  input  [22:0] io_a_sig,
  input         io_b_isNaN,
  input         io_b_isInf,
  input         io_b_isZero,
  input  [8:0]  io_b_exp,
  input  [22:0] io_b_sig,
  output        io_invalidExc,
  output        io_rawOut_isNaN,
  output        io_rawOut_isInf,
  output        io_rawOut_isZero,
  output [8:0]  io_rawOut_exp,
  output [22:0] io_rawOut_sig
);
  wire  mulFullRaw_clock; // @[multi.scala 77:28]
  wire  mulFullRaw_io_a_isNaN; // @[multi.scala 77:28]
  wire  mulFullRaw_io_a_isInf; // @[multi.scala 77:28]
  wire  mulFullRaw_io_a_isZero; // @[multi.scala 77:28]
  wire [8:0] mulFullRaw_io_a_exp; // @[multi.scala 77:28]
  wire [22:0] mulFullRaw_io_a_sig; // @[multi.scala 77:28]
  wire  mulFullRaw_io_b_isNaN; // @[multi.scala 77:28]
  wire  mulFullRaw_io_b_isInf; // @[multi.scala 77:28]
  wire  mulFullRaw_io_b_isZero; // @[multi.scala 77:28]
  wire [8:0] mulFullRaw_io_b_exp; // @[multi.scala 77:28]
  wire [22:0] mulFullRaw_io_b_sig; // @[multi.scala 77:28]
  wire  mulFullRaw_io_invalidExc; // @[multi.scala 77:28]
  wire  mulFullRaw_io_rawOut_isNaN; // @[multi.scala 77:28]
  wire  mulFullRaw_io_rawOut_isInf; // @[multi.scala 77:28]
  wire  mulFullRaw_io_rawOut_isZero; // @[multi.scala 77:28]
  wire [8:0] mulFullRaw_io_rawOut_exp; // @[multi.scala 77:28]
  wire [47:0] mulFullRaw_io_rawOut_sig; // @[multi.scala 77:28]
  wire  guardBit = mulFullRaw_io_rawOut_sig[24]; // @[multi.scala 86:23]
  wire  roundBit = mulFullRaw_io_rawOut_sig[23]; // @[multi.scala 87:23]
  wire  stickyBit = |mulFullRaw_io_rawOut_sig[22:0]; // @[multi.scala 88:42]
  wire  leastSigBitOfResult = mulFullRaw_io_rawOut_sig[25]; // @[multi.scala 89:34]
  wire  roundUp = guardBit & (roundBit | stickyBit | ~roundBit & ~stickyBit & leastSigBitOfResult); // @[multi.scala 92:28]
  wire [22:0] preRoundSig = mulFullRaw_io_rawOut_sig[47:25]; // @[multi.scala 93:26]
  wire [22:0] _io_rawOut_sig_T_1 = preRoundSig + 23'h1; // @[multi.scala 97:47]
  MulFullRawFN mulFullRaw ( // @[multi.scala 77:28]
    .clock(mulFullRaw_clock),
    .io_a_isNaN(mulFullRaw_io_a_isNaN),
    .io_a_isInf(mulFullRaw_io_a_isInf),
    .io_a_isZero(mulFullRaw_io_a_isZero),
    .io_a_exp(mulFullRaw_io_a_exp),
    .io_a_sig(mulFullRaw_io_a_sig),
    .io_b_isNaN(mulFullRaw_io_b_isNaN),
    .io_b_isInf(mulFullRaw_io_b_isInf),
    .io_b_isZero(mulFullRaw_io_b_isZero),
    .io_b_exp(mulFullRaw_io_b_exp),
    .io_b_sig(mulFullRaw_io_b_sig),
    .io_invalidExc(mulFullRaw_io_invalidExc),
    .io_rawOut_isNaN(mulFullRaw_io_rawOut_isNaN),
    .io_rawOut_isInf(mulFullRaw_io_rawOut_isInf),
    .io_rawOut_isZero(mulFullRaw_io_rawOut_isZero),
    .io_rawOut_exp(mulFullRaw_io_rawOut_exp),
    .io_rawOut_sig(mulFullRaw_io_rawOut_sig)
  );
  assign io_invalidExc = mulFullRaw_io_invalidExc; // @[multi.scala 82:19]
  assign io_rawOut_isNaN = mulFullRaw_io_rawOut_isNaN; // @[multi.scala 83:15]
  assign io_rawOut_isInf = mulFullRaw_io_rawOut_isInf; // @[multi.scala 83:15]
  assign io_rawOut_isZero = mulFullRaw_io_rawOut_isZero; // @[multi.scala 83:15]
  assign io_rawOut_exp = mulFullRaw_io_rawOut_exp; // @[multi.scala 83:15]
  assign io_rawOut_sig = roundUp ? _io_rawOut_sig_T_1 : preRoundSig; // @[multi.scala 97:25]
  assign mulFullRaw_clock = clock;
  assign mulFullRaw_io_a_isNaN = io_a_isNaN; // @[multi.scala 79:21]
  assign mulFullRaw_io_a_isInf = io_a_isInf; // @[multi.scala 79:21]
  assign mulFullRaw_io_a_isZero = io_a_isZero; // @[multi.scala 79:21]
  assign mulFullRaw_io_a_exp = io_a_exp; // @[multi.scala 79:21]
  assign mulFullRaw_io_a_sig = io_a_sig; // @[multi.scala 79:21]
  assign mulFullRaw_io_b_isNaN = io_b_isNaN; // @[multi.scala 80:21]
  assign mulFullRaw_io_b_isInf = io_b_isInf; // @[multi.scala 80:21]
  assign mulFullRaw_io_b_isZero = io_b_isZero; // @[multi.scala 80:21]
  assign mulFullRaw_io_b_exp = io_b_exp; // @[multi.scala 80:21]
  assign mulFullRaw_io_b_sig = io_b_sig; // @[multi.scala 80:21]
endmodule
