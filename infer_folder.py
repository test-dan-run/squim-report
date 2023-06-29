import glob
import argparse
import pandas as pd
from typing import List, Dict, Any

from squim import SquimProcessor

processor = SquimProcessor()

def estimate(audio_dir: str, recurse: bool = False) -> List[Dict[str, Any]]:

    if recurse:
        audio_filepaths = glob.glob(f'{audio_dir}/**/*.wav', recursive=True)
    else:
        audio_filepaths = glob.glob(f'{audio_dir}/*.wav')

    estimates = processor.estimate(audio_filepaths)

    results = []
    for fp, est in zip(audio_filepaths, estimates):
        out_dict = {'FILEPATH': fp}
        out_dict.update(est)
        results.append(out_dict)
    
    return results

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Estimate objective SQUIM values for audio files.')
    parser.add_argument('audio_dir', type=str, help='Directory to audio files.')
    parser.add_argument('--recurse', action='store_true')
    parser.add_argument('--output_file', type=str, default='squim_report.csv', help='Filename of output csv file.')
    args = parser.parse_args()

    estimates = estimate(args.audio_dir, args.recurse)
    output_df = pd.DataFrame(estimates)
    output_df.to_csv(args.output_file, header=True, index=None)

    print(f'Report has been generated: {args.output_file}')
