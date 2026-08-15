# Toxic Comment Detection

## 📌 Project Overview

Toxic Comment Detection is a Natural Language Processing (NLP) project that automatically identifies toxic and harmful comments in text. The system uses a deep learning model to classify user comments and can be integrated into web applications for real-time toxicity detection.

The project is designed to help identify inappropriate online content and support safer and more respectful digital communication.

## 🎯 Objectives

* Detect toxic comments automatically.
* Classify text using a trained deep learning model.
* Provide a simple web interface for entering comments.
* Reduce the need for manual moderation.
* Demonstrate the application of NLP and deep learning in content moderation.

## 🧠 Technologies Used

* **Python**
* **PyTorch**
* **Natural Language Processing (NLP)**
* **HTML**
* **CSS**
* **JavaScript**
* **Flask**
* **Git & GitHub**

## 🏗️ Project Structure

```text
Toxic_comment_detection/
│
├── datasets/
│   └── test.csv
│
├── model/
│   └── model_state_dict.pth
│
├── models/
│   └── tokenizer/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** The trained model weights are not included in the GitHub repository because the model file exceeds GitHub's standard 100 MB file-size limit.

## ⚙️ How the System Works

The overall workflow is:

```text
User Input
    ↓
Text Preprocessing
    ↓
Tokenization
    ↓
Deep Learning Model
    ↓
Toxicity Prediction
    ↓
Result Display
```

The user enters a comment through the web interface. The text is processed and converted into the required model input format. The trained deep learning model then analyzes the comment and produces the corresponding prediction.

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sddeepika06/toxic_comment_prediction.git
```

### 2. Navigate to the project directory

```bash
cd toxic_comment_prediction
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install the required dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Run:

```bash
python app.py
```

The application will start locally. Open the URL displayed in the terminal in your web browser.

## 📊 Dataset

The project uses a toxic-comment dataset containing text comments and their corresponding toxicity labels.

The dataset is used for training/testing the deep learning model and evaluating its ability to identify toxic content.

## 🤖 Model

A trained deep learning model is used for toxic comment classification.

The trained model weights are approximately 253 MB and are therefore excluded from this GitHub repository to comply with GitHub's standard file-size restriction.

The model can be hosted separately using a suitable model-storage platform such as Hugging Face Hub or Git LFS.

## 💡 Applications

This system can be used in:

* Social media platforms
* Online discussion forums
* Educational platforms
* Gaming communities
* Chat applications
* Online comment moderation systems

## 🔮 Future Enhancements

* Add multi-class toxicity classification.
* Improve model accuracy using transformer-based architectures.
* Deploy the application using cloud platforms.
* Host the trained model separately.
* Add real-time moderation.
* Provide confidence scores for predictions.
* Support multiple languages.

## 👩‍💻 Author

**Deepika Devaraj**

B.Tech Artificial Intelligence and Data Science

## 📄 License

This project is created for educational and academic purposes.
