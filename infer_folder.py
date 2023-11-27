import glob
import argparse
import pandas as pd
from typing import List, Dict, Union, Any

from squim import SquimProcessor

def estimate(processor: SquimProcessor, audio_dir: str, recurse: bool = False, filetypes: Union[str, List[str]] = 'wav') -> List[Dict[str, Any]]:

    audio_filepaths = []

    # if only a single filetype, encapsulate it with a list
    if type(filetypes) is str:
        filetypes = [filetypes,]

    for ft in filetypes:
        if recurse:
            globbed_paths = glob.glob(f'{audio_dir}/**/*.{ft}', recursive=True)
        else:
            globbed_paths = glob.glob(f'{audio_dir}/*.{ft}')
        audio_filepaths.extend(globbed_paths)

    estimates = processor.estimate(audio_filepaths)

    # generate a list of results in the following format:
    # i.e. [{'FILEPATH': 'rel/path/to/audio.wav', 'STOI': xxx, 'PESQ': yyy, 'SI-SDR': zzz}, ...]
    results = []
    for fp, est in zip(audio_filepaths, estimates):
        out_dict = {'FILEPATH': fp}
        out_dict.update(est)
        results.append(out_dict)
    
    return results

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Estimate objective SQUIM values for audio files.')
    parser.add_argument('audio_dir', type=str, help='Directory to audio files.')
    parser.add_argument('--recurse', action='store_true', help='Whether to recursively scan through all sub folders for audio files.')
    parser.add_argument('--output_file', type=str, default='squim_report.csv', help='Filename of output csv file.')
    parser.add_argument('--filetypes', type=str, default='wav,mp3', help='Audio filetypes to look out for. Separate by commas.')
    args = parser.parse_args()

    processor = SquimProcessor()
    filetypes = [ft for ft in args.filetypes.split(',')]
    estimates = estimate(args.audio_dir, args.recurse, filetypes)
    output_df = pd.DataFrame(estimates)
    output_df.to_csv(args.output_file, header=True, index=None)

    print(f'Report has been generated: {args.output_file}')
