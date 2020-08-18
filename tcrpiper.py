#!/usr/bin/env python3

### D. Malko
### TCRpiper - a pipeline for treatment of TCR sequences
### All rights reserved
### 2020

import os
import re
import glob
import argparse

# It requires R packages: ggplot2, reshape

def main():
    input_parser = argparse.ArgumentParser(description='TCRpiper: a pipeline for treatment of TCR sequences.')
    input_parser.add_argument('-i', metavar='/path/to/input_dir', help='the path to the input directory (the directory has to have a SampleInfo file)', required=True)
    input_parser.add_argument('-o', metavar='/path/to/output_dir', default='.', help='the path to the output directory', required=False)
    input_parser.add_argument('-m', metavar='6G', default='6G', help='Xmx memory size', required=False)
    input_parser.add_argument('-f', metavar='threshold_value', default=0, help='force overseq threshold', required=False)
    input_parser.add_argument('-c', action='store_true', help='force collision filter', required=False )
    input_parser.add_argument('-b', metavar='/path/to/bin', default=None, help='the global path to a bin directory with the programs', required=False)
    input_parser.add_argument('-l', metavar='/path/to/file_name.log', default=None, help='the log file', required=False)

    args = input_parser.parse_args()
    in_dir = re.sub(r'\/$', '', args.i)
    out_dir = re.sub(r'\/$', '', args.o)
    xmx_size = args.m
    bin_path = args.b
    log_file = args.l
    overseq = args.f
    collisions = args.c

    enr = out_dir + '/ENR'
    qc = out_dir + '/runQC'

    Bin(bin_path)
    Xmx(xmx_size)

    log = Log(log_file)
    try:
        log.add('====================MIGEC====================\n')
        migec = Migec(in_dir, out_dir)
        log.add('>>>CheckoutBatch<<<\n' + migec.CheckoutBatch())
        log.add('>>>Histogram<<<\n' + migec.Histogram())
        log.add('>>>HistogramDrawing<<<\n' + migec.Draw())
        log.add('>>>AssembleBatch<<<\n' + migec.AssembleBatch(overseq, collisions))
    except Exception as error:
        log.add('\nMIGEC error:\n{}'.format(error))
        log.write()
        exit('...error')

    try:
        log.add('\n====================MIXCR====================\n')
        mixcr = Mixcr(in_dir, out_dir)
        log.add('>>>Analyze<<<\n' + mixcr.Analyze(migec.get_assemble_dir()))
    except Exception as error:
        log.add('\nMIXCR error:\n{}'.format(error))
        log.write()
        exit('...error')

    try:
        log.add('\n====================VDJtools==================\n')
        vdjtools = VDJtools(out_dir)
        log.add('>>>Convert<<<\n' + vdjtools.Convert(mixcr.get_analize_dir()))
        log.add('>>>Filter<<<\n' + vdjtools.Filter())
    except Exception as error:
        log.add('\nVDJtools error:\n{}'.format(error))
        exit('...error')

    log.add('\n...done')
    log.write()
    print('...done')

# end of main()


