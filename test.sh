#!/usr/bin/bash
../whisper.cpp/stream -m ../whisper.cpp/models/ggml-base.bin -t 8 --step 1000 --length 5000 -l en 2>/dev/null | python scriptmatcher.py alice.txt
