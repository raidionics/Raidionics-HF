import os

import gradio as gr

from .inference import run_model
from .utils import load_pred_volume_to_numpy
from .utils import load_to_numpy
from .utils import nifti_to_glb


class WebUI:
    def __init__(
        self,
        model_name: str = None,
        cwd: str = "/home/user/app/",
        share: int = 1,
    ):
        # global states
        self.images = []
        self.pred_images = []

        # @TODO: This should be dynamically set based on chosen volume size
        self.nb_slider_items = 512

        self.model_name = model_name
        self.cwd = cwd
        self.share = share

        self.class_name = "meningioma"  # default
        self.class_names = {
            "meningioma": "MRI_Meningioma",
            "lower-grade-glioma": "MRI_LGGlioma",
            "metastasis": "MRI_Metastasis",
            "glioblastoma": "MRI_GBM",
            "brain": "MRI_Brain",
        }

        self.result_names = {
            "meningioma": "Tumor",
            "lower-grade-glioma": "Tumor",
            "metastasis": "Tumor",
            "glioblastoma": "Tumor",
            "brain": "Brain",
        }

        # define widgets not to be rendered immediately, but later on
        self.slider = gr.Slider(
            minimum=1,
            maximum=self.nb_slider_items,
            value=1,
            step=1,
            label="Which 2D slice to show",
            interactive=True,
        )

        self.volume_renderer = gr.Model3D(
            clear_color=[0.0, 0.0, 0.0, 0.0],
            label="3D Model",
            visible=True,
            elem_id="model-3d",
        ).style(height=512)

    def set_class_name(self, value):
        print("Changed task to:", value)
        self.class_name = value

    def combine_ct_and_seg(self, img, pred):
        return (img, [(pred, self.class_name)])

    def upload_file(self, file):
        return file.name

    def process(self, mesh_file_name):
        path = mesh_file_name.name
        run_model(
            path,
            model_path=os.path.join(self.cwd, "resources/models/"),
            task=self.class_names[self.class_name],
            name=self.result_names[self.class_name],
        )
        nifti_to_glb("prediction.nii.gz")

        self.images = load_to_numpy(path)
        # @TODO. Dynamic update of the slider does not seem to work like this
        # self.nb_slider_items = len(self.images)
        # self.slider.update(value=int(self.nb_slider_items/2), maximum=self.nb_slider_items)

        self.pred_images = load_pred_volume_to_numpy("./prediction.nii.gz")
        return "./prediction.obj"

    def get_img_pred_pair(self, k):
        k = int(k) - 1
        # @TODO. Will the duplicate the last slice to fill up, since slider not adjustable right now
        if k >= len(self.images):
            k = len(self.images) - 1
        out = [gr.AnnotatedImage.update(visible=False)] * self.nb_slider_items
        out[k] = gr.AnnotatedImage.update(
            self.combine_ct_and_seg(self.images[k], self.pred_images[k]),
            visible=True,
        )
        return out

    def run(self):
        css = """
        #model-3d {
        height: 512px;
        }
        #model-2d {
        height: 512px;
        margin: auto;
        }
        #upload {
        height: 120px;
        }
        """
        with gr.Blocks(css=css) as demo:
            with gr.Row():
                file_output = gr.File(file_count="single", elem_id="upload")
                file_output.upload(self.upload_file, file_output, file_output)

                model_selector = gr.Dropdown(
                    list(self.class_names.keys()),
                    label="Segmentation task",
                    info="Select the preoperative segmentation model to run",
                    multiselect=False,
                    size="sm",
                )
                model_selector.input(
                    fn=lambda x: self.set_class_name(x),
                    inputs=model_selector,
                    outputs=None,
                )

                run_btn = gr.Button("Run segmentation").style(
                    full_width=False, size="lg"
                )
                run_btn.click(
                    fn=lambda x: self.process(x),
                    inputs=file_output,
                    outputs=self.volume_renderer,
                )

            with gr.Row():
                gr.Examples(
                    examples=[
                        os.path.join(self.cwd, "t1gd.nii.gz"),
                    ],
                    inputs=file_output,
                    outputs=file_output,
                    fn=self.upload_file,
                    cache_examples=True,
                )

            with gr.Row():
                with gr.Box():
                    with gr.Column():
                        image_boxes = []
                        for i in range(self.nb_slider_items):
                            visibility = True if i == 1 else False
                            t = gr.AnnotatedImage(
                                visible=visibility, elem_id="model-2d"
                            ).style(
                                color_map={self.class_name: "#ffae00"},
                                height=512,
                                width=512,
                            )
                            image_boxes.append(t)

                        self.slider.input(
                            self.get_img_pred_pair, self.slider, image_boxes
                        )

                        self.slider.render()

                with gr.Box():
                    self.volume_renderer.render()

        # sharing app publicly -> share=True:
        # https://gradio.app/sharing-your-app/
        # inference times > 60 seconds -> need queue():
        # https://github.com/tloen/alpaca-lora/issues/60#issuecomment-1510006062
        demo.queue().launch(
            server_name="0.0.0.0", server_port=7860, share=self.share
        )
