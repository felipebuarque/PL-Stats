import os, sys
import shutil

root_dir = '/home/felipe/Documentos/master/thesis/dev/SPLs/workspace/projects_java/'
dest_dir = '/home/felipe/Dropbox/master/papers/GPCE 2011/sheets/results/'
results_dir = '/_pl-stats/results/'

print ' '
print 'Copying files...'
print ' '

for project in os.listdir(root_dir):
	if os.path.isdir(root_dir + project):
		src_project = root_dir + project
		dst_project = dest_dir + project
		
		print project
		
		if not os.path.exists(dst_project):
			os.mkdir(dst_project)
	
	#	os.system('rm %s' % (src_project + results_dir + 'raffle.csv'))
	#	os.system('rm %s' % (src_project + results_dir + 'raffle1.csv'))
	#	os.system('rm %s' % (src_project + results_dir + 'raffle2.csv'))
	
		for file in os.listdir(src_project + results_dir):
			if file.__contains__('.csv'):
				shutil.copy(src_project + results_dir + file, dst_project)

print ' '
print 'Done.'
print ' '
