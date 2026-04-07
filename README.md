[README.md](https://github.com/user-attachments/files/26554082/README.md)
# CommandSearch

A cyberpunk-themed command-line interface application that provides quick access to streaming services, music platforms, social media, and AI tools. SignOpen combines a sleek neon aesthetic with practical functionality for seamless web navigation.

## Features

- **Movie Streaming**: Access to 80+ streaming platforms (Netflix, Disney+, Prime Video, HBO Max, Hulu, and more)
- **Music Platforms**: Quick links to popular music services (Spotify, Apple Music, YouTube Music, SoundCloud, etc.)
- **Social Media**: One-command login for major social platforms (Facebook, Twitter, Instagram, TikTok, Discord, etc.)
- **AI Tools**: Direct access to ChatGPT, Gemini, Claude, Copilot, and Perplexity
- **Cyberpunk UI**: Custom-designed neon-themed interface with scanline effects
- **Command-based Navigation**: Simple command syntax for quick access to services

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Matthew-Dam/SignOpen.git
cd SignOpen
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Interface (Recommended)
```bash
python frontend.py
```
or
```bash
python frontend2.py
```

### Command-Line Interface
```bash
python main.py
```
Then enter commands like:
- `open netflix` - Opens Netflix
- `open spotify` - Opens Spotify  
- `login instagram` - Opens Instagram login
- `search python tutorials` - Searches for the query

## Available Commands

### Media Access
- `open [service]` - Opens any streaming service (e.g., `open hulu`, `open youtube`)
- Available services include Netflix, Prime Video, Disney+, HBO Max, Spotify, SoundCloud, and many more

### Social Media Login
- `login [platform]` - Opens social media login page
- Supported platforms: Facebook, Twitter, Instagram, TikTok, LinkedIn, Discord, Reddit, WhatsApp, Telegram, and more

### Web Search
- Simply type any search query to search on Bing

## Project Structure

```
SignOpen/
├── main.py              # CLI interface
├── frontend.py          # Advanced cyberpunk GUI
├── frontend2.py         # Alternative GUI
├── cyber_terminal.py    # Terminal emulator component
├── movie_sites.py       # Movie/TV streaming services database
├── music_site.py        # Music platform services database
├── social_media.py      # Social media platform services database
├── ais.py              # AI tools database
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Architecture

- **Backend Modules**: Separate modules manage different service categories
- **Multiple Frontends**: Choose between CLI or GUI experiences
- **Extensible Design**: Easily add new services by updating the respective database files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for modern GUI components
- Cyberpunk aesthetic inspired by neon UI design trends

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/Matthew-Dam/SignOpen/issues) on GitHub.
