"""Build supplement v3 from the deposited supplement v2: align the file
ledger section with the current deposit state (the versioned extension
ledgers certificate_sha256_v5.txt / _v6.txt of the v18/v19 rounds,
which extend without altering the base ledger).

Note: a suspected '\\begin{table}]' bracket defect turned out to be a
display artifact of the tool output (the actual source is
'\\begin{table}[h]', a normal float specifier, verified by hexdump);
no such fix is applied --- the asserted-anchor discipline refused the
non-existent anchor, which is exactly what it is for.

Asserted-anchor editing (never overwrite: writes supplement_v3.tex as
a NEW file).
"""

SRC = '/home/z/my-project/fuller-workspace/extracted/versions/supplement_v2.tex'
DST = 'supplement_v3.tex'

text = open(SRC).read()


def rep(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, f"anchor x{n} (want {count}): {old[:90]!r}"
    text = text.replace(old, new, count)


# sanity: the float specifiers are normal [h]/[t], no stray brackets
assert text.count(r"\begin{table}[h]") == 4
assert text.count(r"\begin{table}]") == 0

# 1. version header
rep("\\documentclass[aps,prx,reprint,superscriptaddress,nobibnotes,"
    "longbibliography]{revtex4-2}",
    "% v3 (v20 alignment round): the file-ledger section now records the\n"
    "% versioned extension ledgers certificate_sha256_v5.txt / _v6.txt of\n"
    "% the v18/v19 deposit rounds (which extend, never alter, the base\n"
    "% ledger).  Content otherwise unchanged from the deposited v2.\n"
    "\\documentclass[aps,prx,reprint,superscriptaddress,nobibnotes,"
    "longbibliography]{revtex4-2}")

# 2. ledger note (align with the current deposit state)
rep("the same list, in \\texttt{sha256sum} format, is the ledger "
    "\\texttt{certificate\\_sha256.txt}, so that "
    "\\texttt{sha256sum -c certificate\\_sha256.txt} verifies the "
    "deposit.",
    "the same list, in \\texttt{sha256sum} format, is the ledger "
    "\\texttt{certificate\\_sha256.txt}, so that "
    "\\texttt{sha256sum -c certificate\\_sha256.txt} verifies the "
    "deposit.  The later deposit rounds extend the ledger without "
    "altering any entry above: \\texttt{certificate\\_sha256\\_v5.txt} "
    "(the $n=4$ colour-resolved scans, the first $n=5$ diagnostics, and "
    "the Haar sequential-Monte-Carlo results quoted in the main text) "
    "and \\texttt{certificate\\_sha256\\_v6.txt} (the $n=5$ two-size "
    "test, the $n=4$ $L=10$ third crossing, and the no-freezing-theorem "
    "verification), each self-verifying in the same way.")

open(DST, 'w').write(text)
print(f"wrote {DST} ({len(text)} chars)")
assert "certificate\\_sha256\\_v5.txt" in text
print("self-check passed")
