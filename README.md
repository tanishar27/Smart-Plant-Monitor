# 🌿 Smart Plant Monitor – Machine Learning Based Dashboard

## 📌 About the Project

Smart Plant Monitor is a machine learning-based plant monitoring project developed using Python and Streamlit.

The project includes a web-based dashboard that uses a trained machine learning model to process plant-related data and present the results through an interactive interface.

It includes a dataset, model training script, model testing script, and a pre-trained machine learning model.

The objective is to explore how machine learning can be used to support smarter and more efficient plant monitoring.

## 🎯 Objectives

- Develop a machine learning-based plant monitoring system.
- Train and test a machine learning model using plant-related data.
- Build an interactive dashboard using Streamlit.
- Present model outputs in an understandable format.
- Explore the use of AI and data science in smart agriculture.

## 🛠️ Technologies Used

- Python
- Machine Learning
- Streamlit
- Pandas
- Plotly
- Joblib
- Visual Studio Code

## ✨ Features

- Interactive web dashboard.
- Machine learning model integration.
- Plant-related dataset processing.
- Model training and testing scripts.
- Visual representation of data.
- Pre-trained model loading.

## 📂 Project Structure

```text
Smart-Plant-Monitor/
│
├── model/
│   └── plant_model.pkl
│
├── app.py
├── plant_data.csv
├── train_model.py
├── test_model.py
├── .gitignore
└── README.md
```

## ⚙️ How It Works

1. Plant-related data is stored in a CSV dataset.
2. The training script processes the data and trains the machine learning model.
3. The trained model is saved as a `.pkl` file.
4. The testing script is used to test the trained model.
5. The Streamlit application loads the model.
6. The dashboard presents the available plant monitoring information and results.

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/tanishar27/Smart-Plant-Monitor.git
```

### 2. Open the project folder

```bash
cd Smart-Plant-Monitor
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

Install the libraries used by the project scripts. For the dashboard, the main packages include:

```bash
pip install streamlit pandas plotly joblib scikit-learn
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧠 Model Training

To train the model again using the available dataset:

```bash
python train_model.py
```

To test the model:

```bash
python test_model.py
```

## 🔮 Future Improvements

- Real-time plant monitoring using IoT sensors.
- Integration with ESP32 hardware.
- Live soil moisture data visualization.
- Automated irrigation integration.
- Cloud-based plant monitoring.
- Improved machine learning models.

## 👩‍💻 Author

**Tanisha Rajpurohit**

B.Tech – Artificial Intelligence and Data Science

- GitHub: https://github.com/tanishar27
- LinkedIn: https://www.linkedin.com/in/tanisharajpurohit/
- X: https://x.com/tanisha_rp_x

---

⭐ If you find this project interesting, consider giving this repository a star!    