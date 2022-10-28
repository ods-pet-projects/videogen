import torch
import clip
import numpy as np
from PIL import Image
from typing import List


class ClipEmbedder:
    def __init__(self, clip_model_name='ViT-B/32', device='cpu'):
        self.device = device
        self.predictor, self.preprocess = clip.load(clip_model_name, device=device)

    def _tonumpy(self, tensor: torch.Tensor) -> np.ndarray:
        return tensor.cpu().detach().numpy()

    def encode_text(self, text: str) -> np.ndarray:
        with torch.no_grad():
            # Encode it to a feature vector using CLIP
            text_latent = self.predictor.encode_text(clip.tokenize(text).to(self.device))
            text_latent /= text_latent.norm(dim=-1, keepdim=True)

        return self._tonumpy(text_latent)

    def encode_imgs(self, pil_imgs: List[Image.Image]) -> np.ndarray:
        # Preprocess all photos
        photos_preprocessed = torch.stack([self.preprocess(photo) for photo in pil_imgs]).to(self.device)

        with torch.no_grad():
            # Encode the photos batch to compute the feature vectors and normalize them
            img_latents = self.predictor.encode_image(photos_preprocessed)
            img_latents /= img_latents.norm(dim=-1, keepdim=True)

        return self._tonumpy(img_latents)
