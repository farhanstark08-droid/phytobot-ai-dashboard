AI MODEL SETUP
1. Train a CNN model for the exact crop and disease classes you want to detect.
2. Save the Keras model as: models/leaf_disease_model.keras
3. Add models/labels.json as a JSON array in the same class order as the model outputs.
   Example: ["Healthy", "Early Blight", "Late Blight"]
4. Install a compatible TensorFlow version for your computer.
Without this trained model, the dashboard receives images automatically but correctly reports
"AI model not configured" instead of inventing a disease prediction.
The included Flask code resizes images to 224x224 and scales pixels to 0..1.
Your model must use the same preprocessing and class order.
