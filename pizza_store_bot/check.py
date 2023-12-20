def check_int(message):
    try:
        message.text = int(message.text)
        return True
    except:
        return False

