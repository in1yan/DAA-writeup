#!/usr/bin/env python3
"""
PDF Combiner Script
Combines all PDF files in a directory into a single PDF file.

Usage:
    python combine_pdfs.py -d <directory> -o <output_file>
    python combine_pdfs.py --directory <directory> --output <output_file>
"""

import os
import sys
import argparse
from pathlib import Path
try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("Error: PyPDF2 is not installed.")
    print("Please install it using: pip install PyPDF2")
    sys.exit(1)


def get_pdf_files(directory):
    """
    Get all PDF files from the specified directory.
    
    Args:
        directory (str): Path to the directory containing PDF files
        
    Returns:
        list: Sorted list of PDF file paths
    """
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if not directory_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")
    
    # Get all PDF files and sort them naturally
    pdf_files = sorted([f for f in directory_path.glob("*.pdf")])
    
    if not pdf_files:
        raise ValueError(f"No PDF files found in directory: {directory}")
    
    return pdf_files


def combine_pdfs(pdf_files, output_file):
    """
    Combine multiple PDF files into a single PDF.
    
    Args:
        pdf_files (list): List of PDF file paths to combine
        output_file (str): Path to the output PDF file
    """
    merger = PdfMerger()
    
    print(f"Combining {len(pdf_files)} PDF files...")
    
    for pdf_file in pdf_files:
        print(f"  Adding: {pdf_file.name}")
        try:
            merger.append(str(pdf_file))
        except Exception as e:
            print(f"  Warning: Could not add {pdf_file.name}: {e}")
            continue
    
    # Write the combined PDF to the output file
    print(f"\nWriting combined PDF to: {output_file}")
    merger.write(output_file)
    merger.close()
    
    print(f"✓ Successfully combined {len(pdf_files)} PDF files into {output_file}")


def main():
    """Main function to handle command-line arguments and orchestrate PDF combination."""
    parser = argparse.ArgumentParser(
        description="Combine all PDF files in a directory into a single PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python combine_pdfs.py -d ./pdfs -o combined.pdf
  python combine_pdfs.py --directory /path/to/pdfs --output output.pdf
  python combine_pdfs.py  # Uses current directory and default output name
        """
    )
    
    parser.add_argument(
        "-d", "--directory",
        type=str,
        default=".",
        help="Directory containing PDF files (default: current directory)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="combined_output.pdf",
        help="Output PDF file name (default: combined_output.pdf)"
    )
    
    parser.add_argument(
        "-s", "--sort",
        choices=["name", "numeric", "date"],
        default="numeric",
        help="Sort method for PDF files (default: numeric)"
    )
    
    args = parser.parse_args()
    
    try:
        # Get all PDF files from the directory
        pdf_files = get_pdf_files(args.directory)
        
        # Sort files based on the chosen method
        if args.sort == "numeric":
            # Natural/numeric sorting (1, 2, 10 instead of 1, 10, 2)
            pdf_files = sorted(pdf_files, key=lambda x: [
                int(c) if c.isdigit() else c.lower() 
                for c in ''.join(filter(str.isalnum, x.stem))
            ])
        elif args.sort == "date":
            # Sort by modification time
            pdf_files = sorted(pdf_files, key=lambda x: x.stat().st_mtime)
        # 'name' uses the default alphabetical sorting from get_pdf_files
        
        # Combine PDFs
        combine_pdfs(pdf_files, args.output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
