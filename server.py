from re import M
from flask import Flask,request,send_file
import dotenv
import os
from main import run

dotenv.load_dotenv()

formHtml = f"""
<html>
   <body>
      <form action = "http://{os.getenv("redirectUrl")}/upload" method = "POST" enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit" value = "Submit" />
         <textarea name="text" style="width:250px;height:150px;"></textarea>
      </form>
   </body>
</html>
"""
 
app = Flask(__name__)

@app.route('/form')
def form():
    return formHtml
 
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
   if request.method == 'POST':
      code = request.form["text"]
      with open("project.spp", "w") as fi:
         fi.write(code)
      f = request.files['file']
      f.save("project.sb3")
      print("Compiling...")
      try:
         run("project.spp", "project.sb3", False)
      except:
         return "Error, check code"
      print("Done")
      return send_file("./project.sb3")
   else: return "Invalid method"
 
app.run(host='localhost', port=5000)