module AddRawFN(
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
`ifdef RANDOMIZE_REG_INIT
  reg [31:0] _RAND_0;
  reg [63:0] _RAND_1;
  reg [63:0] _RAND_2;
  reg [63:0] _RAND_3;
  reg [63:0] _RAND_4;
  reg [31:0] _RAND_5;
`endif // RANDOMIZE_REG_INIT
  wire  notSigNaN_invalidExc = io_a_isInf & io_b_isZero | io_a_isZero & io_b_isInf; // @[add.scala 37:60]
  wire [9:0] _sDiffExps_T = {1'h0,io_a_exp}; // @[Cat.scala 33:92]
  wire [9:0] _sDiffExps_T_1 = {1'h0,io_b_exp}; // @[Cat.scala 33:92]
  reg [9:0] sDiffExps_reg; // @[add.scala 48:32]
  wire [8:0] _modNatAlignDist_T_2 = 9'h0 - sDiffExps_reg[8:0]; // @[add.scala 51:28]
  wire [8:0] _GEN_0 = sDiffExps_reg[9] ? _modNatAlignDist_T_2 : sDiffExps_reg[8:0]; // @[add.scala 50:49 51:25 56:25]
  wire [8:0] common_exp = sDiffExps_reg[9] ? io_b_exp : io_a_exp; // @[add.scala 50:49 52:20 57:20]
  wire [22:0] small_sig = sDiffExps_reg[9] ? io_a_sig : io_b_sig; // @[add.scala 50:49 53:19 58:19]
  wire [22:0] large_sig = sDiffExps_reg[9] ? io_b_sig : io_a_sig; // @[add.scala 50:49 54:19 59:19]
  wire [47:0] _pre_shifted_sig_T = {2'h1,small_sig,23'h0}; // @[Cat.scala 33:92]
  wire [9:0] modNatAlignDist = {{1'd0}, _GEN_0}; // @[add.scala 44:31]
  reg [47:0] pre_shifted_sig_reg; // @[add.scala 63:38]
  reg [47:0] shifted_sig_reg; // @[add.scala 66:34]
  wire [47:0] _sig_sum_T = {2'h1,large_sig,23'h0}; // @[Cat.scala 33:92]
  wire [47:0] sig_sum = _sig_sum_T + shifted_sig_reg; // @[add.scala 68:65]
  reg [47:0] sig_sum_reg; // @[add.scala 69:30]
  wire [48:0] _fullrawout_sig_T = {sig_sum, 1'h0}; // @[add.scala 75:33]
  wire [8:0] _fullrawout_exp_T_1 = common_exp + 9'h1; // @[add.scala 76:36]
  wire [49:0] _fullrawout_sig_T_1 = {sig_sum, 2'h0}; // @[add.scala 79:33]
  wire [49:0] _GEN_4 = sig_sum_reg[47] ? {{1'd0}, _fullrawout_sig_T} : _fullrawout_sig_T_1; // @[add.scala 74:55 75:22 79:22]
  reg [47:0] fullrawout_sig_reg; // @[add.scala 85:37]
  wire  guardBit = fullrawout_sig_reg[24]; // @[add.scala 88:23]
  wire  roundBit = fullrawout_sig_reg[23]; // @[add.scala 89:23]
  wire  stickyBit = |fullrawout_sig_reg[22:0]; // @[add.scala 90:42]
  wire  leastSigBitOfResult = fullrawout_sig_reg[25]; // @[add.scala 91:34]
  wire  roundUp = guardBit & (roundBit | stickyBit | ~roundBit & ~stickyBit & leastSigBitOfResult); // @[add.scala 94:28]
  wire [22:0] preRoundSig = fullrawout_sig_reg[47:25]; // @[add.scala 95:26]
  wire [22:0] _rawOut_sig_reg_T_1 = preRoundSig + 23'h1; // @[add.scala 97:59]
  reg [22:0] rawOut_sig_reg; // @[add.scala 97:33]
  wire  _io_invalidExc_T_12 = io_a_isNaN & ~io_a_isInf & ~io_a_isZero & io_a_exp[7:0] == 8'hff & ~io_a_sig[22] &
    io_a_sig[21:0] != 22'h0; // @[add.scala 18:123]
  wire  _io_invalidExc_T_25 = io_b_isNaN & ~io_b_isInf & ~io_b_isZero & io_b_exp[7:0] == 8'hff & ~io_b_sig[22] &
    io_b_sig[21:0] != 22'h0; // @[add.scala 18:123]
  assign io_invalidExc = _io_invalidExc_T_12 | _io_invalidExc_T_25 | notSigNaN_invalidExc; // @[add.scala 104:99]
  assign io_rawOut_isNaN = io_a_isNaN | io_b_isNaN; // @[add.scala 101:35]
  assign io_rawOut_isInf = io_a_isInf | io_b_isInf; // @[add.scala 38:38]
  assign io_rawOut_isZero = io_a_isZero | io_b_isZero; // @[add.scala 39:40]
  assign io_rawOut_exp = sig_sum_reg[47] ? _fullrawout_exp_T_1 : common_exp; // @[add.scala 74:55 76:22 80:22]
  assign io_rawOut_sig = rawOut_sig_reg; // @[add.scala 98:19]
  always @(posedge clock) begin
    sDiffExps_reg <= _sDiffExps_T - _sDiffExps_T_1; // @[add.scala 46:45]
    pre_shifted_sig_reg <= _pre_shifted_sig_T >> modNatAlignDist; // @[add.scala 62:72]
    if (modNatAlignDist > 10'h18) begin // @[add.scala 65:26]
      shifted_sig_reg <= 48'h0;
    end else begin
      shifted_sig_reg <= pre_shifted_sig_reg;
    end
    sig_sum_reg <= _sig_sum_T + shifted_sig_reg; // @[add.scala 68:65]
    fullrawout_sig_reg <= _GEN_4[47:0]; // @[add.scala 72:30]
    if (roundUp) begin // @[add.scala 97:37]
      rawOut_sig_reg <= _rawOut_sig_reg_T_1;
    end else begin
      rawOut_sig_reg <= preRoundSig;
    end
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
  sDiffExps_reg = _RAND_0[9:0];
  _RAND_1 = {2{`RANDOM}};
  pre_shifted_sig_reg = _RAND_1[47:0];
  _RAND_2 = {2{`RANDOM}};
  shifted_sig_reg = _RAND_2[47:0];
  _RAND_3 = {2{`RANDOM}};
  sig_sum_reg = _RAND_3[47:0];
  _RAND_4 = {2{`RANDOM}};
  fullrawout_sig_reg = _RAND_4[47:0];
  _RAND_5 = {1{`RANDOM}};
  rawOut_sig_reg = _RAND_5[22:0];
`endif // RANDOMIZE_REG_INIT
  `endif // RANDOMIZE
end // initial
`ifdef FIRRTL_AFTER_INITIAL
`FIRRTL_AFTER_INITIAL
`endif
`endif // SYNTHESIS
endmodule
