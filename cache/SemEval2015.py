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

"""The SemEval2015 Task12 Reviews Corpus"""

import datasets

_CITATION = """\
@inproceedings{pontiki2015semeval,
  title={Semeval-2015 task 12: Aspect based sentiment analysis},
  author={Pontiki, Maria and Galanis, Dimitrios and Papageorgiou, Harris and Manandhar, Suresh and Androutsopoulos, Ion},
  booktitle={Proceedings of the 9th international workshop on semantic evaluation (SemEval 2015)},
  pages={486--495},
  year={2015}
}
"""

_LICENSE = """\
    Please click on the homepage URL for license details.
"""

_DESCRIPTION = """\
A collection of SemEval2015 specifically designed to aid research in Aspect Based Sentiment Analysis.
"""

_CONFIG = [
    # restaruants Domain
    "restaurants",
    # Consumer Electronics Domain
    "laptops"
]

_VERSION = "0.0.1"

_HOMEPAGE_URL = "https://alt.qcri.org/semeval2015/task12/index.php?id=data-and-tools/"
_DOWNLOAD_URL = "https://raw.githubusercontent.com/YaxinCui/ABSADataset/main/SemEval2015Task12/{split}/{domain}_{split}.xml"


class SemEval2015Config(datasets.BuilderConfig):
    """BuilderConfig for SemEval2015Config."""

    def __init__(self, _CONFIG, **kwargs):
        super(SemEval2015Config, self).__init__(version=datasets.Version(_VERSION, ""), **kwargs),
        self.configs = _CONFIG


class SemEval2015(datasets.GeneratorBasedBuilder):
    """The lingual Amazon Reviews Corpus"""

    BUILDER_CONFIGS = [
        SemEval2015Config(
            name="All",
            _CONFIG=_CONFIG,
            description="A collection of SemEval2015 specifically designed to aid research in lingual Aspect Based Sentiment Analysis.",
        )
    ] + [
        SemEval2015Config(
            name=config,
            _CONFIG=[config],
            description=f"{config} of SemEval2015 specifically designed to aid research in lingual Aspect Based Sentiment Analysis",
        )
        for config in _CONFIG
    ]
    
    BUILDER_CONFIG_CLASS = SemEval2015Config
    DEFAULT_CONFIG_NAME = "All"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {'text': datasets.Value(dtype='string'),
                'opinions': [
                    {'category': datasets.Value(dtype='string'),
                    'from': datasets.Value(dtype='string'),
                    'polarity': datasets.Value(dtype='string'),
                    'target': datasets.Value(dtype='string'),
                    'to': datasets.Value(dtype='string')}
                ],
                'domain': datasets.Value(dtype='string'),
                'reviewId': datasets.Value(dtype='string'),
                'sentenceId': datasets.Value(dtype='string')
            }
            ),
            supervised_keys=None,
            license=_LICENSE,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        
        train_urls = [_DOWNLOAD_URL.format(split="train", domain=config) for config in self.config.configs]
        dev_urls = [_DOWNLOAD_URL.format(split="trial", domain=config) for config in self.config.configs]
        test_urls = [_DOWNLOAD_URL.format(split="test", domain=config) for config in self.config.configs]

        train_paths = dl_manager.download_and_extract(train_urls)
        dev_paths = dl_manager.download_and_extract(dev_urls)
        test_paths = dl_manager.download_and_extract(test_urls)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"file_paths": train_paths, "domain_list": self.config.configs}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"file_paths": dev_paths, "domain_list": self.config.configs}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"file_paths": test_paths, "domain_list": self.config.configs}),
        ]

    def _generate_examples(self, file_paths, domain_list):
        row_count = 0
        assert len(file_paths)==len(domain_list)

        for i in range(len(file_paths)):
            file_path, domain = file_paths[i], domain_list[i]
            semEvalDataset = SemEvalXMLDataset(file_path, domain)

            for example in semEvalDataset.SentenceWithOpinions:

                yield row_count, example
                row_count += 1


# 输入：xlm文件的文件路径
# 输出：一个DataSet，每个样例包含[reviewid, sentenceId, text, UniOpinions]
#      每个样例包含的Opinion，是一个列表，包含的是单个Opinion的详情

from xml.dom.minidom import parse

class SemEvalXMLDataset():
    def __init__(self, file_name, domain):
        # 获得SentenceWithOpinions，一个List包含(reviewId, sentenceId, text, Opinions)

        self.SentenceWithOpinions = []
        self.xml_path = file_name

        self.sentenceXmlList = parse(self.xml_path).getElementsByTagName('sentence')

        for sentenceXml in self.sentenceXmlList:
            reviewId = sentenceXml.getAttribute("id").split(':')[0]
            sentenceId = sentenceXml.getAttribute("id")
            if len(sentenceXml.getElementsByTagName("text")[0].childNodes) < 1:
                # skip no reviews part
                continue
            text = sentenceXml.getElementsByTagName("text")[0].childNodes[0].nodeValue
            OpinionXmlList = sentenceXml.getElementsByTagName("Opinion")
            Opinions = []
            for opinionXml in OpinionXmlList:
                # some text maybe have no opinion
                target = opinionXml.getAttribute("target")
                category = opinionXml.getAttribute("category")
                polarity = opinionXml.getAttribute("polarity")
                from_ = opinionXml.getAttribute("from")
                to = opinionXml.getAttribute("to")

                opinionDict = {
                    "target": target,
                    "category": category,
                    "polarity": polarity,
                    "from": from_,
                    "to": to
                }
                Opinions.append(opinionDict)
                
            Opinions.sort(key=lambda x: x["from"])
            # 从小到大排序

            self.SentenceWithOpinions.append({
                    "text": text, 
                    "opinions": Opinions, 
                    "domain": domain, 
                    "reviewId": reviewId, 
                    "sentenceId": sentenceId
                    }
                )