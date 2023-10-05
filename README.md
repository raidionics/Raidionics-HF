---
title: 'Raidionics: preoperative central nervous system tumor segmentation'
colorFrom: indigo
colorTo: indigo
sdk: docker
app_port: 7860
emoji: 🧠
pinned: false
license: mit
app_file: app.py
---

<div align="center">
<h1 align="center">Raidionics</h1>
<h3 align="center">preoperative central nervous system tumor segmentation</h3>

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
[![CI/CD](https://github.com/raidionics/Raidionics-HF/actions/workflows/deploy.yml/badge.svg)](https://github.com/raidionics/Raidionics-HF/actions/workflows/deploy.yml)
<a target="_blank" href="https://huggingface.co/spaces/dbouget/raidionics"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>

**Raidionics-HF** was developed by SINTEF Medical Image Analysis to accelerate medical AI research.

</div>

## [Brief intro](https://github.com/raidionics/Raidionics-HF#brief-intro)

This web application enables users to easily test our deep learning models for preoperative central nervous system tumor segmentation.
The plugin is built on top of gradio using the same backend as used for the [Raidionics](https://raidionics.github.io/) software.
Raidionics is an open-source, free-to-use desktop application for pre- and postoperative central nervous system tumor segmentation and standardized reporting.

## [Demo](https://github.com/raidionics/RaidionicsHF#demo) <a target="_blank" href="https://huggingface.co/spaces/dbouget/raidionics"><img src="https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg"></a>

To access the live demo, click on the `Hugging Face` badge above. Below is a snapshot of the current state of the demo app.

<img width="1800" alt="Screenshot 2023-10-04 at 19 10 23" src="https://github.com/raidionics/AeroPath/assets/29090665/8777945b-1c9f-4345-87d9-c530d28cc5ce">

## [Development](https://github.com/raidionics/RaidionicsHF#development)

### [Docker](https://github.com/raidionics/RaidionicsHF#docker)

Alternatively, you can deploy the software locally. Note that this is only relevant for development purposes. Simply dockerize the app and run it:

```
docker build -t RaidionicsHF .
docker run -it -p 7860:7860 RaidionicsHF
```

Then open `http://127.0.0.1:7860` in your favourite internet browser to view the demo.

### [Python](https://github.com/raidionics/RaidionicsHF#python)

It is also possible to run the app locally without Docker. Just setup a virtual environment and run the app.
Note that the current working directory would need to be adjusted based on where `Raidionics-HF` is located on disk.

```
git clone https://github.com/raidionics/Raidionics-HF.git
cd Raidionics-HF/

virtualenv -python3 venv --clear
source venv/bin/activate
pip install -r requirements.txt

python app.py --cwd ./
```

## [Troubleshooting](https://github.com/raidionics/RaidionicsHF#troubleshooting)

Due to `share=True` being enabled by default when launching the app,
internet access is required for the app to be launched. This can disabled by setting
the argument to `--share 0`.

## [Citation](https://github.com/raidionics/RaidionicsHF#citation)

If you found this tool relevant in your research, please cite the following references enabling the backend compute magic.

The final software including updated performance metrics for preoperative tumors and introducing postoperative tumor segmentation:
```
@article{bouget2023raidionics,
    author = {Bouget, David and Alsinan, Demah and Gaitan, Valeria and Holden Helland, Ragnhild and Pedersen, André and Solheim, Ole and Reinertsen, Ingerid},
    year = {2023},
    month = {09},
    pages = {},
    title = {Raidionics: an open software for pre-and postoperative central nervous system tumor segmentation and standardized reporting},
    volume = {13},
    journal = {Scientific Reports},
    doi = {10.1038/s41598-023-42048-7},
}
```

For the preliminary preoperative tumor segmentation validation and software features:
```
@article{bouget2022preoptumorseg,
    title={Preoperative Brain Tumor Imaging: Models and Software for Segmentation and Standardized Reporting},
    author={Bouget, David and Pedersen, André and Jakola, Asgeir S. and Kavouridis, Vasileios and Emblem, Kyrre E. and Eijgelaar, Roelant S. and Kommers, Ivar and Ardon, Hilko and Barkhof, Frederik and Bello, Lorenzo and Berger, Mitchel S. and Conti Nibali, Marco and Furtner, Julia and Hervey-Jumper, Shawn and Idema, Albert J. S. and Kiesel, Barbara and Kloet, Alfred and Mandonnet, Emmanuel and Müller, Domenique M. J. and Robe, Pierre A. and Rossi, Marco and Sciortino, Tommaso and Van den Brink, Wimar A. and Wagemakers, Michiel and Widhalm, Georg and Witte, Marnix G. and Zwinderman, Aeilko H. and De Witt Hamer, Philip C. and Solheim, Ole and Reinertsen, Ingerid},
    journal={Frontiers in Neurology},
    volume={13},
    year={2022},
    url={https://www.frontiersin.org/articles/10.3389/fneur.2022.932219},
    doi={10.3389/fneur.2022.932219},
    issn={1664-2295}
}
```