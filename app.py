import os
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from fastmcp import Client

load_dotenv()

st.set_page_config(page_title="Auto PPT Agent")
st.title("Auto PPT Agent")

token = os.getenv("HF_TOKEN")
model_id = os.getenv("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=token,
)

user_prompt = st.text_area(
    "Enter your presentation requirement",
    height=150,
    placeholder="Example: Create a 6-slide presentation on machine learning for college students. Include supervised learning, unsupervised learning, real-world applications, advantages, and challenges. Use simple language."
)
slide_count = st.number_input("Number of slides", min_value=3, max_value=10, value=5, step=1)

theme = st.selectbox(
    "Choose a presentation theme",
    [
        "Classic Blue",
        "Modern Dark",
        "Minimal Light",
        "Green Professional",
        "Purple Gradient"
    ]
)


def generate_outline(user_prompt: str, slide_count: int):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "You create presentation outlines. Return only valid JSON."
            },
            {
                "role": "user",
                "content":f"""
                Create a {slide_count}-slide presentation outline based on this user request:

                {user_prompt}

                Rules:
                  - Return only valid JSON
                  - First slide should be introduction/title
                  - Last slide should be conclusion/summary
                  - Make the outline match the user's requested sections when possible
                  - Format:
                [
                   {{"title": "Slide 1 title"}},
                   {{"title": "Slide 2 title"}}
                ]
            """
            }
        ],
        temperature=0.2,
        max_tokens=512,
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)
    except Exception:
        return [
    {"title": "Introduction"},
    {"title": "Key Concepts"},
    {"title": "Applications"},
    {"title": "Benefits and Challenges"},
    {"title": "Conclusion"},
]
    

def generate_title(user_prompt: str):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "Generate a short presentation title from the user's request. Return only plain text."
            },
            {
                "role": "user",
                "content": f"""
                    Create a short presentation title from this request:
                    {user_prompt}

                    Rules:
                       - Keep it short
                       - Maximum 6 words
                       - Return only the title
                       - Do not add quotes
                       - Do not add explanation
            """
            }
        ],
        temperature=0.2,
        max_tokens=50,
    )

    return response.choices[0].message.content.strip()    


def generate_bullets(user_prompt: str, slide_title: str):
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "You generate slide bullet points. Return only valid JSON."
            },
            {
                "role": "user",
                "content": f"""
                User request:
                {user_prompt}

                Slide title:
                {slide_title}

                Generate 7 short bullet points for this slide.

                Rules:
                - Keep the language simple
                - Make bullets match the user's requirement
                - Return only valid JSON
                - Format:
                {{"bullets": ["point1", "point2", "point3", "point4"]}}
        """
        }
        ],
        temperature=0.2,
        max_tokens=256,
    )

    raw = response.choices[0].message.content

    try:
        return json.loads(raw)["bullets"]
    except Exception:
        return [
    f"Introduction to {slide_title}",
    f"Main points about {slide_title}",
    f"Important example related to {slide_title}",
    f"Summary of {slide_title}",
]


async def save_outline_to_file(outline):
    async with Client("http://localhost:8002/mcp") as fs_client:
        await fs_client.call_tool(
            "write_file",
            {
                "filename": "outline.json",
                "content": json.dumps(outline, indent=2)
            }
        )


async def save_slide_content_to_file(slide_data):
    async with Client("http://localhost:8002/mcp") as fs_client:
        await fs_client.call_tool(
            "write_file",
            {
                "filename": "slide_content.json",
                "content": json.dumps(slide_data, indent=2)
            }
        )


def build_ppt(user_prompt: str, slide_count: int, theme: str):
    async def _run():
        presentation_title = generate_title(user_prompt)
        outline = generate_outline(user_prompt, slide_count)
        await save_outline_to_file(outline)

        slide_content_data = []

        async with Client("http://localhost:8000/mcp") as mcp_client:
            await mcp_client.call_tool("create_presentation", {})

            await mcp_client.call_tool(
        "add_title_slide",
    {
        "title": presentation_title,
        "subtitle": "Auto-generated presentation",
        "theme": theme
    }
)

            for slide in outline[1:]:
                title = slide["title"]
                bullets = generate_bullets(user_prompt, title)

                slide_content_data.append({
                    "title": title,
                    "bullets": bullets
                })

                await mcp_client.call_tool(
                    "add_bullet_slide",
                    {
                        "title": title,
                        "bullets": bullets,
                        "theme": theme
                    }
                )

            await save_slide_content_to_file(slide_content_data)

            result = await mcp_client.call_tool(
                "save_presentation",
                {
                    "filename": "generated_presentation.pptx"
                }
            )

            if hasattr(result, "data"):
                return result.data
            return result

    return asyncio.run(_run())


if st.button("Generate PPT"):
    clean_prompt = user_prompt.strip()

    if clean_prompt:
        with st.spinner("Generating presentation..."):
            path = build_ppt(clean_prompt, slide_count, theme)

        st.success("Presentation generated successfully")
        st.info("Planning files saved in workspace folder: outline.json and slide_content.json")
        st.write("Saved path:", path)

        with open(path, "rb") as f:
            st.download_button(
                label="Download PPT",
                data=f,
                file_name="generated_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.error("Please enter your presentation requirement")