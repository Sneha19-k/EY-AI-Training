import configparser

config= configparser.ConfigParser()
config["database"] = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "admin1234"
}
#write to config file
with open("app.ini",'w') as configfile:
    config.write(configfile)

#read from config
config.read("app.ini")
print(config["database"]["host"])   #localhost