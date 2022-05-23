gunicorn application:application > log.txt 2>&1 &
python3 data.py > data_log.txt 2>&1 &
