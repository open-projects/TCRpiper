#!/usr/bin/env python3

### D. Malko
### TCRpiper - a pipeline for treatment of TCR sequences
### All right reserved
### 2020

import os
import re
import glob
import argparse


MIGEC_PATH = './bin/migec/migec'
MIXCR_PATH = './bin/mixcr/mixcr'
VDJTOOLS_PATH = './bin/vdjtools/vdjtools'


def main():
    input_parser = argparse.ArgumentParser(description='TCRpiper: a pipeline for treatment of TCR sequences.')
    input_parser.add_argument('-i', metavar='/path/to/input_dir', default='.', help='the path to the input directory (the directory has to have a SampleInfo file)', required=False)
    input_parser.add_argument('-o', metavar='/path/to/output_dir', default='.', help='the path to the output directory', required=False)
    input_parser.add_argument('-l', metavar='/path/to/file_name.log', default=None, help='the log file', required=False)

    args = input_parser.parse_args()
    in_dir = re.sub(r'\/$', '', args.i)
    out_dir = re.sub(r'\/$', '', args.o)
    log_file = args.l

    enr = out_dir + '/ENR'
    qc = out_dir + '/runQC'

    log = ''
    try:
        log += '====================MIGEC====================\n'
        migec = Migec(in_dir, out_dir, MIGEC_PATH)
        log += '>>>CheckoutBatch<<<\n' + migec.CheckoutBatch()
        log += '>>>Histogram<<<\n' + migec.Histogram()
        log += '>>>AssembleBatch<<<\n' + migec.AssembleBatch()
    except Exception as error:
        log += '\nMIGEC error:\n{}'.format(error)
        exit('...error')

    try:
        log += '\n====================MIXCR====================\n'
        mixcr = Mixcr(in_dir, out_dir, MIXCR_PATH)
        log += mixcr.Analyze(migec.get_assemble_dir())
    except Exception as error:
        log += '\nMIXCR error:\n{}'.format(error)
        exit('...error')

    try:
        log += '\n====================VDJtools==================\n'
        vdjtools = VDJtools(out_dir, VDJTOOLS_PATH)
        log += '>>>Convert<<<\n' + vdjtools.Convert(mixcr.get_analize_dir())
        log += '>>>Filter<<<\n' + vdjtools.Filter()
    except Exception as error:
        log += '\nVDJtools error:\n{}'.format(error)
        exit('...error')

    if log_file:
        with open(log_file, "w") as lg:
            lg.write(log)

    print('...done')

# end of main()


class VDJtools:
    def __init__(self, outdir='.', prg_path=None):
        self._vdjtools = re.sub(r'/$', '', prg_path) if prg_path else 'vdjtools'
        self._outdir = re.sub(r'/$', '', outdir)
        self._vdj_dir = self._outdir + '/vdj'

    def Convert(self, dir_name):
        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/*clonotypes*.txt'):
            cmd = self._vdjtools + ' Convert -S mixcr {} {}/{}'.format(file_name, self._vdj_dir, 'vdj')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()
        return output

    def Filter(self, dir_name=None):
        dir_name = dir_name if dir_name else self._vdj_dir

        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/vdj.*clonotypes*.txt'):
            cmd = self._vdjtools + ' FilterNonFunctional {} {}/{}'.format(file_name, self._vdj_dir, 'nc')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()

        return output

    def get_vdj_dir(self):
        return self._vdj_dir

# end of class VDJtools


class Mixcr:
    def __init__(self, indir= '.', outdir='.', prg_path = None):
        self._mixcr = re.sub(r'/$', '', prg_path) if prg_path else 'mixcr'
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
            cmd = self._mixcr + ' analyze amplicon -s hsa --starting-material rna '
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


class Migec:
    def __init__(self, indir= '.', outdir='.', prg_path = None):
        self._migec = re.sub(r'/$', '', prg_path) if prg_path else 'migec'
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
        cmd = self._migec + ' CheckoutBatch -cute {} {}'.format(self._barcodes_file, self._checkout_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def Histogram(self, outdir='histogram'):
        cmd = self._migec + ' Histogram {} {}'.format(self._checkout_dir, self._histogram_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def AssembleBatch(self):
        cmd = self._migec + ' AssembleBatch  -c {} {} {}'.format(self._checkout_dir, self._histogram_dir, self._assemble_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def get_assemble_dir(self):
        return self._assemble_dir

# end of class Migec


if __name__ == '__main__':
    main()
