## siRNA Design Pipeline
Collection of tools to retrieve siRNA (small interfering RNA) candidate sequences targeting your gene of interest from popular siRNA design tools, identify which candidates are suggested by multiple different software tools, and perform further quality checking and validation on identified candidates.

General notes:

- We are designing 21nt siRNA sequences (19nt + 2nt TT overhangs).
- There are 2 requirements the mRNA sequence you provide as input should satisfy: (a) needs to begin at start codon to ensure proper scoring of parameter 4 (for explanation see step 2), (b) needs to exclude introns which allows us to skip parameter 5 (for explanation see step 2)

### Step 1: Automate siRNA candidate discovery

In this step, we retrieve siRNA candidate sequences suggested by a variety of design algorithms and softwares. siRNA candidates which are suggested by multiple tools (>3) will be further analysed in step 2 based on a 20-parameter quality scoring system.

The folder 'software_comparisons' mainly consists of modules which enable webscraping of siRNA design websites.

The software tools included are:

1. ThermoFisher's BLOCK-iT RNAi Designer
2. RNA Wizard
3. siDirect
4. siDESIGN center
5. sFold
6. RNAi explorer
7. Oligowalk
8. SiRNA Design (IDT)
9. Eurofins_siMax

These modules are called in the main.py file, which further relies on the helper_functions.py script.

1. ThermoFisher's BLOCK-iT RNAi Designer

