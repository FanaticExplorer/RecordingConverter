# 🎥 OBS Recording Converter

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![OBS Studio](https://img.shields.io/badge/OBS_Studio-28.0+-blue)](https://obsproject.com/)
[![My page](https://img.shields.io/badge/My_Page-000000?style=flat&logo=bento&logoColor=white)](https://bento.me/fanaticexplorer)

An advanced OBS Studio plugin that automatically converts recordings and replays using FFmpeg with customizable settings.

## Why Choose This Plugin?  

While OBS includes a basic remux function, our plugin offers superior features:  

✅ **Extended Format Support** (MP4, MOV, AVI, FLV, TS)  
✅ **Custom FFmpeg Parameters** for precise encoding control  
✅ **Flexible File Management** (keep or delete originals automatically)  
✅ **Dual Functionality** - Works with both recordings AND replay buffer  
✅ **Optimized Performance** with throttled progress updates  
✅ **Efficient Output** - Produces smaller files compared to standard remuxing  

## ⚡ Quick Installation Guide  

1. **Download these from [Releases](https://github.com/FanaticExplorer/RecordingConverter/releases):**  
   - `RecordingConventer.py` (the plugin)  
   - `Python311.zip` (portable Python)   

2. **Install Python:**  
   - Unzip the Python folder anywhere (e.g., `C:\Python311`)
   - **Alternative Option**: You can also install Python directly from the [official website](https://www.python.org/downloads/release/python-3110/) if you prefer. The provided portable version is simply a convenience for quick setup. Be sure to download version 3.11 specifically, since that's the last version supported by OBS.

3. **Set up Python in OBS:**  
   - Open OBS Studio → Tools → Scripts  
   - Go to "Python Settings" tab  
   - Set "Python Install Path (64bit)" to your Python folder  

4. **Add the plugin:**  
   - In the "Scripts" tab, click "+" and select `RecordingConventer.py`  

5. **Install FFmpeg (see guide below)**  

6. **🌟 Profit! Configure the plugin to your needs**  

## 📥 FFmpeg Installation
1. Download FFmpeg from [official site](https://ffmpeg.org/download.html)  
2. Unzip anywhere  
3. Either:  
   - Add FFmpeg to PATH (recommended), **OR**  
   - Set the FFmpeg path in plugin settings

## 💖 Support the Developer

If you find this plugin useful, consider supporting my work:

[![Buy me a coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/FanaticExplorer)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/FanaticExplorer)
[![Monobank Card](https://img.shields.io/badge/Monobank_Card-000000?style=flat&logo=visa&logoColor=white)](https://send.monobank.ua/3KAPtPvd4a)

You can also support me with cryptocurrency:

**Binance Pay ID:** `780389392`

[![Binance Pay QR code](https://img.shields.io/badge/Binance_Pay_QR_code-F0B90B?style=flat&logo=binance&logoColor=black)](https://i.imgur.com/WEYYdTn.png)

**Direct Wallet Addresses:**
- **BTC:** `1ksLDnSTekh9kdQcgeqtbdZtxKuLtDobC`
- **ETH (ERC20):** `0xef174683a9ca0cc6065bb8de433188bb1767b631`
- **USDT (TRC20):** `TC3SSLB1cyD1PEugufHF5zUv3sVpFhCi7z`
- **SOL (Solana):** `4ZZhbfJMevkg3x9W8KQiBsdFLz5NAkKMm7takXi2Lz8i`

Every donation helps me create and maintain more useful tools!

## License

MIT © [FanaticExplorer](https://github.com/FanaticExplorer)
