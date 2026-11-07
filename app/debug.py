print("starting debugger...")


import debugpy

debugpy.listen(("127.0.0.1", 44551))
debugpy.wait_for_client()

print("client connected to debugger, importing main.py")


import app.main
