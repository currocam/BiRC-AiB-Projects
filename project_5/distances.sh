#!/bin/bash
# Path to the directory containing the input files
input_dir="output"
program="rfdist.py"
# Extension of the input files
extension=".newick"

# Define the list of files
SAMPLES=(
    "1347_FAINT"
    "1689_FGGY_N"
    "214_Arena_glycoprot"
    "494_Astro_capsid"
    "877_Glu_synthase"
    "1493_Fe-ADH"
    "1756_FAD_binding_3"
    "304_A1_Propeptide"
    "608_Gemini_AL2"
    "89_Adeno_E3_CR1"
    "1560_Ferritin"
    "1849_FG-GAP"
    "401_DDE"
    "777_Gemini_V1"
)
programs=(python rapidnj quicktree)


# Loop over each file in the list
for sample in "${SAMPLES[@]}"
    do  
    echo $sample,python,rapidnj, $(python rfdist.py output/$sample_python.newick output/$sample_rapidnj.newick) >> distances.csv
    done
#!/bin/bash
# Path to the directory containing the input files
input_dir="output"
program="rfdist.py"
# Extension of the input files
extension=".newick"

# Define the list of files
SAMPLES=(
    "1347_FAINT"
    "1689_FGGY_N"
    "214_Arena_glycoprot"
    "494_Astro_capsid"
    "877_Glu_synthase"
    "1493_Fe-ADH"
    "1756_FAD_binding_3"
    "304_A1_Propeptide"
    "608_Gemini_AL2"
    "89_Adeno_E3_CR1"
    "1560_Ferritin"
    "1849_FG-GAP"
    "401_DDE"
    "777_Gemini_V1"
)
programs=(python rapidnj quicktree)


# Loop over each file in the list
for sample in "${SAMPLES[@]}"
    do  
    echo $sample,python,rapidnj, $(python rfdist.py output/$sample_python.newick output/$sample_rapidnj.newick) >> distances.csv
    done
