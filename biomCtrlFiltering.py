#!/usr/bin/python3
import argparse, csv, sys
import logging as log

def main ():
	options = _set_options()
	_set_log_level(options.verbosity)

	exclud_indexes, ctrl_indexes = _get_control_indexes(options)

	_print_biom(options.input,exclud_indexes,ctrl_indexes)

def _print_biom (in_file, exclud_indexes, ctrl_indexes):
	fh = open(in_file,mode='r')
	reader = csv.reader(fh,delimiter="\t")
	data = list(reader)
	fh.close()
	csv_w_ctrl = csv.writer(open('conta_filtered_w_ctrl.tsv',mode='w'),delimiter="\t")
	csv_wo_ctrl = csv.writer(open('conta_filtered_wo_ctrl.tsv',mode='w'),delimiter="\t")
	for i in range(0,len(data)):
		if(i not in exclud_indexes):
			csv_w_ctrl.writerow(data[i])
			if(i > 0):
				row_i=[]
				for j in range(0,len(data[i])):
					if j not in ctrl_indexes:
						row_i.append(data[i][j])
				csv_wo_ctrl.writerow(row_i)
			else:
				csv_wo_ctrl.writerow(data[i])


def _get_control_indexes (options):
	fh = open(options.input,mode='r')
	reader = csv.reader(fh,delimiter="\t")
	data = list(reader)
	fh.close()
	ctrl_indexes = []
	for m in options.ctrl_list:
		ctrl_indexes.append(data[1].index(m))
	sum_control=[0]*len(ctrl_indexes)

	for i in range(2,len(data)):
		for j in range(0,len(ctrl_indexes)):
			sum_control[j] += float( data[i][ctrl_indexes[j]] )
	exclud_indexes=[]
	if(options.freq != 0):
		for i in range(2,len(data)):
			for j in range(0,len(ctrl_indexes)):
				percent = float(data[i][indexes[j]])/sum_control[j]
				if(percent >  options.freq):
					if i not in exclud_indexes:
						exclud_indexes.append(i)
						log.debug('otu ' + data[i][0] + ' excluded ' + str(percent) + ' freq ' +  str(data[i][ctrl_indexes[j]]) + ' absolute number ')
	elif(options.num != 0):
		for i in range(2,len(data)):
			for j in range(0,len(ctrl_indexes)):
				if(float(data[i][ctrl_indexes[j]]) > options.num):
					if i not in exclud_indexes:
						exclud_indexes.append(i)
						log.debug('otu ' + data[i][0] + ' excluded ' +  str(data[i][ctrl_indexes[j]]) + ' absolute number ')
	log.debug(str(len(exclud_indexes)) + ' OTU line to be excluded.')
	return exclud_indexes, ctrl_indexes


def _set_options ():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--i-otu-table',action='store',required=True,type=str,dest='input',help='Input table in biom tsv format.')
	parser.add_argument('-f','--min-frequency',action='store',default=0,type=float,dest='freq',help='Minimum control OTU frequency, for the OTU to be excluded.')
	parser.add_argument('-n','--min-number',action='store',default=0,type=float,dest='num',help='Minimum control OTU number for the OTU to be excluded.')
	parser.add_argument('-c','--ctrl-list',action='append',required=True,dest='ctrl_list',help='ID to be considered as control sample. Specify multiple \'-c\' options for multiple control sample.')
	parser.add_argument('-v','--verbosity',help='Verbose level', action='store',type=int,choices=[1,3],default=1,dest='verbosity')
	args = parser.parse_args()
	return args

def _set_log_level(verbosity):
	if verbosity == 1:
		log_format = '%(asctime)s %(levelname)-8s %(message)s'
		log.basicConfig(level=log.INFO,format=log_format)
	elif verbosity == 3:
		log_format = '%(filename)s:%(lineno)s - %(asctime)s %(levelname)-8s %(message)s'
		log.basicConfig(level=log.DEBUG,format=log_format)


if __name__ == "__main__":
	main()
