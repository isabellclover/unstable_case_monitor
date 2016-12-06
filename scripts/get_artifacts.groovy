// copy the output from all the triggered jobs by invoking the Copy Artifact plugin for the  
 // builds that were triggered  
 // Assumptions: test output is in test-output folder, output and report files are  
 // named output.xml and report.html  
 import hudson.plugins.copyartifact.SpecificBuildSelector  
 import hudson.plugins.copyartifact.CopyArtifact  
 import hudson.model.AbstractBuild  
 import hudson.Launcher  
 import hudson.model.BuildListener  
 import hudson.FilePath  
   
 def envVars= build.getEnvironment()  
 def projs = envVars.get("PROJS")  
   
 projs.split(",").each {  
   println "Fetching output from " + it + "..."  
   copyTriggeredResults(it)  
 }  
   
 def copyTriggeredResults(projName) {  
   def buildNbr = build.getEnvironment().get("TRIGGERED_BUILD_NUMBER_" + projName)  
   def selector = new SpecificBuildSelector(buildNbr)  
   
   // CopyArtifact(String projectName, String parameters, BuildSelector selector,  
   // String filter, String target, boolean flatten, boolean optional)  
   def copyArtifact = new CopyArtifact(projName, selector, "**/*.*", null, false, false)  
   
   // use reflection because direct call invokes deprecated method  
   // perform(Build<?, ?> build, Launcher launcher, BuildListener listener)  
   def perform = copyArtifact.class.getMethod("perform", AbstractBuild, Launcher, BuildListener)  
   perform.invoke(copyArtifact, build, launcher, listener)  
   
   // rename test output to be output_${project name}.xml  
   def target = new FilePath(build.workspace, "test-output/output_" + projName + ".xml")  
   def source = new FilePath(build.workspace, "test-output/output.xml")  
   source.renameTo(target)  
 }