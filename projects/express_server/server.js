const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

const projects = [
  {
    id: 1,
    name: 'Calculator',
    description: 'A simple calculator application for basic arithmetic operations.',
    technologies: ['JavaScript', 'HTML', 'CSS'],
    code: 'https://github.com/yourusername/vibe-coding-portfolio/tree/main/projects/calculator'
  },
  {
    id: 2,
    name: 'News Parser',
    description: 'A parser that extracts headlines, summaries, and links from news sources.',
    technologies: ['Python', 'BeautifulSoup', 'requests'],
    code: 'https://github.com/yourusername/vibe-coding-portfolio/tree/main/projects/news_parser'
  },
  {
    id: 3,
    name: 'Telegram Bot',
    description: 'A Telegram bot for simple chat interactions and automation.',
    technologies: ['Python', 'python-telegram-bot'],
    code: 'https://github.com/yourusername/vibe-coding-portfolio/tree/main/projects/telegram_bot'
  }
];

// Middleware для логирования запросов
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/projects', (req, res) => {
  res.json(projects);
});

app.get('/api/projects/:id', (req, res) => {
  const projectId = Number(req.params.id);
  const project = projects.find((item) => item.id === projectId);

  if (!project) {
    return res.status(404).json({ error: 'Project not found' });
  }

  res.json(project);
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
