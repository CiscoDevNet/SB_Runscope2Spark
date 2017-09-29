from flask import Flask, request, url_for, Response
import json
import requests
import config

app = Flask(__name__)

bot_token = config.BOT_TOKEN
room_id = config.ROOM_ID
base_path = "https://api.ciscospark.com"


def spark_msg(base_path, msg, token, rmid):
    msg_path = "/v1/messages"
    spark_url = base_path + msg_path

    headers = {"Content-type": "application/json",
               "Authorization": "Bearer %s" % token
               }

    spark_message = {"roomId": rmid,
                     "markdown": msg
                     }

    rs = requests.post(spark_url, headers=headers, data=json.dumps(spark_message))

    return rs.text


@app.route("/", methods=["POST"])
def r2s_fwd():

    data = str(request.data.decode("utf-8"))
    print(data)
    body = json.loads(data)
    headers = request.headers
    url = request.url_root

    if body["action"] == "acknowledge":
        alert_details = """**Sandbox Always-On API Previous Alert Acknowledged**"""
    else:
        alert_url = body["alert_url"]
        current_count = body["current_count"]
        alerts_hour = body["count_last_hour"]
        alerts_day = body["count_last_day"]
        alerts_30day = body["count_last_30_days"]
        total_alerts = body["total_count"]

        print(headers)
        print(body)
        print(url)

        alert_details = """**Sandbox Always-On API Request Alert Detected**\r\n\r\nPlease visit this URL, %s, to acknowledge and check on the alert\r\n\r\n**Alert Details:**\r\n\r\nCurrent Alert Count: **%s**\r\n\r\nAlert Count Last Hour: **%s**\r\n\r\nAlert Count Last Day: **%s**\r\n\r\nAlert Count Last 30 Days: **%s**\r\n\r\nAll Time Total Alert Count : **%s**\r\n\r\n""" % (alert_url,
                                                                                                                                                                                                                                                                                                                                                                                        current_count,
                                                                                                                                                                                                                                                                                                                                                                                        alerts_hour,
                                                                                                                                                                                                                                                                                                                                                                                        alerts_day,
                                                                                                                                                                                                                                                                                                                                                                                        alerts_30day,
                                                                                                                                                                                                                                                                                                                                                                                        total_alerts)

    print(alert_details)

    print(spark_msg(base_path, alert_details, bot_token, room_id))

    return Response(status=201)


if __name__ == "__main__":
    app.run("0.0.0.0", port=8888)
