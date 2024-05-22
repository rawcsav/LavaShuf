from ultralytics import YOLO
from tqdm import tqdm
import torch

def load_model(checkpoint_path=None):
    if checkpoint_path:
        model = YOLO(checkpoint_path)
    else:
        model = YOLO('yolov8n.yaml')  # or use a larger model like 'yolov8s.yaml'
    return model

def train_model(model, data_yaml, epochs=100, batch_size=16, img_size=640, workers=4, amp=True,
                augment=True, lr0=0.001, val=True, save_period=10):
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        workers=workers,
        amp=amp,
        augment=augment,
        lr0=lr0,
        val=val,
        save_period=save_period
    )
    return results

def main():
    # Set the paths
    data_yaml = 'dataset_extended/data.yaml'
    last_checkpoint = 'train2/weights/last.pt'  # Replace with the path to your last checkpoint

    # Load the model
    if last_checkpoint:
        model = load_model(last_checkpoint)
    else:
        model = load_model()

    # Train the model
    train_results = train_model(
        model=model,
        data_yaml=data_yaml,
        epochs=100,
        batch_size=16,
        img_size=640,
        workers=4,
        amp=True,
        augment=True,
        lr0=0.001,
        val=True,
        save_period=10
    )

    # Print the training results
    print(train_results)

if __name__ == '__main__':
    main()