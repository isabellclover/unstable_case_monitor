// copy the output from all the triggered jobs by invoking the Copy Artifact plugin for the  
// builds that were triggered  
import hudson.plugins.copyartifact.*
import hudson.model.AbstractBuild
import hudson.Launcher
import hudson.model.BuildListener
import hudson.FilePath 
import jenkins.model.Jenkins

doWork()

def doWork() {
	//String jobPath = new File('config.ini').getText('UTF-8')
	jobPath = 'antimalware_feature_unit_test,NMS_develop_unit_test,NMS_develop_PSL_unit_test'
	println 'PathList :' + jobPath
	for (path in jobPath.split(",")){
		jobs = Jenkins.instance.getItemByFullName(path)
		if(jobs != null){
			jobs.each { j ->
			  if (j instanceof com.cloudbees.hudson.plugins.folder.Folder) { return }
			  println('JOB: ' + j.fullName)
			  numbuilds = j.builds.size()
			  if (numbuilds == 0) {
				println('  -> no build')
				return
			  }
			  j.builds.each{ b ->
				println(j.Name + " => "+ b.getNumber())
				copyTriggeredResults(j.Name , Integer.toString(b.getNumber()))
			  }
			  }			
		}
	}
}

def copyTriggeredResults(projName, buildNumber) {
   def reportPath = "TestReports"
   def selector = new SpecificBuildSelector(buildNumber)
   def targetPath = reportPath+ "/"+ projName + "/"+ buildNumber ;
   println(targetPath)
   
   // CopyArtifact(String projectName, String parameters, BuildSelector selector,
   // String filter, String target, boolean flatten, boolean optional)
   def copyArtifact = new CopyArtifact(projName, "", selector, "**/.xml", targetPath, false, true)

   // use reflection because direct call invokes deprecated method
   // perform(Build<?, ?> build, Launcher launcher, BuildListener listener)
   def perform = copyArtifact.class.getMethod("perform", AbstractBuild, Launcher, BuildListener)
   perform.invoke(copyArtifact, build, launcher, listener)
}

  
   
 
   
 