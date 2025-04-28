Paediatric Pre-Ictal EEG Pipeline (Code-Only Release)
This repository hosts all source code and minimal configuration files needed to reproduce the six-step preprocessing and feature-extraction workflow documented in wholeCodes.docx — a streamlined, laptop-friendly pipeline that converts raw CHB-MIT paediatric EEG into 5-second, artefact-suppressed segments with rich feature vectors for downstream seizure-prediction research. ​

🔑 Key points
Target cohort: children < 10 years drawn from CHB-MIT (cases chb05, 06, 08, 09, 10, 12, 13, 14, 16, 20, 22, 23).

Data reduction: only the 30 s immediately before each seizure are retained, yielding 96 excerpts → 576 five-second segments.

Six automated stages:

Pre-ictal cropping (EDF)

ICA + kurtosis cleaning (FIF)

Per-channel z-score normalisation with QC report

Histogram-based normalisation audit (Word + PNG)

Non-overlapping 5-s slicing

Time / spectral / Sample-Entropy feature extraction with tabulated Word output

Zero-GPU requirement: end-to-end runtime ≈ 3 h on a single Intel i7-1165G7 / 16 GB RAM.

