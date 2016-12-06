// copy the output from all the triggered jobs by invoking the Copy Artifact plugin for the  
// builds that were triggered  
import hudson.plugins.copyartifact.*
import hudson.model.AbstractBuild
import hudson.Launcher
import hudson.model.BuildListener
import hudson.FilePath 

for (subBuild in build.builders) {
  println(subBuild.jobName + " => " + subBuild.buildNumber)
  copyTriggeredResults(subBuild.jobName, Integer.toString(subBuild.buildNumber))
}

def copyTriggeredResults(projName, buildNumber) {
   def selector = new SpecificBuildSelector(buildNumber)

   // CopyArtifact(String projectName, String parameters, BuildSelector selector,
   // String filter, String target, boolean flatten, boolean optional)
   def copyArtifact = new CopyArtifact(projName, "", selector, "**", null, false, true)

   // use reflection because direct call invokes deprecated method
   // perform(Build<?, ?> build, Launcher launcher, BuildListener listener)
   def perform = copyArtifact.class.getMethod("perform", AbstractBuild, Launcher, BuildListener)
   perform.invoke(copyArtifact, build, launcher, listener)
}

  
   
 
   
 