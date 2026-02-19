# PyCrawl-Wordlist 🕷️

Hi there! This is my first "serious" project developing tools in Python. I built this while studying at **HackTheBox Academy** to automate a common pentesting task: crawling a website to generate custom wordlists for brute-force attacks.

Since I am still learning, any feedback, optimization tips, or corrections are more than welcome!

## ✨ Features
- **Iterative Crawling:** Navigates through internal links with configurable depth.
- **Scope Control:** Stays within the target domain to avoid external noise.
- **Password Mutation:** Automatically generates variants (e.g., `Word2026!`, `wORD123`) to increase wordlist effectiveness.
- **Custom Filters:** Filters words by minimum length to keep the list clean.

## 🛠️ Installation & Usage

1. Clone the repository:
	```bash
	git clone https://github.com/Syd0z/PyCrawl-Wordlist.git
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Run the tool:
	```bash
	python vuln_test.py -u http://target.htb -d 1 -l 5 --mutate -o wordlist.txt
	```

## Disclaimer
This script was developed for educational purposes and for use in controlled environments (CTFs, labs). I am not responsible for any misuse of this tool against unauthorized targets.