class SampleInfo:
    class Info:
        def __init__(self):
            self.sample_name = None
            self.chain = None
            self.barcode = None
            self.R1 = None
            self.R2 = None
            self.baseline = None
            self.subject_id = None
            self.antigen = None
            self.reads_exp = None

        def set(self, line):
            line = line.strip()
            fields = re.split(r'\t', line)
            if len(fields) == 9:
                (self.sample_name,
                 self.chain,
                 self.barcode,
                 self.R1, self.R2,
                 self.baseline,
                 self.subject_id,
                 self.antigen,
                 self.reads_exp
                 ) = [field.strip() for field in fields]
                return True
            return False
    # end of class Info()

    def __init__(self, file_name = None):
        self._file = file_name
        self._records = list()

    def find(self, dir_name):
        sample_info = None
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/*[Ss]ample*[Ii]nfo*'):
            if sample_info:
                raise Exception(
                    'It seems there are several SampleInfo files (it needs only one):\n1) {}\n2) {}\n'.format(
                        sample_info, file_name))
            else:
                sample_info = file_name
        self._file = sample_info

        return self._file

    def get_file(self):
        return self._file

    def get_records(self):
        return self._records

    def parse(self):
        if not self._file:
            raise Exception('No SampleInfo file in the directory: {}'.format(self._file))

        n_samples = 0
        with open(self._file, 'r') as file:
            for line in file:
                if re.search(r'\sR1\s+R2\s', line):
                    continue  # skip the file header

                inf = self.Info()
                if not inf.set(line):
                    raise Exception("Wrong record in SampleInfo file: {}\nline:{}".format(self._file, line))
                self._records.append(inf)
                n_samples += 1

        if n_samples == 0:
            raise Exception("Wrong format of SampleInfo file (no any samples): {}".format(self._file))

        return self._records

# end of class SampleInfo


class VDJtools:
    def __init__(self, outdir='.'):
        self._jar = Bin().get('vdjtools*.jar')[0]
        self._xmx = Xmx().get()
        self._outdir = re.sub(r'/$', '', outdir)
        self._vdj_dir = self._outdir + '/vdj'

    def Convert(self, dir_name):
        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/*clonotypes*.txt'):
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' Convert -S mixcr {} {}/{}'.format(file_name, self._vdj_dir, 'vdj')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()
        return output

    def Filter(self, dir_name=None):
        dir_name = dir_name if dir_name else self._vdj_dir

        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/vdj.*clonotypes*.txt'):
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' FilterNonFunctional {} {}/{}'.format(file_name, self._vdj_dir, 'nc')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()

        return output

    def get_vdj_dir(self):
        return self._vdj_dir

# end of class VDJtools


class Mixcr:
    def __init__(self, indir= '.', outdir='.'):
        self._jar = Bin().get('mixcr*.jar')[0]
        self._xmx = Xmx().get()
        self._indir = re.sub(r'/$', '', indir)
        self._outdir = re.sub(r'/$', '', outdir)
        self._analyze_dir = self._outdir + '/analyze'

    def Analyze(self, assemble_dir):
        assemble_dir = re.sub(r'/$', '', assemble_dir)
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        os.makedirs(self._analyze_dir, exist_ok=True)

        output = ''
        for record in info.parse():
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' analyze amplicon -s hsa --starting-material rna '
            cmd += '--5-end no-v-primers --3-end c-primers --adapters no-adapters --receptor-type {}'.format(record.chain)
            cmd += ' {}/{}_R1.*.fastq.gz'.format(assemble_dir, record.sample_name)
            cmd += ' {}/{}_R2.*.fastq.gz'.format(assemble_dir, record.sample_name)
            cmd += ' {}/{}'.format(self._analyze_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def get_analize_dir(self):
        return self._analyze_dir

# end of class Mixcr


class Migec:
    def __init__(self, indir= '.', outdir='.'):
        self._jar = Bin().get('migec*.jar')[0]
        self._xmx = Xmx().get()
        self._util = None
        self._indir = re.sub(r'/$', '', indir)
        self._outdir = re.sub(r'/$', '', outdir)
        self._checkout_dir = self._outdir  + '/checkout'
        self._histogram_dir = self._outdir + '/histogram'
        self._assemble_dir = self._outdir + '/assemble'
        self._barcodes_file = self._inspector()

    def _inspector(self):
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        barcodes = ''
        for record in info.parse():
            R1 = re.sub(r'.*/', '', record.R1)
            R1 = self._indir + '/' + R1
            R2 = re.sub(r'.*/', '', record.R2)
            R2 = self._indir + '/' + R2

            if record.barcode == '':
                raise Exception("No barcode in SampleInfo file: {}".format(info.get_file()))
            if not os.path.isfile(R1):
                raise Exception("Wrong R1 file name in SampleInfo file: {}".format(info.get_file()))
            if not os.path.isfile(R2):
                raise Exception("Wrong R2 file name in SampleInfo file: {}".format(info.get_file()))

            barcodes += '\t'.join((record.sample_name, record.barcode, '', R1, R2)) + '\n'

        barcodes_file = self._outdir + '/barcodes.csv'
        os.makedirs(self._outdir, exist_ok=True)

        try:
            with open(barcodes_file, 'w') as file:
                file.write(barcodes)
        except Exception:
            print("Can't create barcode file: {}".format(barcodes_file))

        return barcodes_file

    def CheckoutBatch(self):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' CheckoutBatch -cute {} {}'.format(self._barcodes_file, self._checkout_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def Histogram(self):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' Histogram {} {}'.format(self._checkout_dir, self._histogram_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def AssembleBatch(self, overseq=0, collisions=False):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' AssembleBatch'
        if overseq:
            cmd += ' --force-overseq {}'.format(overseq)
            if collisions:
                cmd += ' --force-collision-filter'
        cmd += ' -c {} {} {}'.format(self._checkout_dir, self._histogram_dir, self._assemble_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def get_assemble_dir(self):
        return self._assemble_dir

    def Draw(self):
        hist = Bin().get('histogram.R')[0]
        cmd = 'cd {}; Rscript {}'.format(self._histogram_dir, hist)
        stream = os.popen(cmd)
        output = stream.read()

        return output

# end of class Migec


class Bin:
    def __new__(cls, bin=None):
        if not hasattr(cls, 'instance'):
            if bin:
                cls._bin = re.sub(r'/$', '', bin)
            else:
                real_path = os.path.dirname(os.path.realpath(__file__))
                cls._bin = re.sub(r'/$', '', real_path) + '/bin'
            cls.instance = super(Bin, cls).__new__(cls)

        return cls.instance

    def get(self, file_name):
        path = self._bin + '/**/' + re.sub(r'^/', '', file_name)

        return glob.glob(path, recursive=True)

# end of Bin class (Singleton)


class Xmx:
    def __new__(cls, mem='8G'):
        if not re.search(r'^\d+[GM]$', mem):
            raise Exception("Wrong value of memory usage limit: {} (default value is '8G')".format(mem))
        if not hasattr(cls, 'instance'):
            cls._mem = mem
            cls.instance = super(Xmx, cls).__new__(cls)

        return cls.instance

    def get(self):
        xmx = '-Xmx' + self._mem

        return xmx

# end of Xmx class (Singleton)

class Log:
    def __init__(self, log_file=None):
        self._file_name = log_file
        self._log = ''

    def add(self, string):
        self._log += string if re.search(r'\n$', string) else string + "\n"

    def write(self):
        if self._file_name:
            with open(self._file_name, "w") as lg:
                lg.write(self._log)

# end of Log class


if __name__ == '__main__':
    main()
