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
	jobPath = getJobNameFromEnv()	
	println 'PathList :' + jobPath
	if(jobPath == null){
		println 'ERROR! empty jobs'
		return
	}
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
			  topBuilds = getTopBuilds(j)
			  for(b in topBuilds){
				println(j.fullName + " => "+ b.number)
				copyTriggeredResults(j.fullName , Integer.toString(b.number))
				}
			  }			
		}
	}
}

def getTopBuilds(job){
	realCount = getBuildLimitFromEnv()
	//default value is 5
	if(realCount == null){
		realCount = 5
	}
	if(job.builds.size() <= realCount){
		realCount = job.builds.size()
	}
	return job.builds.limit(realCount)
}

def getJobNamesFromArg(){
	jobNames = ''
	for (a in this.args){
		jobNames = jobNames + a + ','
	}
	return jobNames
}

def getJobNameFromEnv(){
	return build.getEnvironment(listener).get('TARGET_LIST')
	//return System.getenv("TARGET_LIST")
}

def getBuildLimitFromEnv(){
	return build.getEnvironment(listener).get('BUILD_LIMIT')
}

def copyTriggeredResults(projName, buildNumber) {
   def reportPath = "TestReports"
   def selector = new SpecificBuildSelector(buildNumber)
   def targetPath = reportPath+ "/"+ projName + "/"+ buildNumber ;
   println(targetPath)
   
   // CopyArtifact(String projectName, String parameters, BuildSelector selector, String filter, String target, boolean flatten, boolean optional)
   def copyArtifact = new CopyArtifact(projName, "", selector, "**/TEST*.xml", targetPath, true, true)

   // use reflection because direct call invokes deprecated method
   // perform(Build<?, ?> build, Launcher launcher, BuildListener listener)
   def perform = copyArtifact.class.getMethod("perform", AbstractBuild, Launcher, BuildListener)
   perform.invoke(copyArtifact, build, launcher, listener)
}

  
   
 
   
 