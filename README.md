# Simple tools to make/dump CPC+ CPR cartridge files

- mkcpr.py: make a CPR file from files (one chunk per file); see notes
- cprdump.py: dump the chunks of a CPR file; will skip zero length chunks

Notes:

- The files can't have more than 16K
- Any files with less than 16K won't be padded by the tool (unless `-p` option is used)
- If less than 32 files are provided, zero length chunks wll be added to complete the CPR
- Won't process more than 32 banks
- Use `-r` flag to generate a RAW cartridge

The tools require Python 3, with no other dependency. Run them with `-h` for CLI help.