For our purposes, [this tool](https://rnaidesigner.thermofisher.com/rnaiexpress/) provides sequences which can then be ordered from ThermoFisher with additional chemical modifications they do not disclose; the product is named 'Stealth RNAi siRNA'. The algorithm this tool relies on is proprietary, and the only parameters we can manually set are species and G/C percentage (min & max). Note that we are here extracting information about the position on the mRNA that their siRNA would be targeting, however their product (the effectiveness of which they vouch for) is heavily chemically modified. It is designed to be suitable for in vitro and in vivo experiments; especially for the latter it is endowed with higher specificity, stability, and less cellular toxicity by suppressing the initiation of protein kinase R/interferon response pathway. However, they give no information about the nature and position of these modifications.

2. RNA Wizard

[RNA Wizard](http://www.sirnawizard.com/design_advanced.php) by Invivogen considers optimal internal stability of siRNAs, and excludes immunogenic sequences. However also here, we cannot choose the underlying algorithms and parameters.

3. siDirect

[SiDirect](http://sidirect2.rnai.jp/) is based on the algorithm by [Ui-Tei et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2602766/) by default. Ui-Tei et al. found that off-target effects are strongly related to thermodynamic properties of the siRNA seed region & target mRNA 3' UTR duplex. To obtain siRNA with reduced off-target effects, the melting temperature of the seed duplex should be <21.5°C. Users can also choose other algorithms ([Reynolds et al.](https://www.nature.com/articles/nbt936); [Amarzguioui et al.]) and various combinations of these algorithms. As a default, the siDirect module returns all candidates that are suggested by either Ui-Tei, Reynolds, or Amarzguoui, but this can easily be changed in the code to select e.g. only candidates which are suggested by all three.

4. siDESIGN center

The siDESIGN center by Dharmacon (which was acquired by Horizon Discovery) is based on the algorithms by [Elbashir et al.](https://www.sciencedirect.com/science/article/abs/pii/S1046202302000233?via%3Dihub) and [Reynolds et al](https://www.nature.com/articles/nbt936). If the nucleotide sequence is provided as input, the seed region specificity of siRNAs can be evaluated - this is relevant for estimating off-target effects. The exact matches of the seed region of siRNA to the 3' UTR of the genes are determined; the lower frequency of seed region in the target genome proves the specificity of siRNA.

5. sirna by sFold

[sirna](https://sfold.wadsworth.org/cgi-bin/sirna.pl) is a submodule of sfold [Ding et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC441587/), the software for statistical folding of nucleic acids and studies of regulatory RNAs. siRNA design is based on a combination of RNA target accessibility prediction, siRNA duplex thermodynamic properties and empirical design rules. Its approach to target accessibility evaluation is an original extension of the underlying RNA folding algorithm to account for the likely existence of a population of structures for the target mRNA [source](https://www.hsls.pitt.edu/obrc/index.php?page=URL1097777933).

6. RNAi Explorer

[RNAi Explorer software](http://www.genelink.com/sirna/RNAicustomorder.asp) by Gene Link Inc. includes parameters such as GC content and consecutive bases. This tool does not include different algorithms and parameters. The page seems to be faulty; it remains to be seen whether this defect is temporary. If the page stays down, RNAi Explorer will be excluded from this project.

7. Oligowalk

[Oligowalk](http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_form.cgi) was designed by Mathew's group at the University of Rochester Medical Center. It mainly selects functional siRNAs based on thermodynamic hybridization properties and the algorithm by [Reynolds et al](https://www.nature.com/articles/nbt936). This tool provides both comprehensive thermodynamic information, as well as an estimated probability of it being efficient siRNA. The results are sent per email, which takes several hours. The code is written so that the link which one receives per e-mail can be pasted into the console, upon which the results are analysed. A drawback of Oligowalk is that it has not been updated since 2008.

8. SiRNA Design (IDT)

[This tool](https://eu.idtdna.com/site/order/designtool/index/DSIRNA_CUSTOM) by Integrated DNA Technologies Inc. considers asymmetrical end stability, which is an important siRNA design parameter. Traditionally, siRNAs are around 21nt in length. IDT proposes using 27nt RNA duplexes, which are able to effectively target some sites that 21mers cannot silence. These DsiRNAs are processed by Dicer into 21mer siRNAs. Further background is provided [here](https://eu.idtdna.com/pages/education/decoded/article/rnai). For our purposes, we just extract the site they suggest targeting, but stick to our 21nt length.

9. Eurofins siMax

The [siRNA design tool](https://eurofinsgenomics.eu/en/ecom/tools/sirna-design/) by Eurofins Genomics allows you to specify which stretch of the coding region should be targeted (the whole sequence is the default), which problematic designs to exclude (>3G/Cs in a row, >A/Us in a row, U at 3' end, excluding all of these is set as default), min. and max. GC content (default: 30-53), and min. distance from start and stop codon (default in both cases: 100).

### Step 2

In this step we perform mostly automatic scoring of the suggested candidates that step 1 yields. The scoring is based on rational design parameters suggested by [Fakhr et al. (2016)](https://www.nature.com/articles/cgt20164.pdf). This will be particularly useful to justify or explain potential differences in efficacy that we might observe experimentally. Candidates suggested by step 1 and validated by step 2 should in theory have a high chance of working well.

What are the parameters, and what are their weights?
1. BLAST search of sense strand (1): this should be done **manually**
2. BLAST search of antisense strand (1): this should be done **manually**
3. Not located at SNP site (1): in the case of luciferase, this is not necessary; therefore this parameter is, for now, not implemented yet.
4. Not located in first 75 bases from start codon (1)
5. Not in the intron (1): We can exclude this parameter as our input sequence should already exclude introns.
6. GC content of 36-52% (1). Note: Amarzguioui et al. suggest 31.6-57.9, one could consider being a bit more tolerant with this parameter. The distribution of GCs probably matters more than total content.
7. Asymmetrical base pairing in the duplex (2): more A/U at 5' of antisense strand and more G/C at 5' of sense strand
8. Energy valley in the 9-14th nucleotide of the sense strand (2)
9. GC repeat less than 3 (0.5)
10. AT repeat less than 4 (0.5)
11. No internal secondary structures and hairpins (2): This needs to be checked **manually**, e.g. using the RNAfold web server
12. 3'-TT overhangs (1)
13. Weak base pair at 5'-end of antisense (1): presence of A/U
14. Strong base pair at 5'-end of sense (1): presence of G/C
15. Presence of A at 6th position of antisense strand (1)
16. Presence of A at 3rd position of sense strand (0.5)
17. Presence of A at 19th position of sense strand (0.5)
18. Absence of G/C at 19th position of sense strand (1)
19. Absence of G at 13th nucleotide of sense strand (1)
20. Presence of U at 10th nucleotide of sense strand (1)

### User inputs

Providing the mRNA target (plain nucleotides & [FASTA format](https://www.bioinformatics.nl/tools/crab_fasta.html)), target name, email. Still coming up: select species, GC content, algo combination for siDirect module.



