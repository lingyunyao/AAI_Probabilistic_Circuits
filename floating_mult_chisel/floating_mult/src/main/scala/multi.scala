import chisel3._
import chisel3.stage.{ChiselStage, ChiselGeneratorAnnotation}
//import consts._
//import hardfloat._
import chisel3.util._


class RawFloat(expWidth: Int, sigWidth: Int) extends Bundle {
//  val isNaN = Bool()
//  val isInf = Bool()
//  val isZero = Bool()
  val exp = UInt((expWidth).W)
  val sig = UInt(sigWidth.W)
}


//class MulFullRawFN(expWidth: Int, sigWidth: Int) extends chisel3.RawModule
class MulFullRawFN(expWidth: Int, sigWidth: Int) extends Module
{
    val io = IO(new Bundle {
        val a = Input(new RawFloat(expWidth, sigWidth))
        val b = Input(new RawFloat(expWidth, sigWidth))
        val asyncResetSignal = Input(AsyncReset())
//        val invalidExc = Output(Bool())
        val rawOut = Output(new RawFloat(expWidth, (sigWidth + 1)*2))
    })

    /*------------------------------------------------------------------------
    *------------------------------------------------------------------------*/
//    val notSigNaN_invalidExc = (io.a.isInf && io.b.isZero) || (io.a.isZero && io.b.isInf)
//    val notNaN_isInfOut = io.a.isInf || io.b.isInf

    withReset(io.asyncResetSignal) {
    val a_iszero = Wire(UInt(1.W))
    val b_iszero = Wire(UInt(1.W))
    when ((io.a.exp === 0.U) & (io.a.sig === 0.U)) {
      a_iszero := 1.U
    }.otherwise {
      a_iszero := 0.U
    }

    when ((io.b.exp === 0.U) & (io.b.sig === 0.U)) {
      b_iszero := 1.U
    }.otherwise {
      b_iszero := 0.U
    }

    val notNaN_isZeroOut = a_iszero | b_iszero
    //val notNaN_signOut = io.a.sign ^ io.b.sign
    val bias = (1 << (expWidth - 1)) - 1
    val common_expOut = io.a.exp + io.b.exp - bias.U
    //val common_sExpOut = io.a.sExp + io.b.sExp - (1<<expWidth).S
    val common_sigOut = (Cat(1.U(1.W),io.a.sig) * Cat(1.U(1.W),io.b.sig))((sigWidth + 1)*2 - 1, 0)
    /*------------------------------------------------------------------------
    *------------------------------------------------------------------------*/

    val common_expOut_reg = RegNext(common_expOut, init = 0.U)
    val common_sigOut_reg = RegNext(common_sigOut, init = 0.U)
    
    //io.invalidExc := isSigNaNRawFloat(io.a) || isSigNaNRawFloat(io.b) || notSigNaN_invalidExc
    //io.invalidExc := Utils.isSigNaNUnsignedRawFloat(io.a) || Utils.isSigNaNUnsignedRawFloat(io.b) || notSigNaN_invalidExc
    //io.rawOut.isInf := notNaN_isInfOut
    //io.rawOut.isZero := notNaN_isZeroOut
    //io.rawOut.isNaN := io.a.isNaN || io.b.isNaN
    when (notNaN_isZeroOut === 1.U) {
        io.rawOut.exp := 0.U
        io.rawOut.sig := 0.U
    } .elsewhen (common_sigOut((sigWidth + 1)*2 - 1) === 1.U) {
        io.rawOut.exp := common_expOut_reg + 1.U
        io.rawOut.sig := common_sigOut_reg << 1
    }.otherwise {
        io.rawOut.exp := common_expOut_reg
        io.rawOut.sig := common_sigOut_reg << 2
    }
    }
}

//class MulRawFN(expWidth: Int, sigWidth: Int) extends chisel3.RawModule
class MulRawFN(expWidth: Int, sigWidth: Int) extends Module
{
    val io = IO(new Bundle {
        val a = Input(new RawFloat(expWidth, sigWidth))
        val b = Input(new RawFloat(expWidth, sigWidth))
        val asyncResetSignal = Input(AsyncReset())
//        val invalidExc = Output(Bool())
        val rawOut = Output(new RawFloat(expWidth, sigWidth))
    })

    val mulFullRaw = Module(new MulFullRawFN(expWidth, sigWidth))

    mulFullRaw.io.a := io.a
    mulFullRaw.io.b := io.b
    mulFullRaw.io.asyncResetSignal := io.asyncResetSignal

    withReset(io.asyncResetSignal) {
//    io.invalidExc := mulFullRaw.io.invalidExc
    io.rawOut := mulFullRaw.io.rawOut

    val sig = mulFullRaw.io.rawOut.sig
    val exp = mulFullRaw.io.rawOut.exp
    val guardBit = sig(sigWidth + 1) // G
    val roundBit = sig(sigWidth) // R
    val stickyBit = sig(sigWidth - 1, 0).orR // S: set if any of the rest bits are set
    val leastSigBitOfResult = sig(sigWidth + 2) // the least significant bit of the pre-rounded result

    // roundUp is true when GRS is 101, 110, 111 or when we have a tie (GRS = 100) and the number is odd
    val roundUp = guardBit & (roundBit | stickyBit | (!roundBit & !stickyBit & leastSigBitOfResult))
    //val preRoundSig = sig((sigWidth + 1)*2 - 1, sigWidth + 2)

    // The Mux function will select the preRoundSig + 1.U if roundUp is true, or preRoundSig otherwise.
    // When roundUp is not true, it means we should "round down", i.e., just take the number as it is, effectively truncating the extra bits

    //val rawOut_sig_reg = RegNext(Mux(roundUp, preRoundSig + 1.U, preRoundSig))

    val preRoundSig = Cat(0.U(1.W), sig((sigWidth + 1)*2 - 1, sigWidth + 2))

    val rawOut_sig = Mux(roundUp, preRoundSig + 1.U, preRoundSig)
    val rawOut_exp = Wire(UInt((expWidth).W))
    when (rawOut_sig(sigWidth) === 1.U(1.W)) {
      rawOut_exp := exp + 1.U
    }.otherwise {
      rawOut_exp := exp
    }

    val rawOut_sig_reg = RegNext(rawOut_sig(sigWidth - 1, 0), init = 0.U)
    val rawOut_exp_reg = RegNext(rawOut_exp, init = 0.U)

    io.rawOut.exp := rawOut_exp_reg
    io.rawOut.sig := rawOut_sig_reg
    }    
}
