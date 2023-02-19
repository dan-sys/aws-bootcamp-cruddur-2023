FROM python:3.10-slim-buster

# this sets default work directory within the container(the OS we are building)
WORKDIR /backend-flask

# copy frm our gitpod os to the container
COPY requirements.txt requirements.txt

# this installs the pyhton libraries to used for the app in the container OS
RUN pip3 install -r requirements.txt

#here we are copying all the files from the folder backend-flask
# the first period . - in the copy command indicates the source we are copying everything from this folder (our gitpod workspace env)
# the second period . - in the copy command indicates the destination, we are putting everything we have copied
#we are using a second period simple cause we have our working directory as backend-flask
COPY . .

#here we set the environment variables
# thesse variables we are setting are in our container
ENV FLASK_ENV=development

EXPOSE ${PORT}

#CMD -command
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]