import tensorflow as tf
import json
import numpy as np
from pathlib import Path
from disease_treatements import get_treatment

BASE = Path(__file__).parent

# Load trained model
model = tf.keras.models.load_model(
    BASE / "phytobot_model.keras"
)

# Load disease names
with open(BASE / "class_names.json") as f:
    classes = json.load(f)

# Load test image
image = tf.keras.utils.load_img(
    BASE / "test_images" / "image.png",
    target_size=(224, 224)
)

image = tf.keras.utils.img_to_array(image)
image = np.expand_dims(image, axis=0)

# Prediction
prediction = model.predict(image)

index = np.argmax(prediction[0])
confidence = prediction[0][index] * 100

print("Predicted Disease:", classes[index])
print("Confidence:", round(float(confidence), 2), "%")
# Treatment recommendation
result = get_treatment(classes[index])

print("\n--- PHYTOBOT AI TREATMENT ---")
print("Status:", result["status"])
print("Symptoms:", result["symptoms"])
print("Treatment:", result["treatment"])
print("Prevention:", result["prevention"])