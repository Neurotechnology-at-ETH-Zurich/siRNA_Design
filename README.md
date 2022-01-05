## siRNA Design Pipeline
Collection of tools to retrieve siRNA (small interfering RNA) candidate sequences targeting your gene of interest from popular siRNA design tools, identify which candidates are suggested by multiple different software tools, and perform further quality checking and validation on identified candidates.

## Table of Content:
- [General notes on usage](#notes)
- [Step 1: Automate siRNA candidate discovery](#step1)
  - [ThermoFisher's BLOCK-iT RNAi Designer](#thermo)
  - [RNA Wizard](#rnawiz)
  - [siDirect](#sidirect)
  - [siDESIGN center](#sidesign)
  - [sFold](#sfold)
  - [RNAi explorer](#rnaiexplorer)
  - [Oligowalk](#oligowalk)
  - [SiRNA Design (IDT)](#idt)
  - [Eurofins_siMax](#eurofins)
- [Step 2: Scoring quality of siRNA candidates based on design parameters](#step2)
  - [Parameters](#parameters)
  - [User inputs](#userinputs)
- [Step 3: BLAST search to avoid off-target effects](#blast)
  - [Using the NCBI Blast tool](#ncbi)
  - [Understanding BLAST output](#results)
  - [Evaluating BLAST results](#evaluate)

<a name="notes"></a>
**General notes on usage**:
- We are designing 21nt siRNA sequences (19nt + 2nt TT overhangs).
- There are 2 requirements which the mRNA sequence you provide as input should satisfy; the need for these will become clear in step 2, where the individual scoring parameters are explained. (a) needs to begin at start codon to ensure proper scoring of parameter 4; (b) needs to exclude introns which allows us to skip parameter 5.

<a name="step1"></a>
### Step 1: Automate siRNA candidate discovery

In this step, we retrieve siRNA candidate sequences suggested by a variety of design algorithms and softwares. siRNA candidates which are suggested by multiple tools (>3) will be further analysed in step 2 based on a 20-parameter quality scoring system.

The folder 'software_comparisons' mainly consists of modules which enable webscraping of siRNA design websites.

The software tools included are:

1. [ThermoFisher's BLOCK-iT RNAi Designer](#thermo)
2. [RNA Wizard](#rnawiz)
3. [siDirect](#sidirect)
4. [siDESIGN center](#sidesign)
5. [sFold](#sfold)
6. [RNAi explorer](#rnaiexplorer)
7. [Oligowalk](#oligowalk)
8. [SiRNA Design (IDT)](#idt)
9. [Eurofins_siMax](#eurofins)

These modules are called in the main.py file, which further relies on the helper_functions.py script.

<a name="thermo"></a>
1. ThermoFisher's BLOCK-iT RNAi Designer

For our purposes, [this tool](https://rnaidesigner.thermofisher.com/rnaiexpress/) provides sequences which can then be ordered from ThermoFisher with additional chemical modifications they do not disclose; the product is named 'Stealth RNAi siRNA'. The algorithm this tool relies on is proprietary, and the only parameters we can manually set are species and G/C percentage (min & max). Note that we are here extracting information about the position on the mRNA that their siRNA would be targeting, however their product (the effectiveness of which they vouch for) is heavily chemically modified. It is designed to be suitable for in vitro and in vivo experiments; especially for the latter it is endowed with higher specificity, stability, and less cellular toxicity by suppressing the initiation of protein kinase R/interferon response pathway. However, they give no information about the nature and position of these modifications.

<a name="rnawiz"></a>
2. RNA Wizard

[RNA Wizard](http://www.sirnawizard.com/design_advanced.php) by Invivogen considers optimal internal stability of siRNAs, and excludes immunogenic sequences. However also here, we cannot choose the underlying algorithms and parameters.

<a name="sidirect"></a>
3. siDirect

[SiDirect](http://sidirect2.rnai.jp/) is based on the algorithm by [Ui-Tei et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2602766/) by default. Ui-Tei et al. found that off-target effects are strongly related to thermodynamic properties of the siRNA seed region & target mRNA 3' UTR duplex. To obtain siRNA with reduced off-target effects, the melting temperature of the seed duplex should be <21.5°C. Users can also choose other algorithms ([Reynolds et al.](https://www.nature.com/articles/nbt936); [Amarzguioui et al.]) and various combinations of these algorithms. As a default, the siDirect module returns all candidates that are suggested by either Ui-Tei, Reynolds, or Amarzguoui, but this can easily be changed in the code to select e.g. only candidates which are suggested by all three.

<a name="sidesign"></a>
4. siDESIGN center

The siDESIGN center by Dharmacon (which was acquired by Horizon Discovery) is based on the algorithms by [Elbashir et al.](https://www.sciencedirect.com/science/article/abs/pii/S1046202302000233?via%3Dihub) and [Reynolds et al](https://www.nature.com/articles/nbt936). If the nucleotide sequence is provided as input, the seed region specificity of siRNAs can be evaluated - this is relevant for estimating off-target effects. The exact matches of the seed region of siRNA to the 3' UTR of the genes are determined; the lower frequency of seed region in the target genome proves the specificity of siRNA.

<a name="sfold"></a>
5. sirna by sFold

[sirna](https://sfold.wadsworth.org/cgi-bin/sirna.pl) is a submodule of sfold [Ding et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC441587/), the software for statistical folding of nucleic acids and studies of regulatory RNAs. siRNA design is based on a combination of RNA target accessibility prediction, siRNA duplex thermodynamic properties and empirical design rules. Its approach to target accessibility evaluation is an original extension of the underlying RNA folding algorithm to account for the likely existence of a population of structures for the target mRNA [source](https://www.hsls.pitt.edu/obrc/index.php?page=URL1097777933).

<a name="rnaiexplorer"></a>
6. RNAi Explorer

[RNAi Explorer software](http://www.genelink.com/sirna/RNAicustomorder.asp) by Gene Link Inc. includes parameters such as GC content and consecutive bases. This tool does not include different algorithms and parameters. The page seems to be faulty; it remains to be seen whether this defect is temporary. If the page stays down, RNAi Explorer will be excluded from this project.

<a name="oligowalk"></a>
7. Oligowalk

[Oligowalk](http://rna.urmc.rochester.edu/cgi-bin/server_exe/oligowalk/oligowalk_form.cgi) was designed by Mathew's group at the University of Rochester Medical Center. It mainly selects functional siRNAs based on thermodynamic hybridization properties and the algorithm by [Reynolds et al](https://www.nature.com/articles/nbt936). This tool provides both comprehensive thermodynamic information, as well as an estimated probability of it being efficient siRNA. The results are sent per email, which takes several hours. The code is written so that the link which one receives per e-mail can be pasted into the console, upon which the results are analysed. A drawback of Oligowalk is that it has not been updated since 2008.

<a name="idt"></a>
8. SiRNA Design (IDT)

[This tool](https://eu.idtdna.com/site/order/designtool/index/DSIRNA_CUSTOM) by Integrated DNA Technologies Inc. considers asymmetrical end stability, which is an important siRNA design parameter. Traditionally, siRNAs are around 21nt in length. IDT proposes using 27nt RNA duplexes, which are able to effectively target some sites that 21mers cannot silence. These DsiRNAs are processed by Dicer into 21mer siRNAs. Further background is provided [here](https://eu.idtdna.com/pages/education/decoded/article/rnai). For our purposes, we just extract the site they suggest targeting, but stick to our 21nt length.

<a name="eurofins"></a>
9. Eurofins siMax

The [siRNA design tool](https://eurofinsgenomics.eu/en/ecom/tools/sirna-design/) by Eurofins Genomics allows you to specify which stretch of the coding region should be targeted (the whole sequence is the default), which problematic designs to exclude (>3G/Cs in a row, >A/Us in a row, U at 3' end, excluding all of these is set as default), min. and max. GC content (default: 30-53), and min. distance from start and stop codon (default in both cases: 100).

<a name="step2"></a>
### Step 2: Scoring quality of siRNA candidates based on design parameters

In this step we perform mostly automatic scoring of the suggested candidates that step 1 yields. The scoring is based on rational design parameters suggested by [Fakhr et al. (2016)](https://www.nature.com/articles/cgt20164.pdf). This will be particularly useful to justify or explain potential differences in efficacy that we might observe experimentally. Candidates suggested by step 1 and validated by step 2 should in theory have a high chance of working well.

<a name="parameters"></a>
What are the parameters, and what are their weights?
1. BLAST search of sense strand (1): this should be done **manually** in step 3
2. BLAST search of antisense strand (1): this should be done **manually** in step 3
3. Not located at SNP site (1): in the case of luciferase, this is not necessary; therefore this parameter is, for now, not implemented yet.
4. Not located in first 75 bases from start codon (1)
5. Not in the intron (1): We can exclude this parameter as **our input sequence should already exclude introns**.
6. GC content of 36-52% (1). Note: Amarzguioui et al. suggest 31.6-57.9, one could consider being a bit more tolerant with this parameter. The distribution of GCs probably matters more than total content.
7. Asymmetrical base pairing in the duplex (2): more A/U at 5' of antisense strand and more G/C at 5' of sense strand
8. Energy valley in the 9-14th nucleotide of the sense strand (2)
9. GC repeat less than 3 (0.5)
10. AT repeat less than 4 (0.5)
11. No internal secondary structures and hairpins (2): The secondary structure predictions (MFE and centroid) are retrieved from the RNAfold web server. [The implementation of this parameter will be further explained below.](#secondarystructure)
12. 3'-TT overhangs (1)
13. Weak base pair at 5'-end of antisense (1): presence of A/U
14. Strong base pair at 5'-end of sense (1): presence of G/C
15. Presence of A at 6th position of antisense strand (1)
16. Presence of A at 3rd position of sense strand (0.5)
17. Presence of A at 19th position of sense strand (0.5)
18. Absence of G/C at 19th position of sense strand (1)
19. Absence of G at 13th nucleotide of sense strand (1)
20. Presence of U at 10th nucleotide of sense strand (1)

<a name="secondarystructure"></a>
The file secondarystructure.py retrieves the input DNA sequence, inputs these to the [RNAfold server](http://rna.tbi.univie.ac.at/cgi-bin/RNAWebSuite/RNAfold.cgi), which converts it to the RNA sequence, and then scrapes both the **minimum free energy prediction** as well as the **centroid secondary structure** (=the structure with the minimum total base-pair distance to all structures in the thermodynamic ensemble) off the site, once they have been computed. To ensure robustness we score the secondary structure of both MFE and centroid predictions and then take the average, however some preliminary tests showed that for our sequences tested so far, the scores for the predictions of both models were identical.

The format in which the RNA structure is returned is **dot-bracked notation**. The characters "(" and ")" correspond to the 5' base and the 3' base in the base-pair, respectively, while "." denotes an unpaired base. We are particularly interested in the **unpaired bases**. Roughly speaking, the less the mRNA target sequence is folded onto itself, the more accessible it is for our siRNA. However, the location of unpaired bases is crucial. Gredell et al. [(2008)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2658823/) showed that siRNAs targeting regions of the mRNA predicted to have unpaired 5'- and 3'-ends resulted in greater gene silencing. Therefore, we check for the presence of these so-called **5'- and 3'-loops**. Out of 2 points which can be awarded to a target structure, 0.75 are given for the presence of a 5' loop, another 0.75 for a 3' loop, and the remaining 0.5 are split between "total number of unpaired bases is above average" and "total number of loops is above average". As mentioned before, the  score x/2 is calculated both for the MFE and centroid predicted structure, and then the average of these two scores is calculated. This then constitutes the structure score of an siRNA candidate.

<a name="userinputs"></a>
### User inputs

The user, when running the main.py file in the software_comparisons module, needs to input the mRNA target (plain nucleotides & [FASTA format](https://www.bioinformatics.nl/tools/crab_fasta.html)), a name for your query (e.g. fireflyluc) which only contains letter, and your email, so that the oligowalk and sfold results link can be sent to you once the computation finishes. Further customisable parameters will be added. 

TO-DO: select species, GC content, algo combination for siDirect module.

<a name="blast"></a>
### Step 3: BLAST search to avoid off-target effects

We want to use BLAST (short for Basic Local Alignment Search Tool) to check whether both our antisense strand (the guide strand which is complementary to the mRNA target sequence) and the sense strand (passenger strand, matches mRNA target sequence) are complementary to any gene/mRNA sequence in our organism other than the one we want to target. Both sense and antisense strands should be checked via blast with reference sequence database (Refseq-RNA database) of the desired organism to reduce the risk of silencing unintended genes. 

<a name="ncbi"></a>
**Using the NCBI Blast tool: Which settings to choose?**

- Remember to remove the TT overhang from your sense/antisense sequence before running your alignment check.
- As Blast has some limitations w.r.t. alignment of small sequences, some parameters of blast's algorithms should be changed.
- As we are performing nucleotide-nucleotide compariisons, we choose the Blastn  program. 
- Set the word size to seven in order to have more precise alignment.
- For more stringent specificity checking, set the Expect threshold to a value as high as 1000 or 3000 (similar to primer blast program).

<a name="results"></a>
**Understanding BLAST output**

The statistics reported in the BLAST output tell you different things about how meaningful your alignment is.

For example, coverage tells you whether you have a long or short alignment. Combined with the identity value, it can tell you whether you have a long, low identity match (in the case of genes, this could e.g. signify an orthologous gene), or a short, high identity match (which in the case of genes could signify similar protein domains/active sites). The e-value is a description of how likely it is that the match could have arisen by chance. We will now examine these metrics in more detail.

The **score** is the least informative metric as it is length-dependent. A score of 1000 could arise from a match with a query sequence with 10000 residues, in which case they would be unrelated, or from a match with a 300 residue query sequence, in which case it would signify a true relationship. **Max score** = the highest alignment score calculated from the sum of the rewards for matched nucleotides. **Total score** = the sum of alignment scores of all segments from the same subject sequence

The **e-value**, or expect value, is not length-dependent and often more indicative of a true relationship. It represents the number of alignments expected by chance with the calculated score or better. The lower the e-value, the more statistically significant the match. E.g. an e-value of 0.01 signifies a 1% chance of finding this match in a database of random sequences.

2 factors that strongly influence e-values are (i) the length of the sequence - it is easier to find a perfect match to a shorter sequence than it is to a longer sequence, and (ii) the size of database - it is easier to find a match in a larger database than in a smaller one. The e-value equation is  E=K * m * n * e^( -lambda * S); K and lambda are constants precalculated for the database m=query length, n=database length, S=score of the alignment (raw score).

Raw scores, as mentioned above, are not length normalized, therefore short query sequences cannot achieve high S-scores. The combination of large databases and **short query sequences can lead to relatively high e-values, even if the alignment is virtually identical**. These high e-values make sense because shorter sequences have a higher probability of occuring in the database purely by chance.

**Percent identity** reports on the percentage of basepairs that are the same between your sequence and reference sequence. It is possible that you have a 99% identity match, but only across 35% of your sequence. The latter would be indicated by the **query coverage** metric. In this case, you would have no information on how closely the other 65% of your sequence matches up. 

The **Query coverage** indicates the % of query sequence that overlaps with the reference sequence. If the target sequence in the database spans the whole query sequence, then the query cover is 100%. The smaller the qurey coverage, the less data (nucleotides) are being compared and chance error are higher. E.g. if it is 21%, only 21% of the query sequence matches the subject sequence. If the submitted query was 2889 bases long, 606 were found to align with the subject sequence in the database.

References:
Kim YJ. Computational siRNA design considering alternative splicing. Methods Mol Biol 623, 81–92 (2010)
Fakhr E et al. Precise and efficient siRNA design: a key point in competent gene silencing. Cancer Gene Ther 23, 73–82 (2016)
https://ase.tufts.edu/chemistry/walt/sepa/Activities/BLASTpractice.pdf
https://usuhs.libguides.com/c.php?g=468091&p=3260303
https://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html
https://www.ccg.unam.mx/~vinuesa/tlem/pdfs/Bioinformatics_explained_BLAST.pdf

<a name="evaluate"></a>
**Evaluating BLAST results: what ranges of values are good?**

- In general, real similarity is indicated by: high identity value (>98% sequence similarity), high query cover value (>70%), low e-value (as close to 0 as possible).
- **Coverage**: Queries with >78% coverage with the subject are considered as a risk factor for off-target effects
- **Percent identity**: 15 out of 19 nucleotides matching is tolerable.
- **Further considerations**: it is recommended that candidates that are homologous with >7 nucleotides in undesired genes should be discarded. Note that percent identity, to my understanding, does not necessary consider order though, and that the recommendation refers to stretches of >7 matching nucleotides. Further, it must be mentioned that the attachment of inner nucleotides of siRNA to unwanted genes is more detrimental than the attachment of 3' or 5' ends.
- According to siDirect software, sense and antisense strands with ⩾3 mismatches between siRNA sequence and unintended targets counts as high specificity.
- In summary, less than 78% query coverage with other genes, ⩽15/16 nucleotides out of 19 matching with the respective siRNA, is believed to be tolerable.
- However there is always a probability of unpredictable off-target effects for siRNAs.
