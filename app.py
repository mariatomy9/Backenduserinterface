from flask import Flask, render_template, request,jsonify
import json
from os import path
app = Flask(__name__, static_folder="assets", template_folder="Templates")

def parsed_form():
    pass
def isjson_available():
    file="data.json"
    if path.exists(file):
        with open('data.json') as f:
            data = json.load(f)
        # json_formatted_str = json.dumps(data, indent=2)
        # print(json_formatted_str)   
        return data
    else:
        return 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/formdata",methods=['POST'])
def formdata():
    # raw_data = isjson_available()
    # parsed = parsed_form(raw_data)
    
    return jsonify({'Additional Feedback': 'Excellant Pleasant nalise Also giving instructions for each of the services.',
 'Age': None,
 'AgentID': 'AG10005',
 'CName': 'Ayisha Fathima',
 'Complaint': None,
 'Date': None,
 'Feedback': '00',
 'Gender': 'F',
 'Location': 'Alman',
 'TID': 'CD764'})
              #    name=,
                #    tid=,
                #    aid=,
                #    location=,
                #    age =
                #    feedback=
                #    complaint=
                #    feedbacktext=


@app.route("/database")
def database():
    return render_template("database.html")


@app.route("/databaseupdate",methods=['POST'])
def databasedata():
    raw_data = isjson_available()
    
    return jsonify([{"CustomerID" : "CD701",
    "Service Agent ID": "AG10002",
    "VIP": "Y",
    "Location": "Dubai",
    "Department": "Health",
    "Language": "English",
    "Gender": "M",
    "Age": "35",
    "Complaint": "N",
    "Key Phrase": "affordable,heartfelt,happiness",
    "Cu_Sentiments": "8",
    "AG_Sentiments": "9",}])

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/videodata",methods=['POST'])
def videodata():
    raw_data = isjson_available()
    
    return jsonify({"raw_data":raw_data,
        "CustomerID" : "CD701",
    "Service Agent ID": "AG10002",
    "VIP": "Y",
    "Location": "Dubai",
    "Department": "Health",
    "Language": "English",
    "Gender": "M",
    "Age": "35",
    "Complaint": "N",
    "Key Phrase": "affordable,heartfelt,happiness",
    "Cu_Sentiments": "8",
    "AG_Sentiments": "9",})

@app.route("/powerbi")
def powerbi():
    return render_template("powerbi.html")
# def 
# dictionary ={ 
#     "name" : "sathiyajith", 
#     "rollno" : 56, 
#     "cgpa" : 8.6, 
#     "phonenumber" : "9976770500"
# } 
     
# with open("sample.json", "w") as outfile: 
#     json.dump(dictionary, outfile)

if __name__ == "__main__":
    app.run(debug=True)
