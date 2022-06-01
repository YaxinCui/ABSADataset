
# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Introduction to the """

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
"""

_DESCRIPTION = """"""

_URL = "https://raw.githubusercontent.com/IsakZhang/XABSA/master/data/rest/gold-{lang}-{split}.txt"


class XABSAConfig(datasets.BuilderConfig):
    """BuilderConfig for """

    def __init__(self, **kwargs):
        """BuilderConfig .
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(XABSAConfig, self).__init__(**kwargs)


class XABSA(datasets.GeneratorBasedBuilder):
    """XABSA dataset."""

    BUILDER_CONFIGS = [
        XABSAConfig(name="en", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
        XABSAConfig(name="es", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
        XABSAConfig(name="fr", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
        XABSAConfig(name="ru", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
        XABSAConfig(name="nl", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
        XABSAConfig(name="tr", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
    ]
    
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ate_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "T-ASP",
                            ]
                        )
                    ),
                    "atepc_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "T-POS",
                                "T-NEU",
                                "T-NEG",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": _URL.format(split="train", lang=self.config.name),
            "dev": _URL.format(split="dev", lang=self.config.name),
            "test": _URL.format(split="train", lang=self.config.name),
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]
        
    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ate_tags = []
            atepc_tags = []
            for i, line in enumerate(f):
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ate_tags": ate_tags,
                            "atepc_tags": atepc_tags,
                        }
                        guid += 1
                        tokens = []
                        ate_tags = []
                        atepc_tags = []
                else:
                    # 
                    splits = line.split("\t")
                    token = splits[0]
                    atepc_tag = splits[1]
                    category = splits[2].rstrip()

                    tokens.append(token)
                    atepc_tags.append(atepc_tag)
                    if atepc_tag[0]=='O':
                        ate_tags.append('O')
                    else:
                        ate_tags.append(atepc_tag[0]+"-ASP")
            
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ate_tags": ate_tags,
                "atepc_tags": atepc_tags,
            }
