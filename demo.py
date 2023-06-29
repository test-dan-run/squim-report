import gradio as gr
from typing import Tuple
from squim import SquimProcessor

processor = SquimProcessor()

def estimate(audio_filepath: str) -> Tuple[str]:

    estimates = processor.estimate(audio_filepath)

    return tuple(estimates.values())

with gr.Blocks() as demo:
    gr.HTML(
        """
            <div style="text-align: center; max-width: 700px; margin: 0 auto;">
            <div
                style="
                display: inline-flex;
                align-items: center;
                gap: 0.8rem;
                font-size: 1.75rem;
                "
            >
                <h1 style="font-weight: 900; margin-bottom: 7px; line-height: normal;">
                TorchAudio-SQUIM Objective
                </h1>
            </div>
            <p style="margin-bottom: 10px; font-size: 94%">
                [STOI] [PESQ] [SI-SDR]
            </p>
            </div>
        """
    )

    with gr.Row(equal_height=False):
        with gr.Column():
            audio_input = gr.Audio(label='Input', type='filepath', visible=True)
            audio_btn = gr.Button(value='Estimate')
        with gr.Column():
            stoi_output = gr.Textbox(label='STOI')
            pesq_output = gr.Textbox(label='PESQ')
            sdr_output = gr.Textbox(label='SI-SDR')

    audio_btn.click(estimate, inputs=audio_input, outputs=[stoi_output, pesq_output, sdr_output])

if __name__ == '__main__':
    demo.launch(
        server_name='0.0.0.0',
        server_port=8080,
        enable_queue=True,
    )