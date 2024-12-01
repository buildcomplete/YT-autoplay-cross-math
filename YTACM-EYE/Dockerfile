FROM gnuoctave/octave:8.4.0
WORKDIR /eye
RUN octave -q --no-window-system --eval "pkg install -forge io"
RUN octave -q --no-window-system --eval "pkg install -forge control"
RUN octave -q --no-window-system --eval "pkg install -forge signal"
RUN octave -q --no-window-system --eval "pkg install -forge image"

CMD ["tail", "-f", "/dev/null"]
#CMD ["python3", "file-listener.py"]