from typing import Tuple
from squim import SquimProcessor
import argparse

processor = SquimProcessor()

def estimate(audio_filepath: str) -> Tuple[str]:

    estimates = processor.estimate(audio_filepath)

    return estimates[0]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Estimate objective SQUIM values for an audio file.')
    parser.add_argument('audio_filepath', type=str, help='Absolute path to an audio file.')
    args = parser.parse_args()

    print(f'[{args.audio_filepath}] SQUIM scores:', estimate(args.audio_filepath))
