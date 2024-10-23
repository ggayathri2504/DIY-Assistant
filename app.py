import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io


def resize_image(image, max_size=800):
    """Resize image while maintaining aspect ratio"""
    ratio = max_size / max(image.size)
    if ratio < 1:  # Only resize if the image is larger than max_size
        new_size = tuple([int(dim * ratio) for dim in image.size])
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image


def compress_image(image, quality=85):
    """Compress image to reduce file size"""
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer


def encode_image(image_file):
    """Convert image to base64 with resizing and compression"""
    # Open image
    image = Image.open(image_file)

    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize image
    resized_image = resize_image(image)

    # Compress image
    compressed_buffer = compress_image(resized_image)

    # Convert to base64
    return base64.b64encode(compressed_buffer.getvalue()).decode("utf-8")


def analyze_diy_image(client, image_base64):
    system_prompt = """You are a DIY and crafts expert. When presented with an image, provide detailed building instructions in the following format:

Project Name: [name of the item]
Difficulty Level: [Beginner/Intermediate/Advanced]
Estimated Time: [time to complete]

Required Tools:
- [list all necessary tools]

Materials Needed:
- [list all materials with quantities]

Step-by-Step Instructions:
1. [detailed step]
2. [detailed step]
...

Safety Precautions:
- [list important safety measures]

Tips and Tricks:
- [helpful tips for better results]

Estimated Cost: [cost range in USD]"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                },
                {
                    "type": "text",
                    "text": system_prompt,
                },
            ],
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=messages,
            temperature=0.1,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


def main():
    st.set_page_config(page_title="DIY Project Assistant", page_icon="🛠️", layout="wide")

    # Load and display the Groq logo
    logo_image = Image.open("groq-logo.png")  # Uncomment and add your logo
    st.image(logo_image, width=200)

    st.title("🛠️ DIY Project Assistant")
    st.write(
        "Upload a photo of any furniture, craft, or DIY project to get detailed building instructions!"
    )

    # Add custom CSS for better styling
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 100%;
            height: 3em;
            margin-top: 1em;
        }
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1em 0;
        }
        .stMarkdown {
            text-align: justify;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # API Key input with improved instructions
    with st.expander("ℹ️ API Key Instructions", expanded=False):
        st.markdown(
            """
        1. Go to [Groq's website](https://groq.com) and sign up for an account
        2. Generate an API key from your dashboard
        3. Copy and paste the key below
        """
        )

    api_key = st.text_input("Enter your Groq API Key", type="password")

    if api_key:
        client = Groq(api_key=api_key)

        # Add image settings
        st.sidebar.markdown("### Image Settings")
        max_size = st.sidebar.slider("Max Image Size (pixels)", 400, 1200, 800, 100)
        quality = st.sidebar.slider("Image Quality", 50, 100, 85, 5)

        # Project type selection
        project_type = st.sidebar.selectbox(
            "Project Type",
            ["Furniture", "Home Decor", "Storage Solutions", "Crafts", "Other"],
            help="Select the type of project you're interested in",
        )

        # File uploader with clear instructions
        uploaded_file = st.file_uploader(
            "Upload a project image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit photo of the item you want to build",
        )

        if uploaded_file is not None:
            # Process and display images
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### Original Image")
                original_image = Image.open(uploaded_file)
                st.image(original_image, use_column_width=True)
                st.info(f"Original Size: {original_image.size}")

            with col2:
                st.markdown("### Processed Image")
                # Process image with current settings
                processed_image = resize_image(original_image, max_size)
                st.image(processed_image, use_column_width=True)
                st.info(f"Processed Size: {processed_image.size}")

            # Analyze button and results
            if st.button("🔨 Get Building Instructions"):
                with st.spinner("Analyzing your project..."):
                    # Convert image to base64 with current settings
                    processed_buffer = compress_image(processed_image, quality)
                    image_base64 = base64.b64encode(processed_buffer.getvalue()).decode(
                        "utf-8"
                    )

                    # Get analysis
                    analysis = analyze_diy_image(client, image_base64)

                    # Display results in a nice format
                    st.markdown("### 📋 Project Instructions")
                    st.write(analysis)

                    # Add download button for instructions
                    st.download_button(
                        label="📥 Download Instructions",
                        data=analysis,
                        file_name="diy_instructions.txt",
                        mime="text/plain",
                    )

                    # Add disclaimer in a warning box
                    st.warning(
                        "⚠️ Note: These instructions are AI-generated suggestions. Always prioritize safety and consult with experienced DIY enthusiasts or professionals when needed."
                    )

    else:
        st.info("👆 Please enter your Groq API key to get started.")

    # Add tips in an expander
    with st.expander("📝 Tips for Best Results", expanded=False):
        st.markdown(
            """
        ### Photography Tips:
        - Take photos in good lighting
        - Capture multiple angles if possible
        - Ensure the entire item is visible
        - Include size reference when possible
        - Use a clean, uncluttered background
        
        ### Project Documentation:
        - Note down any specific materials or finishes you prefer
        - Consider your skill level when choosing projects
        - Have basic tools ready before starting
        - Always prioritize safety equipment
        
        ### Image Settings:
        - Adjust the Max Image Size to balance quality and processing speed
        - Higher Image Quality means better detail but larger file size
        - For most project photos, the default settings work well
        """
        )

    # Add version info and credits
    st.markdown(
        """
    ---
    Made with ❤️ using Streamlit and Groq API | v1.0.0
    """
    )


if __name__ == "__main__":
    main()
