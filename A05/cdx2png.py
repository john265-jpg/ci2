#!/usr/bin/env python3
"""
cdx2png.py (RDKit Version)
Converts ChemDraw CDXML files to PNG images and finds the molecules 
with the lowest and highest relative molecular weights (Mr).
"""

import sys
import os
import glob
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw
from rdkit.Chem import AllChem

def main():
    if len(sys.argv) < 2:
        print("Error: No input files provided.", file=sys.stderr)
        print("Usage: python cdx2png.py <file1.cdxml> [file2.cdxml ...] or python cdx2png.py *.cdxml", file=sys.stderr)
        sys.exit(1)

    # Expand wildcards (e.g., rx*.cdxml or *.cdxml) for Windows/Linux compatibility
    input_args = []
    for arg in sys.argv[1:]:
        matched = glob.glob(arg)
        if matched:
            input_args.extend(matched)
        else:
            input_args.append(arg)

    min_mw = float('inf')
    max_mw = float('-inf')
    min_filename = None
    max_filename = None

    converted_count = 0

    for cdxml_filename in input_args:
        base, ext = os.path.splitext(cdxml_filename)
        if not ext:
            cdxml_filename += ".cdxml"
            base_name = base
        else:
            base_name = base

        if not os.path.exists(cdxml_filename):
            print(f"Warning: File '{cdxml_filename}' not found. Skipping.", file=sys.stderr)
            continue

        png_filename = base_name + ".png"

        try:
            # Parse the CDXML file natively using RDKit
            mols = Chem.MolsFromCDXMLFile(cdxml_filename)
            valid_mols = [m for m in mols if m is not None]
            
            if not valid_mols:
                print(f"Warning: No valid molecules found in '{cdxml_filename}'. Skipping.", file=sys.stderr)
                continue

            # Select the first molecule structure in the file
            mol = valid_mols[0]

            # Compute relative molecular weight (Mr)
            mw = Descriptors.MolWt(mol)

            # Generate 2D depiction coordinates for clear rendering
            AllChem.Compute2DCoords(mol)

            # Render and save to PNG
            Draw.MolToFile(mol, png_filename, size=(500, 500))
            print(f"Converted: {cdxml_filename} -> {png_filename} (Mr: {mw:.3f})")
            converted_count += 1

            # Track minimum molecular weight
            if mw < min_mw:
                min_mw = mw
                min_filename = cdxml_filename

            # Track maximum molecular weight
            if mw > max_mw:
                max_mw = mw
                max_filename = cdxml_filename

        except Exception as e:
            print(f"Error processing '{cdxml_filename}': {e}", file=sys.stderr)

    # Print summary results to standard output
    if converted_count > 0 and min_filename and max_filename:
        print("\n" + "="*40)
        print(" MOLECULAR WEIGHT (Mr) SUMMARY")
        print("="*40)
        print(f"Lowest Mr:")
        print(f"  File : {min_filename}")
        print(f"  Mr   : {min_mw:.3f}")
        print("-" * 40)
        print(f"Largest Mr:")
        print(f"  File : {max_filename}")
        print(f"  Mr   : {max_mw:.3f}")
        print("="*40)
    else:
        print("\nNo valid molecules were successfully converted.")

if __name__ == "__main__":
    main()