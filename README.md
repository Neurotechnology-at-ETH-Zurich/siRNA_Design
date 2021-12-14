## siRNA Design Pipeline
Collection of tools to retrieve siRNA (small interfering RNA) candidate sequences targeting your gene of interest from popular siRNA design tools, identify which candidates are suggested by multiple different software tools, and perform further quality checking and validation on identified candidates.

General notes:

- We are designing 21nt siRNA sequences (19nt + 2nt TT overhangs).
- ...

### Step 1: Retrieving siRNA candidate sequences suggested by a variety of design algorithms and softwares. 
siRNA candidates which are suggested by multiple tools (>3) will be further analysed in step 2 based on a 20-parameter quality scoring system.
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

For our purposes, [this tool](https://rnaidesigner.thermofisher.com/rnaiexpress/) provides sequences which can then be ordered from ThermoFisher with additional chemical modifications they do not disclose; the product is named 'Stealth RNAi siRNA'. The algorithm this tool relies on is proprietary, and the only parameters we can manually set are species and G/C percentage (min & max).

2. RNA Wizard

We know that this tool considers optimal internal stability of siRNAs, and excludes immunogenic sequences. However also here, we cannot choose the underlying algorithms and parameters.

3. siDirect

This tool allows us to choose from different algorithms and their combinations.

4. siDESIGN center

The siDESIGN center by Dharmacon (which was acquired by Horizon Discovery) is based on the algorithms by [Elbashir et al.](https://www.sciencedirect.com/science/article/abs/pii/S1046202302000233?via%3Dihub) and [Reynolds et al](https://www.nature.com/articles/nbt936). If the nucleotide sequence is provided as input, the seed region specificity of siRNAs can be evaluated - this is relevant for estimating off-target effects. The exact matches of the seed region of siRNA to the 3' UTR of the genes are determined; the lower frequency of seed region in the target genome proves the specificity of siRNA.

5. sFold

6. RNAi Explorer

This tool does not include different algorithms and parameters. The page seems to be faulty; it remains to be seen whether this defect is temporary. If the page stays down, RNAi Explorer will be excluded from this project.

7. Oligowalk

This tool provides comprehensive thermodynamic information, as well as an estimated probability of it being efficient siRNA. The results are sent per email, which takes several hours. The code is written so that the link which one receives per e-mail can be pasted into the console, upon which the results are analysed. A drawback of Oligowalk is that it has not been updated since 2008.

8. SiRNA Design (IDT)

This tool considers asymmetrical end stability, which is an important siRNA design parameter.

9. Eurofins siMax




