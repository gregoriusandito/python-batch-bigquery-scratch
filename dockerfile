# Ubuntu 16.04 ships with both Python 3 and Python 2 pre-installed
FROM ubuntu:latest

# Install cron
RUN apt-get update
RUN apt-get install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron

# Add shell script and grant execution rights
ADD script.sh /script.sh
RUN chmod +x /script.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Add python script to be applied in batch
ADD batch.py /batch.py

# Add requirements for the python script
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log