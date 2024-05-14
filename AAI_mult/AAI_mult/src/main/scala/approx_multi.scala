import chisel3._
import chisel3.stage.{ChiselStage, ChiselGeneratorAnnotation}
import hardfloat._
import chisel3.util._

class RawFloat(expWidth: Int, sigWidth: Int) extends Bundle {
//  val isNaN = Bool()
//  val isInf = Bool()
//  val isZero = Bool()
  val exp = UInt((expWidth).W)
  val sig = UInt(sigWidth.W)
}



//----------------------------------------------------------------------------
//----------------------------------------------------------------------------
//class Approx_multi_RawFN(expWidth: Int, sigWidth: Int) extends RawModule
class Approx_multi_RawFN(expWidth: Int, sigWidth: Int) extends Module
{
    val io = IO(new Bundle {
        //val subOp = Input(Bool())
        val a = Input(new RawFloat(expWidth, sigWidth))
        val b = Input(new RawFloat(expWidth, sigWidth))
        val asyncResetSignal = Input(AsyncReset())
//        val invalidExc = Output(Bool())
        val rawOut = Output(new RawFloat(expWidth, sigWidth))
    })

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

    val bias = (1 << (expWidth - 1)) - 1
    val rawOut_exp = io.a.exp - bias.U + io.b.exp
    val rawOut_sig = (Cat(0.U(1.W), io.a.sig) + (Cat(0.U(1.W), io.b.sig)))(sigWidth, 0)

    val rawOut_exp_reg = RegNext(rawOut_exp, init = 0.U)
    val rawOut_sig_reg = RegNext(rawOut_sig, init = 0.U)

    when (notNaN_isZeroOut === 1.U) {
        io.rawOut.exp := 0.U
        io.rawOut.sig := 0.U
    } .elsewhen (rawOut_sig_reg(sigWidth) === 1.U) {
        io.rawOut.exp := rawOut_exp_reg + 1.U
        io.rawOut.sig := rawOut_sig_reg
    }.otherwise {
        io.rawOut.exp := rawOut_exp_reg
        io.rawOut.sig := rawOut_sig_reg(sigWidth - 1, 0)
    }
    }
//    io.rawOut.isNaN := io.a.isNaN || io.b.isNaN
//    io.rawOut.isInf := notNaN_isInfOut
//    io.rawOut.isZero := notNaN_isZeroOut
//    io.invalidExc := Utils.isSigNaNUnsignedRawFloat(io.a) || Utils.isSigNaNUnsignedRawFloat(io.b) || notSigNaN_invalidExc    
}

