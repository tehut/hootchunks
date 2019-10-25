FROM python:3.6.1

# Create the group and user to be used in this container
RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/flask
WORKDIR /home/flask

# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY app/requirements.txt /home/flask
RUN pip3 install --no-cache-dir -r requirements.txt
# likely to remove
# COPY hootchunk home/flask/lib/python3.6/site-packages

# Copy the source code into the container

COPY app Makefile run.sh entrypoint.sh /home/flask/

RUN chmod +x /home/flask/entrypoint.sh
RUN chown -R flask:flaskgroup /home/flask
EXPOSE 5000
ENV SERVICE "localhost"
USER flask
CMD ["sh" ,"/home/flask/entrypoint.sh", "${SERVICE}"]
