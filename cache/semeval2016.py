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
"""Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition"""

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{tjong-kim-sang-2002-introduction,
    title = "Introduction to the {C}o{NLL}-2002 Shared Task: Language-Independent Named Entity Recognition",
    author = "Tjong Kim Sang, Erik F.",
    booktitle = "{COLING}-02: The 6th Conference on Natural Language Learning 2002 ({C}o{NLL}-2002)",
    year = "2002",
    url = "https://www.aclweb.org/anthology/W02-2024",
}
"""

_DESCRIPTION = """\
Named entities are phrases that contain the names of persons, organizations, locations, times and quantities.
Example:
[PER Wolff] , currently a journalist in [LOC Argentina] , played with [PER Del Bosque] in the final years of the seventies in [ORG Real Madrid] .
The shared task of CoNLL-2002 concerns language-independent named entity recognition.
We will concentrate on four types of named entities: persons, locations, organizations and names of miscellaneous entities that do not belong to the previous three groups.
The participants of the shared task will be offered training and test data for at least two languages.
They will use the data for developing a named-entity recognition system that includes a machine learning component.
Information sources other than the training data may be used in this shared task.
We are especially interested in methods that can use additional unannotated data for improving their performance (for example co-training).
The train/validation/test sets are available in Spanish and Dutch.
For more details see https://www.clips.uantwerpen.be/conll2002/ner/ and https://www.aclweb.org/anthology/W02-2024/
"""

_URL = "https://raw.githubusercontent.com/yangheng95/ABSADatasets/v1.2/datasets/atepc_datasets/120.SemEval2016Task5/{split}/{domain}_{split}_{lang}.xml.dat.atepc"


class Conll2002Config(datasets.BuilderConfig):
    """BuilderConfig for Conll2002"""

    def __init__(self, **kwargs):
        """BuilderConfig forConll2002.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Conll2002Config, self).__init__(**kwargs)


class Conll2002(datasets.GeneratorBasedBuilder):
    """Conll2002 dataset."""

    BUILDER_CONFIGS = [
        Conll2002Config(name="es", version=datasets.Version("1.0.0"), description="SemEval 2016 dataset"),
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
                                "B-ASP",
                                "I-ASP",
                            ]
                        )
                    ),
                    "atepc_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-POS",
                                "I-POS",
                                "B-NEU",
                                "I-NEU",
                                "B-NEG",
                                "I-NEG",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/W02-2024/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": _URL.format(split="train", domain="restaurants", lang="spanish"),
#            "dev": _URL.format(split="", domain="restaurants", lang="spanish"),
            "test": _URL.format(split="train", domain="restaurants", lang="spanish"),
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
#            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
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
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
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
                    # conll2002 tokens are space separated
                    splits = line.split(" ")
                    token = splits[0]
                    ate_tag = splits[1]
                    pc_tag = splits[2].rstrip()

                    tokens.append(token)
                    ate_tags.append(ate_tag)

                    if pc_tag == "-999":
                        atepc_tags.append("O")
                    else:
                        # Negative, Neutral, Positive
                        atepc_tags.append(f"{ate_tag[0]}-{pc_tag[:3].upper()}")
            
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ate_tags": ate_tags,
                "atepc_tags": atepc_tags,
            }
