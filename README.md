# Loratty BBS (In Active Development - Not Ready For Use!)

A modern Bulletin Board System (BBS) implementation built with Python.

## Features

- Modular architecture with plugins
- Configurable transport layer
- Event-driven core
- Admin interface
- Storage abstraction

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/loratty-bbs.git
   cd loratty-bbs
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

## Configuration

Edit `config/loratty.yaml` to configure the BBS settings.

## Running

```bash
python -m loratty.main
```

## Project Structure

- `loratty/core/` - Core system components
- `loratty/bbs/` - BBS-specific functionality
- `loratty/admin/` - Administrative tools
- `loratty/plugins/` - Plugin system
- `loratty/storage/` - Data storage abstraction
- `loratty/utils/` - Utility functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
