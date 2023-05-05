#!/usr/bin/env zsh

# Check if running on M1 Mac
if [[ "$(uname -m)" == "arm64" ]]; then
    # Install Rosetta 2 if not already installed
    if ! softwareupdate --history | grep -q "Rosetta"; then
        echo "Installing Rosetta 2..."
        sudo softwareupdate --install-rosetta
    else
        echo "Rosetta 2 is already installed."
    fi

    # Set Homebrew installation path for M1 Mac
    HOMEBREW_PREFIX="/opt/homebrew"
else
    HOMEBREW_PREFIX="/usr/local"
fi

# Install Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Add Homebrew to PATH
echo "eval \"\$(${HOMEBREW_PREFIX}/bin/brew shellenv)\"" >> ~/.zprofile
eval "\$(${HOMEBREW_PREFIX}/bin/brew shellenv)"

echo "Homebrew installation complete."
if [[ "$(uname -m)" == "arm64" ]]; then
    # Install ffmpeg
    /opt/homebrew/bin/brew install ffmpeg
    echo "ffmpeg installation complete."

    # Install Portaudio
    /opt/homebrew/bin/brew install portaudio
    echo "Portaudio installation complete."
else
    /usr/local/bin/brew install ffmpeg
    echo "ffmpeg installation complete."

    /usr/local/bin/brew install portaudio
    echo "Portaudio installation complete."
fi

