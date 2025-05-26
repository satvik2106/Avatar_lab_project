from phonemizer import phonemize

def test_phonemizer(language_code: str, text: str):
    try:
        output = phonemize(text, language=language_code, backend='espeak', strip=True)
        print(f"Phonemizer output for language '{language_code}': {output}")
        return True
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test phonemizer setup with Hindi text
    language_code = "hi"
    text = "नमस्ते दुनिया"
    success = test_phonemizer(language_code, text)
    if success:
        print("Phonemizer is correctly installed and configured.")
    else:
        print("Phonemizer setup failed. Please ensure eSpeak NG is installed and environment variables are set.")
