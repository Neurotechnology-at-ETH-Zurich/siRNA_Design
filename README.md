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
2. siRNA Wizard
3. siDirect
4. siDESIGN center
5. sFold
6. RNAi explorer
7. Oligowalk
8. IDT
9. Eurofins_siMax

1. ThermoFisher's BLOCK-iT RNAi Designer
For our purposes, [this tool](https://rnaidesigner.thermofisher.com/rnaiexpress/) provides sequences which can then be ordered from ThermoFisher with additional chemical modifications they do not disclose; the product is named 'Stealth RNAi siRNA'. The algorithm this tool relies on is proprietary, and the only parameters we can manually set are species and G/C percentage (min & max).

These modules are called in the main.py file, which further relies on the helper_functions.py script.
