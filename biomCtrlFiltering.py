#!/usr/bin/python3
import argparse, csv, re
import logging as log

def main ():
	options = _set_options()
	_set_log_level(options.verbosity)

	exclud_indexes = _get_control_indexes(options.input,options.freq,options.ctrl_list)
	_print_biom(options.input,exclud_indexes,options.out)

def _print_biom (in_file, exclud_indexes, out):
	fh = open(in_file,mode='r')
	reader = csv.reader(fh,delimiter="\t")
	data = list(reader)
	fh.close()
	csv_file = csv.writer(open(out,mode='w'),delimiter="\t")
	for i in range(0,len(data)):
		if(i not in exclud_indexes):
			csv_file.writerow(data[i])

def _get_control_indexes (in_file,freq,ctrl_list):
	fh = open(in_file,mode='r')
	reader = csv.reader(fh,delimiter="\t")
	data = list(reader)
	fh.close()
	indexes = []
	for m in ctrl_list:
		indexes.append(data[1].index(m))
	sum_control=[0]*len(data)
	for i in range(2,len(data)-1):
		for j in indexes:
			sum_control[i] += float(data[i][j])
	total_ctrl = sum(sum_control)

	exclud_indexes=[]
	for i in range(2,len(sum_control)):
		percent = sum_control[i]/total_ctrl
		if(percent >  freq):
			exclud_indexes.append(i)
			log.debug('otu ' + data[i][0] + ' excluded ' + str(percent) + ' freq ' +  str(sum_control[i]) + ' absolute number ')
	log.debug(str(len(exclud_indexes)) + ' OTU line to be excluded.')
	return exclud_indexes


def _set_options ():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--i-otu-table',action='store',required=True,type=str,dest='input',help='Input table in biom tsv format.')
	parser.add_argument('-f','--min-frequency',action='store',default=0.1,type=float,dest='freq',help='Minimum control OTU frequency, for the OTU to be excluded.')
	parser.add_argument('-c','--ctrl-list',action='append',required=True,dest='ctrl_list',help='ID to be considered as control sample. Specify multiple \'-c\' options for multiple control sample.')
	parser.add_argument('-o','--out',help='The output file name',action='store',type=str,default='conta_filtered.tsv')
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
