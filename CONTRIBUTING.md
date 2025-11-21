# Contributing to Chess with AI

Thank you for your interest in contributing to this project. The guidelines below outline how to contribute effectively.

## How to Contribute

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/your-feature-name`)  
3. Implement your changes  
4. Test thoroughly  
5. Commit (`git commit -m "Describe your change"`)  
6. Push (`git push origin feature/your-feature-name`)  
7. Open a Pull Request  

## Code Style

- Follow PEP 8  
- Use clear variable and function names  
- Add comments for non-trivial chess logic  
- Keep functions focused and readable  

## Reporting Bugs

Include:
- Operating system  
- Python version  
- Pygame version  
- Steps to reproduce  
- Expected vs actual behavior  
- Any errors or screenshots  

## Feature Suggestions

Before suggesting:
- Check existing issues  
- Describe the feature and its value  
- Consider scope and alignment with the project  

## Development Setup

```bash
git clone https://github.com/KrishAtGit/ChessWithAI---Python.git
cd ChessWithAI---Python
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python chess_game.py
