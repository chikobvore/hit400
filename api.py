import requests

#production
api_token = 'v0eref4fkwx3hycw'

headers = {'content-type': 'application/x-www-form-urlencoded'}


def reply_message(sender,message):
      message = message.encode('utf8').decode('latin-1')

      api_instance_url = 'https://api.ultramsg.com/instance6481/messages/chat'
      payload = "token="+api_token+"&to="+sender+"&body="+str(message)+"&priority=10&referenceId="
      response = requests.request("POST",api_instance_url, data=payload, headers=headers)

      print(str(response.text))
      return str(response.text)

def send_attachment(sender,attachment_url,caption):
      caption = caption.encode('utf8').decode('latin-1')

      api_instance_url = "https://api.ultramsg.com/instance6481/messages/image"
      payload = "token="+api_token+"&to="+sender+"&image="+attachment_url+"&caption="+caption+"&referenceId=&nocache="
      response = requests.request("POST", api_instance_url, data=payload, headers=headers)
      print(str(response.text))
      return str(response.text)

          