# conscious-canvas

Art Project for Camp Humans Being at Burning Man 2023

## Getting Started

1. Ensure that Python 3.10+ is installed. Newer versions of Python will probably work.
   ```
   python --version
   ```
1. Create a virtual env, activate it, and install this package with the `AR` environment variable
   ```
   pip -m venv venv
   source venv/bin/activate
   AR=/usr/bin/ar pip install -e .
   ```
1. Run the app:
   - For developing on a MacBook without Stable Diffusion, run in mock mode:
     ```
     MOCK_A1111=True ./run.sh
     ```
   - If running Stable Diffusion via A1111, run normally:
     ```
     ./run.sh
     ```
1. There are two entrypoints for the app:
   - The iPad sketching interface runs at http://localhost:8000 (left)
   - The projector display runs at http://localhost:8000/projection.html (right)
   ![Alt text](docs/dev_screenshot.png)

#### Random notes
- SSL localhost is necessary to get mic recording working on mobile Safari.
  - How to set up SSL localhost on Ubuntu: https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/