#!/usr/bin/env python 

#'''FUNCTION & USAGE'''

import os
import argparse
from collections import defaultdict
from itertools import combinations

__description__ = ""
__author__ = "Malvika Sharan <malvika.sharan@uni-wuerzburg.de>"
__email__ = "malvika.sharan@uni-wuerzburg.de"
__version__ = ""

def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("inpath")
    parser.add_argument("outpath")
    parser.add_argument("sample_count")
    parser.add_argument("seed_threshold")
    args = parser.parse_args()
    
    seed_based_cluster_comparison = SeedBasedClusterComparison(
        args.inpath, args.outpath, args.sample_count, args.seed_threshold)
    if int(args.sample_count) == 2:
        seed_based_cluster_comparison.compare_two_samples()
    elif int(args.sample_count) == 3:
        seed_based_cluster_comparison.compare_three_samples()
    elif int(args.sample_count) == 4:
        seed_based_cluster_comparison.compare_four_samples()
    else:
        print("please provide total sample count to be compared.")
    
class SeedBasedClusterComparison(object):
    '''Filter the RPS blast result'''
    def __init__(self, inpath,
                 outpath, sample_count,
                 seed_threshold):
        self._inpath = inpath
        self._outpath = outpath
        self._sample_count = sample_count
        self._seed_threshold = seed_threshold
        
    def compare_two_samples(self):
        ''''''
        for folders in combinations(os.listdir(self._inpath), 2):
            for files1 in os.listdir(self._inpath+'/'+folders[0]):
                mir_dict1 = self._compile_mir_comparison(
                    self._inpath+'/'+folders[0]+'/'+files1)
                for files2 in os.listdir(self._inpath+'/'+folders[1]):
                    mir_dict2 = self._compile_mir_comparison(
                        self._inpath+'/'+folders[1]+'/'+files2)
                    outfile = (
                        self._outpath+'/'+folders[0]+'_'+files1.split('.')[0]
                        +'_COMP_'+folders[1]+'_'+files2).replace('seed_cluster_', '')
                    header = '\t'.join(['Libraries', 
                        folders[0]+':TotalMirs', folders[0]+':miR&log2FC',
                        folders[1]+':TotalMirs', folders[1]+':miR&log2FC'])
                    self._create_two_samples_outfile(outfile, header,
                                 mir_dict1, mir_dict2)
                    
    def compare_three_samples(self):
        ''''''
        for folders in combinations(os.listdir(self._inpath), 3):
            for files1 in os.listdir(self._inpath+'/'+folders[0]):
                mir_dict1 = self._compile_mir_comparison(
                    self._inpath+'/'+folders[0]+'/'+files1)
                for files2 in os.listdir(self._inpath+'/'+folders[1]):
                    mir_dict2 = self._compile_mir_comparison(
                        self._inpath+'/'+folders[1]+'/'+files2)
                    for files3 in os.listdir(self._inpath+'/'+folders[2]):
                        mir_dict3 = self._compile_mir_comparison(
                            self._inpath+'/'+folders[2]+'/'+files3)
                        outfile = (
                            self._outpath+'/'+folders[0]+'_'+files1.split('.')[0]
                            +'_COMP_'+folders[1]+'_'+files2.split('.')[0]
                            +'_COMP_'+folders[2]+'_'+files3).replace('seed_cluster_', '')
                        header = '\t'.join(['Libraries',
                            folders[0]+':TotalMirs', folders[0]+':miR&log2FC',
                            folders[1]+':TotalMirs', folders[1]+':miR&log2FC',
                            folders[2]+':TotalMirs', folders[2]+':miR&log2FC'])
                        self._create_three_samples_outfile(outfile, header,
                                     mir_dict1, mir_dict2, mir_dict3)
                        
    def compare_four_samples(self):
        ''''''
        for folders in combinations(os.listdir(self._inpath), 4):
            for files1 in os.listdir(self._inpath+'/'+folders[0]):
                mir_dict1 = self._compile_mir_comparison(
                    self._inpath+'/'+folders[0]+'/'+files1)
                for files2 in os.listdir(self._inpath+'/'+folders[1]):
                    mir_dict2 = self._compile_mir_comparison(
                        self._inpath+'/'+folders[1]+'/'+files2)
                    for files3 in os.listdir(self._inpath+'/'+folders[2]):
                        mir_dict3 = self._compile_mir_comparison(
                            self._inpath+'/'+folders[2]+'/'+files3)
                        for files4 in os.listdir(self._inpath+'/'+folders[3]):
                            mir_dict4 = self._compile_mir_comparison(
                                self._inpath+'/'+folders[3]+'/'+files4)
                            outfile = (
                                self._outpath+'/'+folders[0]+'_'+files1.split('.')[0]
                                +'_COMP_'+folders[1]+'_'+files2.split('.')[0]
                                +'_COMP_'+folders[2]+'_'+files3.split('.')[0]
                                +'_COMP_'+folders[3]+'_'+files4).replace('seed_cluster_', '')
                            header = '\t'.join(['Libraries',
                                folders[0]+':TotalMirs', folders[0]+':miR&log2FC',
                                folders[1]+':TotalMirs', folders[1]+':miR&log2FC',
                                folders[2]+':TotalMirs', folders[2]+':miR&log2FC',
                                folders[3]+':TotalMirs', folders[3]+':miR&log2FC'])
                            self._create_four_samples_outfile(outfile, header,
                                         mir_dict1, mir_dict2, mir_dict3, mir_dict4)
    
    def _compile_mir_comparison(self, infile):
        ''''''
        comparison_dict = {}
        with open(infile, 'r') as in_fh:
            for entry in in_fh:
                if not 'Libraries' in entry:
                    annotation = entry.split('\t')[0]
                    print(float(entry.split('\t')[3]))
                    if float(entry.split('\t')[3]) >= float(self._seed_threshold) or float(
                        entry.split('\t')[3]) <= float(self._seed_threshold)*-1:
                        total_log2fc = "%s:%.3f" % (
                            entry.split('\t')[2],
                            float(entry.split('\t')[3]))
                        comparison_dict.setdefault(annotation, []).append(total_log2fc)
        return comparison_dict
    
    def _create_two_samples_outfile(self, outfile, header,
                        gene_dict1, gene_dict2):
        ''''''
        common_gene_set = set(gene_dict1.keys()
                             ).intersection(set(gene_dict2))
        if len(list(common_gene_set)) > 0:
            with open(outfile, 'w') as out_fh:
                out_fh.write(header+'\n')
                for genes in common_gene_set:
                    if len(gene_dict1[genes]) > 1:
                        gene_list1 = ' | '.join(gene_dict1[genes])
                    else:
                        gene_list1 = gene_dict1[genes][0]
                    if gene_dict2[genes] > 1:
                        gene_list2 = ' | '.join(gene_dict2[genes])
                    else:
                        gene_list2 = gene_dict2[genes][0]
                    out_fh.write('%s\t%s\t%s\t%s\t%s\n' % (
                        genes, len(gene_dict1[genes]), gene_list1,
                        len(gene_dict2[genes]), gene_list2))
        
    def _create_three_samples_outfile(self, outfile, header,
                        gene_dict1, gene_dict2, gene_dict3):
        ''''''
        common_gene_set = set(gene_dict1.keys()
                             ).intersection(set(gene_dict2)
                            ).intersection(set(gene_dict3))
        if len(list(common_gene_set)) > 0:
            with open(outfile, 'w') as out_fh:
                out_fh.write(header+'\n')
                for genes in common_gene_set:    
                    if len(gene_dict1[genes]) > 1:
                        gene_list1 = ' | '.join(gene_dict1[genes])
                    else:
                        gene_list1 = gene_dict1[genes][0]
                    if gene_dict2[genes] > 1:
                        gene_list2 = ' | '.join(gene_dict2[genes])
                    else:
                        gene_list2 = gene_dict2[genes][0]
                    if gene_dict3[genes] > 1:
                        gene_list3 = ' | '.join(gene_dict3[genes])
                    else:
                        gene_list3 = gene_dict3[genes][0]
                    out_fh.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                        genes, len(gene_dict1[genes]), gene_list1,
                        len(gene_dict2[genes]), gene_list2,
                        len(gene_dict3[genes]), gene_list3))
                
    def _create_four_samples_outfile(self, outfile, header,
                        gene_dict1, gene_dict2, gene_dict3, gene_dict4):
        ''''''
        common_gene_set = set(gene_dict1.keys()
                            ).intersection(set(gene_dict2)
                            ).intersection(set(gene_dict3)
                            ).intersection(set(gene_dict4))
        if len(list(common_gene_set)) > 0:
            #print(list(common_gene_set))
            with open(outfile, 'w') as out_fh:
                out_fh.write(header+'\n')
                for genes in common_gene_set:
                    if len(gene_dict1[genes]) > 1:
                        gene_list1 = ' | '.join(gene_dict1[genes])
                    else:
                        gene_list1 = gene_dict1[genes][0]
                    if gene_dict2[genes] > 1:
                        gene_list2 = ' | '.join(gene_dict2[genes])
                    else:
                        gene_list2 = gene_dict2[genes][0]
                    if gene_dict3[genes] > 1:
                        gene_list3 = ' | '.join(gene_dict3[genes])
                    else:
                        gene_list3 = gene_dict3[genes][0]
                    if gene_dict4[genes] > 1:
                        gene_list4 = ' | '.join(gene_dict4[genes])
                    else:
                        gene_list4 = gene_dict4[genes][0]
                    out_fh.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                        genes, len(gene_dict1[genes]), gene_list1,
                        len(gene_dict2[genes]), gene_list2,
                        len(gene_dict3[genes]), gene_list3,
                        len(gene_dict4[genes]), gene_list4))
        
if __name__ == '__main__':
    main()
