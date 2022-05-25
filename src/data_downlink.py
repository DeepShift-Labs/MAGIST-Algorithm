import fiftyone as fo

dataset = fo.zoo.load_zoo_dataset(
              "open-images-v6",
              split="validation",
              label_types=["detections"],
              classes=["Cat", "Dog"],
              max_samples=100,
          )

patches = dataset.to_patches("detections")

# The `ground_truth` field has type `Detection`, but COCO format expects
# `Detections`, so the labels are automatically coerced to single-label lists
patches.export(
    export_dir="Data2",
    dataset_type=fo.types.TFObjectDetectionDataset,
    label_field="detections",
)



#PascalVOC

#-Data
# - Cats
# - Dogs