import sys
import re

sourceFile = sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.read()

orca_sig = r'(; generated by OrcaSlicer(.*))'
lines = re.sub(orca_sig, r"; generated by SuperSlicer\2", lines)

if "MANUAL_TOOL_CHANGE" not in lines:

    # Localize o índice da primeira ocorrência de "PAUSE"
    pause_index = lines.find("PAUSE")

    # Remova a primeira ocorrência de "PAUSE" se encontrada
    if pause_index != -1:
        lines = lines[:pause_index] + lines[pause_index:].replace("PAUSE", "", 1)  

    # Localize o índice da linha "; CP TOOLCHANGE LOAD"
    toolchange_load_indices = [i for i, line in enumerate(lines.split('\n')) if "; CP TOOLCHANGE LOAD" in line]

    # Para cada ocorrência de "; CP TOOLCHANGE LOAD"
    for toolchange_load_index in toolchange_load_indices:
        # Verifique as 5 linhas seguintes
        for i in range(toolchange_load_index + 1, min(toolchange_load_index + 6, len(lines.split('\n')))):
            if "E18.0000" in lines.split('\n')[i] or "E63.0000" in lines.split('\n')[i] or "E9.0000" in lines.split('\n')[i]:
                # Substitua os valores por "E0.4"
                lines = lines.replace("E18.0000", "E0.1").replace("E63.0000", "E0.1").replace("E9.0000", "E0.1")

    # Localize o índice da linha "; Retract(unload)"
    retract_unload_indices = [i for i, line in enumerate(lines.split('\n')) if "; Retract(unload)" in line]

    # Para cada ocorrência de "; Retract(unload)"
    for retract_unload_index in retract_unload_indices:
        # Verifique as 4 linhas seguintes
        for i in range(retract_unload_index + 1, min(retract_unload_index + 5, len(lines.split('\n')))):
            if "E-15.0000" in lines.split('\n')[i] or "E-55.3000" in lines.split('\n')[i] or "E-15.8000" in lines.split('\n')[i] or "E-7.9000" in lines.split('\n')[i]:
                # Substitua os valores por "E0.4"
                lines = lines.replace("E-15.0000", "E-0.1").replace("E-55.3000", "E-0.1").replace("E-15.8000", "E-0.1").replace("E-7.9000", "E-0.1")

with open(sourceFile, "w") as of:
    of.write(lines)
