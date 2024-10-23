🛠️ DIY Project Assistant
A Streamlit-powered web application that uses Groq's Vision API to analyze images of furniture, crafts, or DIY projects and provide detailed building instructions, required tools, and materials.
Show Image
🌟 Features

📷 Upload and analyze images of DIY projects
🔧 Get detailed building instructions and materials list
⚙️ Automatic image optimization and processing
📊 Project difficulty assessment and time estimates
💰 Cost estimates for materials
🔍 Multiple project type support
📱 Responsive design for mobile and desktop

🚀 Getting Started
Prerequisites

Python 3.8 or higher
Groq API key (Get one here)
Git (for cloning the repository)

Installation

Clone the repository:

bashCopygit clone https://github.com/yourusername/diy-project-assistant.git
cd diy-project-assistant

Create a virtual environment (optional but recommended):

bashCopypython -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

Install required packages:

bashCopypip install -r requirements.txt
Running the App

Start the Streamlit app:

bashCopystreamlit run app.py

Open your browser and go to http://localhost:8501

📝 Usage

Enter your Groq API key in the designated field
Select project type from the sidebar
Upload an image of the DIY project you want to build
Adjust image settings if needed
Click "Get Building Instructions"
Review the generated instructions and download them if desired

🎯 Example Projects
The app can analyze various types of DIY projects:

Furniture (tables, chairs, shelves)
Home Decor (wall art, planters)
Storage Solutions (organizers, boxes)
Crafts (jewelry, decorations)
And more!

⚙️ Configuration
Image Settings

Max Image Size: 400-1200 pixels (default: 800)
Image Quality: 50-100% (default: 85)
Supported formats: JPG, JPEG, PNG

Project Types

Furniture
Home Decor
Storage Solutions
Crafts
Other

🔒 Security

API keys are handled securely and never stored
Images are processed locally before being sent to the API
All communication with Groq API is encrypted

📸 Tips for Best Results

Image Quality:

Use well-lit photos
Capture multiple angles
Keep the background clean
Include size references


Project Selection:

Consider your skill level
Check required tools availability
Review safety precautions

💡 Acknowledgments

Built with Streamlit
Powered by Groq API
Image processing by Pillow

👥 Authors

Gayathri G - @ggayathri2504
