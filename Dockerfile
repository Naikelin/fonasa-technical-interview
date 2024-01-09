FROM python
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["bash", "-c", "flask db migrate && flask db upgrade && flask run --host=0.0.0.0"]
