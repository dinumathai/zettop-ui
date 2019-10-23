# Zettop UI
The UI for [zettop](http://www.zettop.com/)

### Technology Stack
1. Python  - Web server using `flask` library.
2. Jquery
3. Bootstrap

### Install and Run application
1. Install `flask` library for python - `pip install flask`
2. Install `gevent` library for python - `pip install gevent`
3. Update the `app.py` file with port ins which application must run - `app.run(host='0.0.0.0', port=5000, debug=False)`
4. Run the application - `python app.py`


### Browser Support
The application uses EventSource. The browser support is available [here](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Browser_compatibility)

### OS support
- Tested only in linux redhat. 
- Will not work in windows as the `subprocess.Popen` is not able execute the current command, refer `app.py`. To test ui in windows, change the streaming url in `script/try.js`