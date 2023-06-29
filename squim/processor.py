import torch
import torchaudio
from torchaudio._internal import load_state_dict_from_url
from torchaudio.prototype.pipelines import SQUIM_OBJECTIVE as bundle
from torchaudio.prototype.models import SquimObjective, squim_objective_base

from tqdm import tqdm
from typing import List, Dict, Union, Optional

METRICS = ('STOI', 'PESQ', 'SI-SDR')

class SquimProcessor:
    def __init__(self, model_path: Optional[str] = None, sr: int = 16000):
        '''Constructor for SquimProcessor
        
        Args:
            model_path (str): Absolute path to a SQUIM_OBJECTIVE model file.
        
        '''
        if model_path:
            self.model = self._load_model_from_path(model_path)
            self.target_sr = sr
        else:
            self.model = bundle.get_model()
            self.target_sr = bundle.sample_rate

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)

    def _load_model_from_path(self, model_path: str) -> SquimObjective:
        '''Load model from an absolute path.
        
        Args:
            model_path (str): Absolute path to a SQUIM_OBJECTIVE model file.
        
        '''
        state_dict = load_state_dict_from_url(model_path)
        model = squim_objective_base()
        model.load_state_dict(state_dict)
        model.eval()

        return model

    def load_audio(self, audio_filepath: str) -> torch.Tensor:
        '''Load input audio file as a torch tensor.

        Args:
            audio_filepath (str): Absolute path to the target audio file.
        
        Returns:
            torch.Tensor: waveform as a tensor of shape (1, num_samples)
        
        '''
        waveform, sr = torchaudio.load(audio_filepath)
        # convert multichannel audio to mono
        waveform = torch.mean(waveform, dim=0, keepdim=True)
        # resample audio to expected sample rate
        waveform = torchaudio.functional.resample(waveform, sr, self.target_sr)

        return waveform.to(self.device)

    def estimate_single(self, audio_filepath: str) -> Dict[str, float]:
        '''Generate the SQUIM estimates of a single audio file.

        Args:
            audio_filepath (str): Absolute path to the target audio file.
        
        Returns:
            Dict[str, float]: dictionary containing the estimates for each metric.
                i.e. {'STOI': xxx, 'PESQ': yyy, 'SI-SDR': zzz}

        '''
        waveform = self.load_audio(audio_filepath)
        with torch.no_grad():
            scores = self.model(waveform)
        
        return {metric:round(score.item(), 3) for metric, score in zip(METRICS, scores)}

    def estimate_multi(self, audio_filepaths: List[str]) -> List[Dict[str, float]]:
        '''Generate the SQUIM estimates of multiple audio files.

        Args:
            audio_filepaths (List[str]): List of absolute paths to the target audio files.
        
        Returns:
            List[Dict[str, float]]: dictionary containing the estimates for each metric.
                i.e. [{'STOI': xxx, 'PESQ': yyy, 'SI-SDR': zzz}, ...]

        '''
        results = []
        for audio_filepath in tqdm(audio_filepaths, total=len(audio_filepaths)):
            results.append(self.estimate_single(audio_filepath))

        return results
    
    def estimate(self, audio_filepaths: Union[List[str], str]) -> List[Dict[str, float]]:
        '''Core calling method to divert to single/multi estimate methods.
        
        Returns:
            List[Dict[str, float]]: dictionary containing the estimates for each metric.
                i.e. [{'STOI': xxx, 'PESQ': yyy, 'SI-SDR': zzz}, ...]
        '''

        if type(audio_filepaths) is str:
            return [self.estimate_single(audio_filepaths),]
        else:
            return self.estimate_multi(audio_filepaths)
