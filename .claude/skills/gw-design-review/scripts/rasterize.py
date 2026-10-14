#!/usr/bin/env python3
"""Render PDF pages to PNG images so they can be viewed and audited.

Usage
-----
    python3 rasterize.py design.pdf                    every page, 150 dpi, into a temp folder
    python3 rasterize.py design.pdf --pages 3          one page
    python3 rasterize.py design.pdf --pages 2-4 --dpi 300 --out review-pages/

Prints one PNG path per line, named by real page number (page-03.png is page 3), so
findings can cite pages correctly.

Backends, tried in this order — whichever is installed first is used:
    pdftoppm      (poppler: brew install poppler / apt-get install poppler-utils)
    Ghostscript   (brew install ghostscript / apt-get install ghostscript)
    pypdfium2     (pip install pypdfium2 — pure wheel, no system packages; easiest to add)
    PyMuPDF       (pip install pymupdf)
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile

# 150 dpi renders US Letter at 1275x1650 px: enough to read 9 pt type, and close to the
# ~1600 px long edge that image viewers in AI clients downscale to anyway, so higher values
# mostly cost time. For fine detail (captions, logo clear space), use --dpi 300 and crop.
DEFAULT_DPI = 150


def parse_pages(spec):
    """'3' -> (3, 3); '2-5' -> (2, 5); None -> (None, None)."""
    if not spec:
        return None, None
    try:
        if "-" in spec:
            a, b = spec.split("-", 1)
            first, last = int(a), int(b)
        else:
            first = last = int(spec)
    except ValueError:
        raise ValueError(f"--pages must look like 3 or 2-5, not {spec!r}")
    if first < 1 or last < first:
        raise ValueError(f"--pages range {spec!r} is empty or starts below 1")
    return first, last


def _pdftoppm(pdf, work, dpi, first, last):
    exe = shutil.which("pdftoppm")
    if not exe:
        return None
    cmd = [exe, "-r", str(dpi), "-png"]
    if first:
        cmd += ["-f", str(first), "-l", str(last)]
    subprocess.run(cmd + [pdf, os.path.join(work, "p")], check=True, capture_output=True)
    return sorted(glob.glob(os.path.join(work, "p*.png")))


def _ghostscript(pdf, work, dpi, first, last):
    exe = shutil.which("gs") or shutil.which("gswin64c")
    if not exe:
        return None
    cmd = [exe, "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=png16m", f"-r{dpi}",
           "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4"]          # antialiased, like a viewer
    if first:
        cmd += [f"-dFirstPage={first}", f"-dLastPage={last}"]
    cmd += [f"-sOutputFile={os.path.join(work, 'p%04d.png')}", pdf]
    subprocess.run(cmd, check=True, capture_output=True)
    return sorted(glob.glob(os.path.join(work, "p*.png")))


def _pypdfium2(pdf, work, dpi, first, last):
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return None
    doc = pdfium.PdfDocument(pdf)
    first, last = first or 1, min(last or len(doc), len(doc))
    out = []
    for n in range(first, last + 1):
        path = os.path.join(work, f"p{n:04d}.png")
        doc[n - 1].render(scale=dpi / 72).to_pil().save(path)
        out.append(path)
    return out


def _pymupdf(pdf, work, dpi, first, last):
    try:
        import fitz
    except ImportError:
        return None
    doc = fitz.open(pdf)
    first, last = first or 1, min(last or len(doc), len(doc))
    out = []
    for n in range(first, last + 1):
        path = os.path.join(work, f"p{n:04d}.png")
        doc[n - 1].get_pixmap(dpi=dpi).save(path)
        out.append(path)
    return out


BACKENDS = [("pdftoppm", _pdftoppm), ("Ghostscript", _ghostscript),
            ("pypdfium2", _pypdfium2), ("PyMuPDF", _pymupdf)]


def rasterize(pdf, out_dir=None, dpi=DEFAULT_DPI, pages=None, quiet=False):
    """Render pages of `pdf` to PNGs. Returns the list of paths, in page order."""
    if not os.path.isfile(pdf):
        raise FileNotFoundError(f"no such file: {pdf}")
    first, last = parse_pages(pages)
    stem = os.path.splitext(os.path.basename(pdf))[0]
    out_dir = out_dir or tempfile.mkdtemp(prefix=f"{stem}-pages-")
    os.makedirs(out_dir, exist_ok=True)

    failures = []
    for label, backend in BACKENDS:
        work = tempfile.mkdtemp(prefix="raster-")
        try:
            produced = backend(pdf, work, dpi, first, last)
            if produced is None:
                continue                                  # not installed; try the next one
            if not produced:
                failures.append(f"{label}: produced no pages (is the page range past the end?)")
                continue
            # Rename to real page numbers, whatever numbering the backend used.
            start = first or 1
            final = []
            for i, path in enumerate(produced):
                dest = os.path.join(out_dir, f"page-{start + i:02d}.png")
                shutil.move(path, dest)
                final.append(dest)
            if not quiet:
                print(f"Rendered {len(final)} page(s) at {dpi} dpi with {label} into {out_dir}",
                      file=sys.stderr)
            return final
        except subprocess.CalledProcessError as exc:
            msg = (exc.stderr or b"").decode(errors="replace").strip().splitlines()
            failures.append(f"{label}: {msg[-1] if msg else 'failed'}")
        except Exception as exc:                          # a broken PDF, usually
            failures.append(f"{label}: {exc}")
        finally:
            shutil.rmtree(work, ignore_errors=True)

    if failures:
        raise RuntimeError("could not render the PDF:\n  " + "\n  ".join(failures))
    raise RuntimeError(
        "no PDF renderer is installed. Install any one of:\n"
        "  pip install pypdfium2                (no system packages needed)\n"
        "  brew install poppler                 (or: apt-get install poppler-utils)\n"
        "  brew install ghostscript             (or: apt-get install ghostscript)\n"
        "If nothing can be installed here, ask the user for PNG exports of the pages.")


def main(argv):
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG images.")
    parser.add_argument("pdf")
    parser.add_argument("--out", metavar="DIR", help="output folder (default: a new temp folder)")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI,
                        help=f"resolution (default {DEFAULT_DPI}; use 300 for fine detail)")
    parser.add_argument("--pages", metavar="N or A-B", help="one page or a range (default: all)")
    args = parser.parse_args(argv[1:])
    try:
        for path in rasterize(args.pdf, args.out, args.dpi, args.pages):
            print(path)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
