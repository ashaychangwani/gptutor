import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from datasets import load_dataset, Dataset, Audio

model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")


# ds = load_dataset("hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
ds = Dataset.from_dict({"audio":["Lecture Recordings 2/GMT20221212-215516_Recording.wav"]}).cast_column("audio", Audio())

inputs = processor(ds[0]["audio"]["array"], sampling_rate=ds[0]["audio"]["sampling_rate"], return_tensors="pt")
print("reached here")
generated_ids = model.generate(inputs["input_features"], attention_mask=inputs["attention_mask"])
print("reached here2")

transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
print("done")