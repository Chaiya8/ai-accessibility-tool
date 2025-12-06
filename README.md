# LearnEasy – AI Accessibility Tool

## 📚 Project Overview

**LearnEasy** is an AI-powered accessibility tool designed to make complex educational content more understandable for learners of all levels. Using state-of-the-art natural language processing models, LearnEasy transforms difficult text into simpler, more digestible formats while maintaining accuracy and meaning.

### Key Features

- 🎯 **Text Simplification** – Reduce reading level complexity while preserving meaning
- 📝 **Text Summarization** – Condense lengthy content into concise summaries
- 💡 **Concept Explanation** – Generate detailed explanations for complex ideas
- 🔗 **Example Generation** – Provide real-world examples to illustrate concepts
- 🛣️ **Step Decomposition** – Break down processes into manageable steps
- 🔊 **Text-to-Speech** – Convert text to audio for multi-sensory learning
- 📊 **Process Visualization** – Create diagrams to visualize step-by-step processes

### Problem Statement

Many students and professionals struggle with understanding complex educational materials. LearnEasy bridges this gap by leveraging AI to adapt content to different reading levels and learning styles, promoting inclusive education and accessibility.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** – Interactive web interface for frontend
- **FastAPI** – RESTful backend API
- **Transformers (Hugging Face)** – Google FLAN-T5 model for NLP tasks
- **PyTorch** – Deep learning framework
- **gTTS** – Google Text-to-Speech for audio generation
- **Graphviz** – Diagram visualization

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Usage Instructions](#usage-instructions)
4. [API Documentation](#api-documentation)
5. [Code Examples](#code-examples)
6. [Contributing](#contributing)
7. [Acknowledgments](#acknowledgments)
8. [License](#license)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Chaiya8/ai-accessibility-tool.git
   cd ai-accessibility-tool
   ```

2. **Create a Virtual Environment** (Recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Pre-trained Models** (Automatic on first run)
   The FLAN-T5 model will be automatically downloaded when you first run the application.

---

## 📁 Project Structure

```
ai-accessibility-tool/
├── README.md                      # Project documentation
├── CONTRIBUTING.md                # Contribution guidelines
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
│
├── backend/                       # Backend API (FastAPI)
│   ├── main.py                   # API endpoints and routing
│   ├── simplify.py               # Core text transformation logic
│   ├── texttspeech.py            # Text-to-Speech conversion
│   └── diagram.py                # Diagram generation utilities
│
├── frontend/                      # Frontend (Streamlit)
│   └── streamlitapp.py           # Streamlit UI application
│
└── docs/                          # Documentation
    └── API_DOCUMENTATION.md       # Detailed API reference
```

---

## 💻 Usage Instructions

### Running the Frontend (Streamlit)

```bash
streamlit run frontend/streamlitapp.py
```

The application will open in your browser at `http://localhost:8501`

**How to Use:**

1. Paste your text in the input area
2. Select a transformation mode:
   - **Simplify** – Reduce text to a specific reading level
   - **Summarize** – Create a concise summary
   - **Explain10** – Generate a detailed explanation
   - **Example** – Get relevant examples
   - **Steps** – Decompose into process steps
3. Choose a reading level (for simplify mode)
4. Click "Transform" to process your text
5. View results and download audio if needed

### Running the Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

- Interactive API documentation: `http://localhost:8000/docs`

---

## 🔌 API Documentation

### Endpoints

#### 1. Text Transformation

**Endpoint:** `POST /transform`

**Request Body:**

```json
{
  "text": "Your complex text here",
  "mode": "simplify",
  "level": "6th grade"
}
```

**Mode Options:**

- `simplify` – Reduce reading level
- `summarize` – Condense content
- `explain10` – Generate explanation
- `example` – Create examples
- `steps` – Decompose into steps

**Reading Levels (for simplify):**

- `3rd grade`
- `5th grade`
- `6th grade`
- `8th grade`
- `High school`

**Response:**

```json
{
  "original": "Your complex text here",
  "transformed": "Simplified version of text",
  "mode": "simplify"
}
```

#### 2. Text-to-Speech

**Endpoint:** `POST /tts`

**Request Body:**

```json
{
  "text": "Text to convert to audio",
  "lang": "en"
}
```

**Response:**

```json
{
  "audio_base64": "base64_encoded_audio_data",
  "format": "mp3"
}
```

#### 3. Diagram Generation

**Endpoint:** `POST /diagram`

**Request Body:**

```json
{
  "text": "Step-by-step process description"
}
```

**Response:**

```json
{
  "diagram_svg": "SVG_diagram_code",
  "steps": ["step1", "step2", "step3"]
}
```

---

## 📖 Code Examples

### Example 1: Simple Text Simplification

```python
from backend.simplify import run_instruction

text = "Photosynthesis is the process by which plants convert light energy into chemical energy."
simplified = run_instruction(text, mode="simplify", level="3rd grade")
print(simplified)
# Output: "Plants use sunlight to make food."
```

### Example 2: Using the API

```python
import requests

url = "http://localhost:8000/transform"
payload = {
    "text": "The mitochondria is the powerhouse of the cell.",
    "mode": "simplify",
    "level": "5th grade"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Example 3: Text-to-Speech

```python
from backend.texttspeech import text_to_audio_base64

text = "Hello, this is LearnEasy"
audio_base64 = text_to_audio_base64(text, lang="en")
```

---

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)

### Reporting Issues

- Use the GitHub Issues tab to report bugs
- Provide a clear description and steps to reproduce
- Include your environment details (OS, Python version, etc.)

### Feature Requests

- Suggest improvements through GitHub Discussions
- Include use cases and expected behavior
- Reference relevant issues if applicable

---

## 🙏 Acknowledgments

- **Hugging Face** – For the Transformers library and FLAN-T5 model
- **Streamlit** – For the interactive web framework
- **Google** – For Google Text-to-Speech API
- **OpenAI and Anthropic** – For AI research and best practices

---

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

---
Team

Chaiya Emmanuel, Frank Lim, Bhoomika Gupta, Mathias  Beccera, Michael Acheampong,
---

## 🎯 Future Roadmap

- [ ] Multi-language support
- [ ] Mobile application
- [ ] Offline mode capability
- [ ] Custom model fine-tuning
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard

---

**Made with ❤️ for accessible education**
