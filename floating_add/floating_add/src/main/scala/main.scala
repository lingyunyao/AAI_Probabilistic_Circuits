import chisel3._
import chisel3.stage.{ChiselStage, ChiselGeneratorAnnotation}

object MyModuleMain extends App {
  val annos = Seq(ChiselGeneratorAnnotation(() => new AddRawFN(9,23)))
  (new ChiselStage).execute(args, annos)
}

object GenerateVerilog_AddRawFN extends App {
  println(ChiselStage.emitVerilog(new AddRawFN(9,23)))
}
object GenerateVerilog_AddFullRawFN extends App {
  println(ChiselStage.emitVerilog(new AddRawFN(9,23)))
}
