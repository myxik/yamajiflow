# 🌊 JYFlow

> Your personalized AI-powered research companion that keeps you surfing the wave of scientific discovery.

JYFlow is a lightweight CLI tool that transforms how you stay updated with academic research. It curates and summarizes arXiv papers based on your interests, powered by state-of-the-art language models and semantic search.

## ✨ Features

- 🎯 **Interest-Based Filtering**: Automatically finds papers that match your research interests using embedding similarity
- 🤖 **AI-Powered Summaries**: Generates concise, intelligent summaries of complex research papers
- 📅 **Time-Aware**: Filter papers by date to catch up on recent developments
- 🎨 **Neat Reports**: Generates clean, markdown-formatted research digests
- 📦 **Package**: Easy to install with PyPI, Poetry or Docker

## 🚀 Quick Start

There are couple of ways to use JyFlow. Most obvious is PyPI package, but you can also install it with Poetry or Docker. We try to provide all options for different use cases.

### Install with PyPI

```bash
pip install jyflow
```

### Install with Poetry

```bash
poetry install
```

### Set your OpenAI API key

```bash
export OPENAI_API_KEY="your-api-key"
```

### Generate summaries for today's papers

```bash
jyflow generate summaries --interests "quantum computing, machine learning" --k 10
```


## 💡 Why JYFlow?

JYFlow was born from a personal need to stay informed without getting overwhelmed (with tons of LLM research going here and there). It's designed to be simple yet powerful, helping researchers and enthusiasts alike to:

- Save hours of manual paper scanning
- Never miss relevant research in your field
- Get quick insights into complex papers
- Build a curated research feed
- Focus on what's important

## 🛠 Technical Stack

- Python 3.9+
- OpenAI API for intelligent summarization
- FAISS for efficient similarity search
- arXiv API for paper retrieval
- Poetry for dependency management

## 🤝 Contributing

JYFlow is an open-source project built with love for the research community. Contributions, suggestions, and feedback are always welcome! Feel free to:

- Open an issue
- Submit a PR
- Share your use case
- Suggest improvements

## 📝 License

MIT

---

Built with researchers by an engineer.