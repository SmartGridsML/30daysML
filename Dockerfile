# FROM python:3.9

# RUN useradd -m -u 1000 user
# USER user
# ENV PATH="/home/user/.local/bin:$PATH"

# WORKDIR /app

# COPY --chown=user ./requirements.txt /spaces/dana_airequirements.txt 
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY --chown=user . /app
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.9

WORKDIR /app

# Copy requirements first for better caching
COPY spaces/dana_ai/requirements.txt .
RUN pip install  -r requirements.txt

# Copy the rest of the application
COPY spaces/dana_ai .

# Set the working directory to where app.py is located
#WORKDIR spaces/dana_ai
RUN ls -la
CMD ["python", "app.py"]