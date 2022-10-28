FROM pytorch/pytorch
WORKDIR /videogen
COPY . .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/openai/CLIP.git
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
