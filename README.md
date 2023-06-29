# SQUIM Report
This is an usage implementation of [TorchAudio-SQUIM](https://ieeexplore.ieee.org/document/10096680). The end goal is to create a dataset report generator based on the speech quality objective metrics - STOI, PESQ, SI-SDR. May consider adding other metrics in the future.

## TODOs
- [x] Script to estimate SQUIM for a single audio file
- [x] Gradio demo for estimating SQUIM a single audio file
- [ ] Dataset report generator 

## Install
Note: TorchAudio-SQUIM is still in development, and only available in [TorchAudio's main branch](https://pytorch.org/audio/main/prototype.pipelines.html#squim-objective). You will have to install the preview (nightly) build to use it. Run the command below to install the nightly build for CUDA 11.8 using pip, or head over to [pytorch.org](https://pytorch.org/) for other versions.

```shell
# CUDA 11.8 nightly build
pip3 install --pre torch torchaudio --index-url https://download.pytorch.org/whl/nightly/cu118
# for Gradio demo
pip3 install gradio
# Clone repository
git clone https://github.com/test-dan-run/squim-report.git
```

## How to Use
For a single file.
```shell
python3 infer.py <path-to-audio-file>
# [test.wav] SQUIM scores: {'STOI': 0.677, 'PESQ': 1.194, 'SI-SDR': -1.396}
```

## Citations

```bibtex
@INPROCEEDINGS{10096680,
  author={Kumar, Anurag and Tan, Ke and Ni, Zhaoheng and Manocha, Pranay and Zhang, Xiaohui and Henderson, Ethan and Xu, Buye},
  booktitle={ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)}, 
  title={Torchaudio-Squim: Reference-Less Speech Quality and Intelligibility Measures in Torchaudio}, 
  year={2023},
  volume={},
  number={},
  pages={1-5},
  doi={10.1109/ICASSP49357.2023.10096680}}

```