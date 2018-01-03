# This script takes an fio run log as input and spits out a summary of important data points
# understand fio results more in depth - figure out why there's a stdev in each job's clat line
# TODO: Find appropriate latency metric and capture it

import argparse
import numpy
import re
import sys
import os.path

# reads the contents of a file into memory; one line <=> one list item. Returns the list
def read_file_into_list(fileName):
    if not os.path.isfile(fileName):
        raise IOError("Cannot find file %s" %fileName)
    else:
        strippedList = []
        with open(fileName) as f:
            fileContents = f.readlines()

        for line in fileContents:
            strippedList.append(line.rstrip("\n"))

    return strippedList

# takes a list of strings and returns a list of strings which match a given regular expression
def lines_matching_regex(contentsList, regex):

    matchingLines = []

    for line in contentsList:
        if re.search(regex, line) is not None:
            matchingLines.append(line)

    return matchingLines

# returns a list of values of param
def parameter_value(matchingLines, param):
    values = []

    for l in matchingLines:
        tempList = l.split()

        for item in tempList:
            if param in item:
                if param == "iops":
                    values.append(int(item.strip(param + "=").rstrip(',')))
                elif param == "bw":
                    tempString = item.strip(param + "=").rstrip(',')
                    if re.search("[0-9]B", tempString):
                        values.append(float(tempString.rstrip("B/s")))
                    elif re.search("[0-9]KB", tempString):
                        values.append(float(tempString.rstrip("KB/s"))*1024)
                elif param == "aggrb":
                    tempString = item.strip(param + "=").rstrip(',')
                    if re.search("[0-9]B", tempString):
                        return float(tempString.rstrip("B/s"))
                    elif re.search("[0-9]KB", tempString):
                        return float(tempString.rstrip("KB/s"))*1024

    return values

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, type=str, help="File containing a single column of numeric values")
    args = parser.parse_args()

    if len(sys.argv) < 2:
	parser.print_help()
	sys.exit(2)

    strippedList = read_file_into_list(args.file)
    readIOPSResult = lines_matching_regex(strippedList, r'read.*iops')
    writeIOPSResult = lines_matching_regex(strippedList, r'write.*iops')
    readBandwidthResult = lines_matching_regex(strippedList, r'read.*bw')
    writeBandwidthResult = lines_matching_regex(strippedList, r'write.*bw')
    aggrReadBandwidthResult = lines_matching_regex(strippedList, r'READ.*aggrb')
    aggrWriteBandwidthResult = lines_matching_regex(strippedList, r'WRITE.*aggrb')

    if readIOPSResult:
        readIOPS = parameter_value(readIOPSResult, "iops")
    if writeIOPSResult:
        writeIOPS = parameter_value(writeIOPSResult, "iops")
    if readBandwidthResult:
        readBandwidth = parameter_value(readBandwidthResult, "bw")
    if writeBandwidthResult:
        writeBandwidth = parameter_value(writeBandwidthResult, "bw")
    if aggrReadBandwidthResult:
        aggrReadBandwidth = parameter_value(aggrReadBandwidthResult, "aggrb")
    if aggrWriteBandwidthResult:
        aggrWriteBandwidth = parameter_value(aggrWriteBandwidthResult, "aggrb")

    if readIOPSResult and readBandwidthResult:
        print("Avg Read Bandwidth Per Job = %.2f MB/s, StDev = %.2f" % (numpy.mean(readBandwidth)/1024/1024, numpy.std(readBandwidth)/1024/1024))
        print("Avg Read IOPS = %.2f, StDev = %.2f" %(numpy.mean(readIOPS), numpy.std(readIOPS)))
        print("Aggregate Read Bandwidth for this fio run = %.2f MB/s" % float(aggrReadBandwidth/1024/1024))
    if writeIOPSResult and writeBandwidthResult:
        print("Avg Write Bandwidth Per Job = %.2f MB/s, StDev = %.2f" % (numpy.mean(writeBandwidth)/1024/1024, numpy.std(writeBandwidth)/1024/1024))
        print("Avg Write IOPS = %.2f, StDev = %.2f" % (numpy.mean(writeIOPS), numpy.std(writeIOPS)))
        print("Aggregate Write Bandwidth for this fio run = %.2f MB/s" % float(aggrWriteBandwidth/1024/1024))
