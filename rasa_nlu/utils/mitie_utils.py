from mitie import total_word_feature_extractor
from typing import Optional

from rasa_nlu.components import Component
from rasa_nlu.model import Metadata
import urllib

class MitieNLP(Component):

    name = "init_mitie"

    context_provides = {
        "pipeline_init": ["mitie_feature_extractor"],
    }

    def __init__(self, extractor=None):
        self.extractor = extractor

    @classmethod
    def cache_key(cls, model_metadata):
        # type: (Metadata) -> str

        return cls.name + "-" + str(model_metadata.metadata.get("mitie_feature_extractor_fingerprint"))

    def pipeline_init(self, mitie_file):
        # type: (str) -> dict
        print mitie_file
        if self.extractor is None:
            if "http" in mitie_file:
                url = mitie_file
                mitie_file = mitie_file.split('/')[-1]
                print mitie_file
                urllib.urlretrieve (url+"?dl=1", mitie_file)

            self.extractor = total_word_feature_extractor(mitie_file)
        MitieNLP.ensure_proper_language_model(self.extractor)
        return {"mitie_feature_extractor": self.extractor}

    @staticmethod
    def ensure_proper_language_model(extractor):
        # type: (Optional[mitie.total_word_feature_extractor]) -> None
        import mitie

        if extractor is None:
            raise Exception("Failed to load MITIE feature extractor. Loading the model returned 'None'.")

    def persist(self, model_dir):
        # type: (str) -> dict

        return {
            "mitie_feature_extractor_fingerprint": self.extractor.fingerprint
        }
