// copy the output from all the triggered jobs by invoking the Copy Artifact plugin for the  
// builds that were triggered  
import hudson.plugins.copyartifact.*
import hudson.model.AbstractBuild
import hudson.Launcher
import hudson.model.BuildListener
import hudson.FilePath 

def builders = [88,89,90]
def jobname = "clean-sweep_develop_tests_local"


for (subBuild in builders) {
  println(jobname + " => " + subBuild)
  copyTriggeredResults(jobname, Integer.toString(subBuild))
}

def copyTriggeredResults(projName, buildNumber) {
   def reportPath = "TestReports"
   def selector = new SpecificBuildSelector(buildNumber)
   def targetPath = reportPath+ "/"+ projName + "/"+ buildNumber ;
   println(targetPath)
   
   // CopyArtifact(String projectName, String parameters, BuildSelector selector,
   // String filter, String target, boolean flatten, boolean optional)
   def copyArtifact = new CopyArtifact(projName, "", selector, targetPath, null, false, true)

   // use reflection because direct call invokes deprecated method
   // perform(Build<?, ?> build, Launcher launcher, BuildListener listener)
   def perform = copyArtifact.class.getMethod("perform", AbstractBuild, Launcher, BuildListener)
   perform.invoke(copyArtifact, build, launcher, listener)
}

  
   
 
   
 