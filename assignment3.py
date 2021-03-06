#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Christian Jansen'


##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"

    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    
        #print("TODO")
                
        ##
        ## Example loop
        ##
        
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')
        
        ## TODO now do something with the 'annotation_result'

        ##
        ## End example code
        ##
        annotation_result_dict = json.loads(annotation_result)
        #for i,line in enumerate(annotation_result_dict):
            #print(line)
            #if i > 10:
            #    break
            #if 'notfound' not in line.keys():
            #    print(line)


        #for index, line in enumerate(annotation_result):
        #    print("line ", index,": ",line)
        #    if index > 50:
        #        break

        return annotation_result_dict
    
    
    def get_list_of_genes(self, annot_dict):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        genenames = set([])
        for item in annot_dict:
            if 'notfound' not in item.keys():
                if 'dbnsfp' in item:
                    if 'genename' in item['dbnsfp']:
                        genenames.add(item['dbnsfp']['genename'])
                if 'snpeff' in item:
                    for annot in item['snpeff']['ann']:
                        if isinstance(annot, dict):
                            genenames.add(annot['genename'])
                if 'cadd' in item:
                    if 'gene' in item['cadd']:
                        for annot in item['cadd']['gene']:
                            if 'genename' in annot:
                                if isinstance(annot, dict):
                                    genenames.add(annot['genename'])

        return genenames
    
    
    def get_num_variants_modifier(self, annot_dict):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''
        var_modified = 0
        for item in annot_dict:
            if 'snpeff' in item:
                for annot in item['snpeff']['ann']:
                    if isinstance(annot, dict):
                        if annot['putative_impact'] == 'MODIFIER':
                            var_modified += 1
                            break
        return var_modified
        
    
    def get_num_variants_with_mutationtaster_annotation(self,annot_dict):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''
        mut_tast = 0
        for item in annot_dict:
            if 'dbnsfp' in item:
                if 'mutationstaster' in item['dbnsfp']:
                    mut_tast += 1
        return mut_tast

        
    
    def get_num_variants_non_synonymous(self,annot_dict):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''
        not_syn = 0
        for item in annot_dict:
            if 'cadd' in item:
                if item['cadd']['consequence'] == 'NON_SYNONYMOUS':
                    not_syn += 1
        return not_syn
        
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("URL for vcf in ibio: https://vcf.iobio.io/?species=Human&build=GRCh38")
            
    
    def print_summary(self):
        annotation = self.annotate_vcf_file()
        print("Gene List: ", self.get_list_of_genes(annotation))
        print("Number of variant MODIFIER: ",self.get_num_variants_modifier(annotation))
        print("Mutationstaster annotation: ", self.get_num_variants_with_mutationtaster_annotation(annotation))
        print("Number of non synonymous variants: ", self.get_num_variants_non_synonymous(annotation))
        self.view_vcf_in_browser()
        #print("Print all results here")
    
    
def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



