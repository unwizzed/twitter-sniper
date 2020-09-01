import requests, threading, time, ctypes,json

r = requests
goods = []
error, goods, failed = 0, 0 ,0
config = json.loads(open("config.json","r").read())


def check(name):
	global failed,good,error
	if len(name) > 4:
		headers = {
		"x-twitter-auth-type": "OAuth2Session",
		"x-csrf-token": config["csrf"],
		"x-twitter-active-user": "yes",
		"authorization":config["auth_bearer"]
		}
		cookies = {
		"auth_token":config["auth_token"]
		}
		uri = "https://twitter.com/i/api/i/users/username_available.json?username={}".format(name)
		while 1:
			try:
				rsp = r.get(uri, headers=headers, cookies=cookies)
				if "false" in rsp.text:
					print("Already used : {} - RSP : {}".format(name, rsp.text))
					failed += 1
					ctypes.windll.kernel32.SetConsoleTitleW("{} Good Names | {} Dead Names | {} Error".format(good, failed, error))
					break
				elif "true" in rsp.text:
					print("Freshed : {}  - RSP : {}".format(name, rsp.text))
					goods.append(name)
					good += 1
					ctypes.windll.kernel32.SetConsoleTitleW("{} Good Names | {} Dead Names | {} Error".format(good, failed, error))
					break
				else:
					error += 1
					ctypes.windll.kernel32.SetConsoleTitleW("{} Good Names | {} Dead Names | {} Error".format(good, failed, error))
					time.sleep(1)

			except requests.exceptions.ConnectionError: pass
	else: print("Length of word is too small : {}".format(name))


threads = []
for line in open("names.txt", "r").readlines():
	line = line.rstrip()
	t = threading.Thread(target=check, args=[line])
	t.start()
	threads.append(t)

for thread in threads:
	thread.join()

print("Sniped : " + str(goods))
