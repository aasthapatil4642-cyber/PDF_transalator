import streamlit as st
from groq import Groq
from pypdf import PdfReader


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI PDF Translator",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# Groq Client
# --------------------------------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# --------------------------------------------------
# Title and Description
# --------------------------------------------------

st.title("📄 AI PDF Translator")

st.write(
    "Upload a PDF document, select your target language, "
    "and translate the document using AI."
)


# --------------------------------------------------
# File Uploader
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)


# --------------------------------------------------
# Language Selection
# --------------------------------------------------

languages = [
    "English",
    "Hindi",
    "Marathi",
    "Gujarati",
    "Bengali",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Punjabi",
    "French",
    "German",
    "Spanish",
    "Italian",
    "Japanese",
    "Korean",
    "Chinese",
    "Arabic"
]

target_language = st.selectbox(
    "Select Target Language",
    languages
)


# --------------------------------------------------
# Process PDF
# --------------------------------------------------

if uploaded_file is not None:

    try:

        # Read PDF
        reader = PdfReader(uploaded_file)

        # Extract text
        document_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                document_text += text + "\n"

        # Validate extracted text
        if not document_text.strip():

            st.error(
                "No readable text was found in this PDF."
            )
            st.stop()


        # --------------------------------------------------
        # Display Extracted Content
        # --------------------------------------------------

        st.subheader("📖 Original Document")

        st.text_area(
            "Extracted PDF Content",
            document_text,
            height=400
        )


        # --------------------------------------------------
        # Translate Button
        # --------------------------------------------------

        if st.button("🌐 Translate Document"):

            translation_prompt = f"""
You are a professional document translator.

Translate the following document into {target_language}.

Important instructions:
- Translate the complete document.
- Preserve the original structure as much as possible.
- Preserve headings, paragraphs, lists and line breaks.
- Do not add explanations.
- Do not summarize the document.
- Return only the translated document.

Document:

{document_text}
"""


            # --------------------------------------------------
            # Groq API
            # --------------------------------------------------

            try:

                with st.spinner(
                    "Translating document..."
                ):

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a professional "
                                    "document translation assistant."
                                )
                            },
                            {
                                "role": "user",
                                "content": translation_prompt
                            }
                        ],
                        temperature=0.2,
                        max_tokens=6000
                    )


                    translated_text = (
                        response.choices[0]
                        .message.content
                    )


                # --------------------------------------------------
                # Display Translation
                # --------------------------------------------------

                st.subheader(
                    f"🌐 Translated Document ({target_language})"
                )

                st.text_area(
                    "Translated Content",
                    translated_text,
                    height=500
                )


                # --------------------------------------------------
                # Download Button
                # --------------------------------------------------

                st.download_button(
                    label="📥 Download Translation",
                    data=translated_text,
                    file_name=(
                        f"translated_document_"
                        f"{target_language}.txt"
                    ),
                    mime="text/plain"
                )


            except Exception as e:

                st.error(
                    f"Translation failed: {e}"
                )


    except Exception as e:

        st.error(
            f"Could not read the PDF: {e}"
        )