import chisel3._
import chiseltest._
import org.scalatest._
import org.scalatest.flatspec.AnyFlatSpec
import java.io.File
import chisel3.experimental.BundleLiterals._

import scala.util.Random

class AddRawFNWrapper(expWidth: Int, sigWidth: Int) extends chisel3.Module {
  val io = IO(new Bundle {
    val a = Input(new RawFloat(expWidth, sigWidth))
    val b = Input(new RawFloat(expWidth, sigWidth))
//    val invalidExc = Output(Bool())
    val rawOut = Output(new RawFloat(expWidth, sigWidth + 2))
    val resetDriver = Input(Bool())
    val asyncResetSignal = Input(AsyncReset())
  })

  val addRawFN = Module(new AddRawFN(expWidth, sigWidth))
  addRawFN.io.a := io.a
  addRawFN.io.b := io.b
  addRawFN.io.asyncResetSignal := io.resetDriver.asAsyncReset
//  io.invalidExc := addRawFN.io.invalidExc
  io.rawOut := addRawFN.io.rawOut
}

class AddRawFNTester extends AnyFlatSpec with ChiselScalatestTester {

  def randFloat(): Float = {
    val random = new Random()
    random.nextFloat() * 10000.0f

  }
  "MulRawFN" should "multiply two floating point numbers" in {
    val exp_width = 8
    val sig_width = 23
    test(new AddRawFNWrapper(exp_width, sig_width)).withAnnotations(Seq(WriteVcdAnnotation)) { dut =>

        //dut.io.asyncResetSignal.poke(true.B.asAsyncReset)  // Assert reset
        dut.io.resetDriver.poke(true.B)  // Assert reset
        dut.clock.step(1)
        //dut.io.asyncResetSignal.poke(false.B.asAsyncReset)  // De-assert reset
        dut.io.resetDriver.poke(false.B)  // De-assert reset
        dut.clock.step(1)

  for (i <- 0 until 200) {
      //val decimalNumber_1 = randFloat() 
      //val decimalNumber_2 = randFloat()
      val decimalNumber_1: Double = 0//9.865337129695835
      val decimalNumber_2: Double = 0.2790962998300388//8.879517657322083

      //val decimalNumber_1: Double = 1234.567
      val floatNumber_1: Float = decimalNumber_1.toFloat
      val floatBits_1: Int = java.lang.Float.floatToRawIntBits(floatNumber_1)
      val exponent_1 = (floatBits_1 >>> sig_width) & ((1 << exp_width) - 1) // 9 bits for exponent
      val significand_1 = floatBits_1 & ((1 << sig_width) - 1) // 23 bits for significand

      //val decimalNumber_2: Double = 1234.567
      val floatNumber_2: Float = decimalNumber_2.toFloat
      val floatBits_2: Int = java.lang.Float.floatToRawIntBits(floatNumber_2)

      val exponent_2 = (floatBits_2 >>> sig_width) & ((1 << exp_width) - 1) // 9 bits for exponent
      val significand_2 = floatBits_2 & ((1 << sig_width) - 1) // 23 bits for significand

      println(s"The first decimalNumber_1: $decimalNumber_1")
      println(s"The first Exponent: $exponent_1 , ${exponent_1.toBinaryString}")
      println(s"The first Significand: $significand_1, ${significand_1.toBinaryString}")      
      
      println(s"The second decimalNumber_2: $decimalNumber_2")
      println(s"The second Exponent: $exponent_2, ${exponent_2.toBinaryString}")
      println(s"The second Significand: $significand_2, ${significand_2.toBinaryString}")

//      dut.io.a.isNaN.poke(false.B)
//      dut.io.a.isInf.poke(false.B)
//      dut.io.a.isZero.poke(false.B)

     /*   dut.io.asyncResetSignal.poke(true.B.asAsyncReset)  // Assert reset
        dut.clock.step(1)
        dut.io.asyncResetSignal.poke(false.B.asAsyncReset)  // De-assert reset
        dut.clock.step(1)
*/
      dut.io.a.exp.poke(exponent_1.U)
      dut.io.a.sig.poke(significand_1.U)

//      dut.io.b.isNaN.poke(false.B)
//      dut.io.b.isInf.poke(false.B)
//      dut.io.b.isZero.poke(false.B)

      dut.io.b.exp.poke(exponent_2.U)
      dut.io.b.sig.poke(significand_2.U)

      dut.clock.step(1)


      // Generate VCD file
      val vcdFileName = "waveform.vcd"
      val vcdFile = new File(vcdFileName)
      dut.clock.setTimeout(0)
      dut.clock.step(10)

      val rawOut = dut.io.rawOut.peek()


      val bias = (1 << (exp_width - 1)) - 1
      val exponent_result = rawOut.exp.litValue.toInt - bias
      
      val significand_binary = rawOut.sig.litValue.bigInteger.toString(2)
      val significand_integer = BigInt(significand_binary, 2)
      val significand_result = 1 + (significand_integer.toDouble / (1 << sig_width))

      val decimalValue = significand_result * scala.math.pow(2, exponent_result)
      println(s"The result: $decimalValue")
      println(s"The result of decimalNumber_1 + decimalNumber_2: ${decimalNumber_1+decimalNumber_2}")
      println(s"The result Exponent: ${rawOut.exp.litValue.toInt}, ${java.lang.Long.toBinaryString(java.lang.Double.doubleToRawLongBits(scala.math.pow(2, exponent_result)))}")
      println(s"The result Significand: $significand_result, ${java.lang.Long.toBinaryString(java.lang.Double.doubleToRawLongBits(significand_result))}")
      println(s"The Error: ${decimalNumber_1+decimalNumber_2 - decimalValue}")
      println(s" ")
      
      assert(scala.math.abs(decimalValue - (decimalNumber_1+decimalNumber_2)) < 1)
  }
      
    }
  }
}

