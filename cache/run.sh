# Copyright 2020 The HuggingFace Team. All rights reserved.
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
seed=42

#   --validation_split_percentage 5 \
#   --evaluation_strategy epoch \

python3 run_ate.py \
  --model_name_or_path microsoft/deberta-v3-small \
  --dataset_name semeval2016.py \
  --output_dir ./test-ate \
  --num_train_epochs 10 \
  --seed=${seed} \
  --save_strategy no \
  --label_all_tokens False \
  --return_entity_level_metrics False \
  --load_best_model_at_end True \
  --metric_for_best_model eval_f1 \
  --do_train \
  --do_eval True \
  --do_predict