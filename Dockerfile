# Specify your base image
FROM python:3.8
# create a work directory
RUN mkdir /app
# navigate to this work directory
WORKDIR /app
#Copy all files
COPY . .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# set app port
EXPOSE 8080

ENTRYPOINT [ "python" ] 

# Run
CMD [ "app.py","run","--host","0.0.0.0"] 