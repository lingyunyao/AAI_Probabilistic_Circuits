import chisel3._
import chisel3.stage.{ChiselStage, ChiselGeneratorAnnotation}

object MyModuleMain extends App {
  val annos = Seq(ChiselGeneratorAnnotation(() => new MulRawFN(9,23)))
  (new ChiselStage).execute(args, annos)
}

object GenerateVerilog_MulRawFN extends App {
  println(ChiselStage.emitVerilog(new MulRawFN(9,23)))
}
object GenerateVerilog_MulFullRawFN extends App {
  println(ChiselStage.emitVerilog(new MulFullRawFN(9,23)))
}
