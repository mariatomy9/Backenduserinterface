from flask import Flask, render_template, request, jsonify
import json
from os import path
from plyer import notification
import threading

app = Flask(__name__, static_folder="assets", template_folder="Templates")


def azure():

    # ----------------------------------VIDEO INDEXER---------------------------------

    import requests
    import os
    import io
    import json

    video_url = "https://storage123indexer.blob.core.windows.net/container2/New%20Directory/Conversation%20between%20Two%20Friends%20in%20English_Conversation%20about%20Sport_Daily%20Usage%20EnglishConversation.mp4"
    file_name = "videoplayback-test2.mp4"  # Example: myfile.wav

    # Important stuff
    video_indexer_account_id = "e9d3648f-54b1-4936-92b7-5b3eb8b47c23"  # Get this from https://www.videoindexer.ai/settings/account
    video_indexer_api_key = "a924aa2e5bff4d22b5896993dbe4e6cf"  # Get this from subscription at https://api-portal.videoindexer.ai/products/authorization
    video_indexer_api_region = (
        "eastus"  # Get this from https://www.videoindexer.ai/settings/account
    )

    auth_uri = "https://api.videoindexer.ai/auth/{}/Accounts/{}/AccessToken".format(
        video_indexer_api_region, video_indexer_account_id
    )
    auth_params = {"allowEdit": "true"}
    auth_header = {"Ocp-Apim-Subscription-Key": video_indexer_api_key}
    auth_token = requests.get(
        auth_uri, headers=auth_header, params=auth_params
    ).text.replace('"', "")

    msg("Video Indexer", "Authorization Complete")
    print("Video Indexer API: Authorization Complete.")
    print("Video Indexer API: Uploading file: ", file_name)

    # Upload Video to Video Indexer API
    upload_uri = "https://api.videoindexer.ai/{}/Accounts/{}/Videos".format(
        video_indexer_api_region, video_indexer_account_id
    )
    upload_header = {"Content-Type": "multipart/form-data"}
    upload_params = {
        "name": file_name,
        "accessToken": auth_token,
        "streamingPreset": "Default",
        "fileName": file_name,
        "videoUrl": video_url,
    }
    # files= {'file': (file_name, audio_file)}
    r = requests.post(upload_uri, params=upload_params)
    response_body = r.json()

    msg("Video Indexer", "Upload Completed")
    print("Video Indexer API: Upload Completed.")
    print("Video Indexer API: File Id: {} .".format(response_body.get("id")))

    # ---------------------------------------
    import time

    video_id = response_body.get("id")

    upload_uri = "https://api.videoindexer.ai/{}/Accounts/{}/Videos/{}/Index".format(
        video_indexer_api_region, video_indexer_account_id, video_id
    )
    upload_params = {"accessToken": auth_token, "language": "English"}
    print("Getting video info for: {}".format(video_id))

    g = requests.get(upload_uri, params=upload_params)
    response = g.json()
    while response["state"] == "Processing":
        g = requests.get(upload_uri, params=upload_params)
        response = g.json()
        msg(
            "Video Indexer", f"Status : {response['videos'][0]['processingProgress']}",
        )
        print(
            "Video still processing, current status: {}".format(
                response["videos"][0]["processingProgress"],
            )
        )
        time.sleep(15)
    jsondumper("video", response)
    msg("Video Indexer", "Video Indexed")
    print("Video Indexed")

    # -----EMOTION CALCULATION---------

    msg("Video Indexer", "Calculating")
    for x in response["videos"][0]["insights"]["transcript"]:
        print(x["text"])
    for j in x["instances"]:
        print(f"start time is {j['start']} and end time is {j['end']}")
    print("\n\n")

    for i in response["summarizedInsights"]["sentiments"]:
        print(i["sentimentKey"])
    for j in i["appearances"]:
        print(f"start time is {j['startTime']} and end time is {j['endTime']}")
    print("\n\n")

    for x in response["videos"][0]["insights"]["transcript"]:
        for y in x["instances"]:
            a = y["start"]
            b = y["end"]
            # print((a,b))
            for i in response["summarizedInsights"]["sentiments"]:
                for j in i["appearances"]:
                    c = j["startTime"]
                    d = j["endTime"]
                    # print((c,d))
                    # for time in (a, b):
                    if c <= a < d or c < b <= d:
                        print(i["sentimentKey"])
                        print((a, b))

    msg("Video Indexer", "Calculating Sentiments")
    l1 = []
    for x in response["videos"][0]["insights"]["transcript"]:
        if x["speakerId"] == int(1) or x["speakerId"] == int(3):
            for y in x["instances"]:
                a = y["start"]
                b = y["end"]
                # print((a,b))
                for i in response["summarizedInsights"]["sentiments"]:
                    for j in i["appearances"]:
                        c = j["startTime"]
                        d = j["endTime"]
                        # print((c,d))
                        if c <= a < d or c < b <= d:
                            # print(i['sentimentKey'])
                            l1.append(str(i["sentimentKey"]))
                            # print((a,b))

    print(l1)

    msg("Video Indexer", "Completed")
    l2 = []
    for x in response["videos"][0]["insights"]["transcript"]:
        if x["speakerId"] == int(2) or x["speakerId"] == int(4):
            for y in x["instances"]:
                a = y["start"]
                b = y["end"]
                # print((a,b))
                for i in response["summarizedInsights"]["sentiments"]:
                    for j in i["appearances"]:
                        c = j["startTime"]
                        d = j["endTime"]
                        # print((c,d))
                        if c <= a < d or c < b <= d:
                            # print(i['sentimentKey'])
                            l2.append(str(i["sentimentKey"]))
                            # print((a,b))

    print(l2)

    # ------------TOPIC EXTRACTION----------------
    l3 = []
    for i in response["summarizedInsights"]["topics"]:
        l3.append(i["name"])
    print(l3)

    thisdict = {"Positive": 9, "Neutral": 5, "Negative": 1}
    person1 = [thisdict[k] for k in l1]
    person2 = [thisdict[k] for k in l2]

    def Average(lst):
        return sum(lst) / len(lst)

    print(Average(person1))
    print(Average(person2))
    video_insights={"Customer Sentiments":Average(person1),"Agent Sentiments":Average(person2),"Language":"English","keywords":l3}
    jsondumper("videoInsights", video_insights)
    # ----------------------FORM RECOGNISER-----------------------------

    # import os
    # #! pip install azure-ai-formrecognizer --pre
    # #print(os.getcwd())

    # [END recognize_custom_forms]
    from formRecognise import RecognizeCustomForms

    sample = RecognizeCustomForms()
    output = sample.recognize_custom_forms()
    jsondumper("form", output)

    # # ----------------------DATABASE------------------------------------
    import uuid

    entry1 = {
        "id": "Andersen_" + str(uuid.uuid4()),
        "Customer ID": "CD700",
        "Service Agent ID": "AG10003",
        "VIP": "N",
        "Location": "Shrajah",
        "Department": "Health",
        "Language": "Tagalog",
        "Gender": "M",
        "Age": "30",
        "Complaint": "N",
        "Key Phrase": "",
        "Cu_Sentiments": "",
        "AG_Sentiments": "",
    }

    entry2 = {
        "id": "Andersen2_" + str(uuid.uuid4()),
        "Customer ID": "CD701",
        "Service Agent ID": "AG10002",
        "VIP": "Y",
        "Location": "Dubai",
        "Department": "Health",
        "Language": "English",
        "Gender": "M",
        "Age": "25",
        "Complaint": "N",
        "Key Phrase": "affordable,heartfelt,happiness",
        "Cu_Sentiments": "8",
        "AG_Sentiments": "9",
    }

    from azure.cosmos import exceptions, CosmosClient, PartitionKey

    # Initialize the Cosmos client
    endpoint = "https://cosmostrials.documents.azure.com:443/"
    key = "sC22JndQuhxLXjSzTwtsnDTjPNR8tqI6aEpXnc68nVn1TjGN9IJa9zfTjuxf6ATx0GOWnKwWUSon7M8JFp92Hw=="

    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)
    # </create_cosmos_client>

    # Create a database
    # <create_database_if_not_exists>
    database_name = "Details"
    database = client.create_database_if_not_exists(id=database_name)
    # </create_database_if_not_exists>

    # Create a container
    # Using a good partition key improves the performance of database operations.
    # <create_container_if_not_exists>
    container_name = "Details5"
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/Location"),
        offer_throughput=400,
    )
    # </create_container_if_not_exists>

    # Add items to the container
    family_items_to_create = [entry1, entry2]
    # family_items_to_create = b
    # <create_item>
    for family_item in family_items_to_create:
        container.create_item(body=family_item)
    # </create_item>

    # Read items (key value lookups by partition key and id, aka point reads)
    # <read_item>

    msg("Database created", "Data entered")
    for family in family_items_to_create:
        item_response = container.read_item(
            item=family["id"], partition_key=family["Location"]
        )
        request_charge = container.client_connection.last_response_headers[
            "x-ms-request-charge"
        ]
        print(
            "Read item with id {0}. Operation consumed {1} request units".format(
                item_response["id"], (request_charge)
            )
        )
    # </read_item>

    # Query these items using the SQL query syntax.
    # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
    # <query_items>
    query = "SELECT * FROM c WHERE c.Location IN ('Shrajah', 'Dubai')"

    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    request_charge = container.client_connection.last_response_headers[
        "x-ms-request-charge"
    ]

    print(
        "Query returned {0} items. Operation consumed {1} request units".format(
            len(items), request_charge
        )
    )


