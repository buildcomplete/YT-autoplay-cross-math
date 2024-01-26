FROM gnuoctave/octave:8.4.0
WORKDIR /eye
RUN apt-get update && apt-get install -y octave-io octave-image octave-signal
CMD ["tail", "-f", "/dev/null"]
#CMD ["python3", "file-listener.py"]