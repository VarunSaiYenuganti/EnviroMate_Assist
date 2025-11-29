EnviroMate Assist – Recycling Instruction Generator

Overview:

EnviroMate Assist is an AI-powered recycling web app designed to help users understand how to recycle everyday objects. It uses image processing, image captioning, and language models to generate clear, accurate recycling instructions.

How It Works

The system follows a three-step pipeline:

1️⃣ Image Segmentation – FastSAM

Identifies objects in the input image by segmenting individual items.

2️⃣ Image Captioning – BLIP

Generates descriptive captions for each segmented object.

3️⃣ Recycling Instruction Generation – OpenAI Model

Uses captions + an embedded recycling guideline database to produce:

Object-specific instructions,
Location-aware recycling advice.

Tools & Technologies:

Python

FastSAM – object segmentation

BLIP – caption generation

LangChain – instruction generation framework

OpenAI Embeddings (Ada-002)

OpenAI GPT-3.5 Turbo – recycling instruction generation

Implementation Flow:

Run main.py to start the backend server

Hit the run process API

Pipeline executes:
✔ Segmentation → ✔ Captioning → ✔ Instruction Generation

Example Output:
{
 "image": "segment_1.png",
 "label": "there is a large plastic jar with a blue lid",
 "answer": "The plastic jar with the blue lid can be recycled in your blue cart or at a community recycling depot. Ensure the lid is larger than 7.5 cm. If not recyclable, dispose of in the black cart."
}