def jsondumper(name, data):
    with open(f"{name}.json", "w") as json_file:
        json.dump(data, json_file)


def parsed_form():
    pass


def msg(title, message):

    notification.notify(
        title=title, message=message, timeout=1, app_icon="lightbulb.ico"
    )


def isjson_available(file):
    print(path.exists(file))
    if path.exists(file):
        with open(file) as f:
            data = json.load(f)
        # json_formatted_str = json.dumps(data, indent=2)
        # print(json_formatted_str)
        return data
    else:
        return


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/next")
def next():
    threading.Thread(target=azure).start()
    return render_template("next.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/formdata", methods=["POST"])
def formdata():
    raw_data = isjson_available("form.json")
    # parsed = parsed_form(raw_data)

    return jsonify(
        {
            "raw_data": raw_data,
            "Additional Feedback": raw_data["Additional Feedback"],
            "Age": raw_data["Age"],
            "AgentID": raw_data["AgentID"],
            "CName": raw_data["CName"],
            "Complaint": raw_data["Complaint"],
            "Date": raw_data["Date"],
            "Feedback": raw_data["Feedback"],
            "Gender": raw_data["Gender"],
            "Location": raw_data["Location"],
            "TID": raw_data["TID"],
        }
    )
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


@app.route("/databaseupdate", methods=["POST"])
def databasedata():
    
    video_data =isjson_available("videoInsights.json")
    raw_data = isjson_available("form.json")
      
    return jsonify(
        [
            {
                "CustomerID": raw_data["TID"],
                "Service Agent ID": raw_data["AgentID"],
                "VIP": "Y",
                "Location": raw_data["Location"],
                "Department": "Health",
                "Language": video_data["Language"],
                "Gender": raw_data["Gender"],
                "Age": raw_data["Age"],
                "Complaint":raw_data["Complaint"],
                "Key Phrases": video_data["keywords"],
                "Customer Sentiments": video_data["Customer Sentiments"],
                "Agent Sentiments": video_data["Agent Sentiments"],
            }
        ]
    )


@app.route("/video")
def video():
    return render_template("video.html")


@app.route("/videodata", methods=["POST"])
def videodata():
    raw_data = isjson_available("video.json")
    video_data =isjson_available("videoInsights.json")
       
    

    return jsonify(
        {
            "raw_data": raw_data,
            "Customer Sentiments": video_data["Customer Sentiments"],
            "Agent Sentiments": video_data["Agent Sentiments"],
            "Language": video_data["Language"],
            "keywords": video_data["keywords"],
            
        }
    )


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
