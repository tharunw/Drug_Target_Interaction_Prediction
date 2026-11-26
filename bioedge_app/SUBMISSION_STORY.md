# BioEdge AI: A Local-First Biomedical Research Companion

**Creator:** R Tharun Kumar  
**Foundation project:** Drug–Target Interaction Prediction

## What I built
BioEdge AI is an experimental application layer for my existing drug–target interaction machine-learning project. It provides a local research interface to explore project documentation and compare reported model-evaluation results. It includes local TF-IDF retrieval over the project's README, an optional integration point for a locally running Ollama model, and an interactive model-performance dashboard.

## Problem it addresses
Machine-learning projects often contain useful methodology, feature definitions, evaluation results and limitations spread across technical documentation. BioEdge AI makes this information easier to explore through a single research-oriented interface. The local retrieval mode is designed to keep document search on the user's computer and does not require a cloud AI API.

## Technical approach
The interface is built with Streamlit. The retrieval component uses scikit-learn TF-IDF vectorisation and cosine similarity to find relevant README passages. An optional Ollama connection can generate a response from retrieved context when a local model is already installed. Plotly visualises baseline and enhanced model R² values.

## Connection to my existing research
The underlying project contains 18,745 drug–protein observations, 680 model input features and 11 protein targets. The enhanced representation combines 256 Morgan fingerprint features, 24 original protein sequence features and 400 dipeptide composition features. In the reported protein-grouped evaluation, R² changed from -0.2249 to -0.1763. This is a modest improvement, but the negative values show that generalisation to unseen protein targets remains challenging.

## What makes it meaningful to me
As a Biological Sciences student, I wanted to connect computational biology with practical AI software development. This prototype extends my original modelling work into an interactive tool and gave me an opportunity to think about retrieval, local processing, transparent evidence and the user experience of scientific software.

## Scope and limitations
This is a time-constrained prototype. The current retrieval-only feature indexes the project README, not arbitrary uploaded PDFs. Generative answers require Ollama and a compatible model installed locally; this integration must be tested on the target computer before describing it as operational. The dashboard displays metrics transcribed from the original README and does not run new predictions. The application is for research exploration only and is not clinically validated or intended for diagnosis or treatment.

## Technologies
Python, Streamlit, scikit-learn, TF-IDF, cosine similarity, Plotly, Pandas and optional Ollama integration.
