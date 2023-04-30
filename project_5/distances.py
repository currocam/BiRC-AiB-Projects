import subprocess
import pandas as pd

SAMPLES = [
    "1347_FAINT",
    "1689_FGGY_N",
    "214_Arena_glycoprot",
    "494_Astro_capsid",
    "877_Glu_synthase",
    "1493_Fe-ADH",
    "1756_FAD_binding_3",
    "304_A1_Propeptide",
    "608_Gemini_AL2",
    "89_Adeno_E3_CR1",
    "1560_Ferritin",
    "1849_FG-GAP",
    "401_DDE",
    "777_Gemini_V1",
]

dists = list()
samples_ls, files1, files2 = list(), list(), list()
for sample in SAMPLES:
    python = f"output/{sample}_python.newick"
    rapidnj = f"output/{sample}_rapidnj.newick"
    quicktree = f"output/{sample}_quicktree.newick"
    dists.append(subprocess.check_output(["python", "rfdist.py", python, rapidnj]))
    dists.append(subprocess.check_output(["python", "rfdist.py", rapidnj, quicktree]))
    dists.append(subprocess.check_output(["python", "rfdist.py", quicktree, python]))
    samples_ls.extend([sample, sample, sample])
    files1.extend(["python", "rapidnj", "quicktree"])
    files2.extend(["rapidnj", "quicktree", "python"])

dists = [int(x) for x in dists]
data = {"sample": samples_ls, "file1": files1, "file2": files2, "dist": dists}
df = pd.DataFrame(data)
df.to_csv("distances.csv", index=False)
