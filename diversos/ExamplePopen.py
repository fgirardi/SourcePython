import subprocess
import shlex

def cmd():

	p = subprocess.Popen(["ls -lat"],
			stdin = subprocess.PIPE, 
			stdout = subprocess.PIPE, 
			stderr = subprocess.PIPE,
			shell = True
			)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	p.communicate()
	print ("Return code: {0}".format(p.returncode))
	if p.returncode != 0:
		print 'Error executing command [%s]' % cmd 
		print 'stderr: [%s]' % stderr
		print 'stdout: [%s]' % stdout

	else:
		print("stdout: {0}".format(stdout))
		print("stderr: {0}".format(stderr))
cmd()
