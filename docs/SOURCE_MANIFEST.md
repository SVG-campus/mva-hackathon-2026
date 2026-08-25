# Frozen source manifest — discovery pass

Access date: 2026-08-25 (America/Los_Angeles)

This manifest covers the first-level links exposed by the challenge application and the public source/data repositories. It does not recursively crawl every link on external partner websites.

## Challenge application

| Item | Frozen value | Source |
|---|---:|---|
| Live Space | running | https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/ |
| Public Space repository | `SageBio/rare-disease-real-kid-mva-hackathon-2026` | https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026 |
| Space commit | `37e25dceda63ecec7c5b2ebeffd1ea0052ad886e` | https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/commit/37e25dceda63ecec7c5b2ebeffd1ea0052ad886e |
| Space last modified | `2026-08-24T19:41:49Z` | Hugging Face repository API |
| Submissions open | 2026-08-25 | challenge Overview/source |
| Submission close | 2026-10-24 23:59 UTC | challenge Overview/source |
| Current public Track 1 leaderboard | zero rows at discovery time | public Gradio `/leaderboard_df` endpoint |
| Space source files inventoried | 31 entries | Hugging Face repository tree API |

Public source files inspected: `README.md`, `app.py`, `config.py`, `evaluation.py`, `groundtruth.py`, `requirements.txt`, `tabs/about.py`, `tabs/faq.py`, `tabs/leaderboard.py`, `tabs/rules.py`, `tabs/submit_track1.py`, `tabs/submit_track2.py`, `utils.py`, the CSV template, and the two-sheet Excel methods form.

## Dataset repository

| Item | Frozen value | Source |
|---|---:|---|
| Dataset | `SageBio/mva-hackathon-2026-data` | https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data |
| Dataset commit | `f534cb0c1a607110c6dad0194299bd3dd62df542` | https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data/commit/f534cb0c1a607110c6dad0194299bd3dd62df542 |
| Gating | automatic approval with rule attestation and contact sharing | dataset card/API |
| File count | 13 | repository tree API |
| Total size | 84,985,955,953 bytes (84.986 GB; 79.149 GiB) | repository tree API |
| FASTQs | 84,668,434,104 bytes across eight files | repository tree API |
| VCF | 315,153,971 bytes | repository tree API |
| VCF index | 2,343,376 bytes | repository tree API |
| Clinical phenotype DOCX | 16,865 bytes | repository tree API; content intentionally not accessed |

The VCF-only route reduces gated transfer from about 85 GB to about 318 MB including its index. Whether it is analytically sufficient remains a live falsifier.

## Official templates pinned locally

| File | SHA-256 |
|---|---|
| `challenge_reference/evaluation.py` | `6D18B581E65A45E1CCC120071D588E740C2E42E983FF50704C60A40232B19180` |
| `challenge_reference/track1_submission_template.csv` | `7B3ED41C091D34FB6C5622D049C7A3F46124211FC7EC02947E69DAEF8752755A` |
| `challenge_reference/methods_description_form.xlsx` | `E160C3B12DFF23584660DE42FB13095AC1D592C991FFF92714E6F7F6678249B4` |

## First-level link traversal

All substantive outbound links encoded in the challenge source were opened or fetched during discovery:

| Destination | Role |
|---|---|
| https://mvasociety.org/ | patient organization and MVA background |
| https://sagebionetworks.org/ | organizer |
| https://huggingface.co/ | platform |
| https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data | gated dataset |
| https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions | community and updates |
| https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/1 | signup-support discussion |
| https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2 | unresolved third-party LLM/data-handling discussion |
| https://huggingface.co/terms-of-service | required platform terms |
| https://huggingface.co/join | registration route |
| https://conscience.ca/beacon/ | benchmarking partner |
| https://aws.amazon.com/ | prize sponsor |
| https://www.anthropic.com/ | prize sponsor |
| https://wilhelmfoundation.org/ | acknowledged advisor |
| `/file=static/templates/track1_submission_template.csv` | downloaded and hashed |
| `/file=static/templates/methods_description_form.xlsx` | downloaded, structurally inspected, visually rendered, and hashed |

The Google Fonts endpoints are presentation dependencies, not challenge evidence. GitHub and YouTube/Vimeo appear as required submission destinations or input placeholders, not as preselected project links.

## Relevant scientific and benchmark sources

- Stenton et al., *Human Genomics* (2024), CAGI6 Rare Genomes Project assessment: https://doi.org/10.1186/s40246-024-00604-w
- Malumbres and Villarroya-Beltri, *Nature Reviews Genetics* (2024), MVA biology: https://doi.org/10.1038/s41576-024-00762-6
- ClinGen definitive BUB1B–MVA1 validity curation: https://search.clinicalgenome.org/kb/gene-validity/CGGV%3Aassertion_59147f27-d5a3-4760-ba8d-0429bae3c906-2019-11-22T14%3A53%3A26.352Z
- Frattini et al. (2025), review of seven numbered MVA forms: https://doi.org/10.1002/ajmg.a.63901
- Suijkerbuijk et al. (2010), BUBR1 dysfunction in MVA patient cells: https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/
- Yost et al. (2017), biallelic TRIP13 mechanism: https://pmc.ncbi.nlm.nih.gov/articles/PMC5493194/
- de Wolf et al. (2021), CENATAC: https://doi.org/10.15252/embj.2020106536
- Grange et al. (2022), SLF2/SMC5: https://pmc.ncbi.nlm.nih.gov/articles/PMC9636423/
- Villarroya-Beltri et al. (2022), MAD1L1: https://pubmed.ncbi.nlm.nih.gov/36322655/
- Abdel-Salam et al. (2023), MAD2L1BP: https://pubmed.ncbi.nlm.nih.gov/37796616/
- Carvalhal et al. (2022), BUB1: https://pmc.ncbi.nlm.nih.gov/articles/PMC8769543/
- Guo et al. (2024), CEP192: https://doi.org/10.1016/j.xhgg.2023.100256
- Ochiai et al. (2014), functional proof of an upstream BUB1B variant: https://pmc.ncbi.nlm.nih.gov/articles/PMC3910577/
