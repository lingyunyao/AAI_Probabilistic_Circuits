scalaVersion := "2.13.10"

libraryDependencies ++= Seq(
  "edu.berkeley.cs" %% "chisel3" % "3.5.5",
 // "edu.berkeley.cs" %% "chiseltest" % "0.6.0",
  "edu.berkeley.cs" %% "hardfloat"% "1.6.0-fcdfff6c7-SNAPSHOT",
  "edu.berkeley.cs" %% "chiseltest" % "0.5.1",
  "org.scalatest" %% "scalatest" % "3.2.9" % "test"
)

/*
resolvers ++= Seq(
  Resolver.sonatypeRepo("snapshots"),
  Resolver.sonatypeRepo("releases")
)
*/
resolvers ++= Resolver.sonatypeOssRepos("snapshots")

addCompilerPlugin("edu.berkeley.cs" % "chisel3-plugin" % "3.5.5" cross CrossVersion.full)
//addCompilerPlugin("edu.berkeley.cs" % "chisel3-plugin" % "3.5.5" cross CrossVersion.full)
//scalacOptions += "-Xplugin-require:chisel3"
scalacOptions ++= Seq(
  "-deprecation",
  "-encoding", "UTF-8",
  "-feature",
  "-unchecked",
  "-Xfatal-warnings",
  "-language:reflectiveCalls",
 // "-Ymacro-annotations",
  "-P:chiselplugin:genBundleElements" // Available since v3.5.1, to be made default in v3.6
)

 
