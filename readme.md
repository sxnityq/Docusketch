# Docusketch assignment
This is the Docusketch assignment readme.md file which describes how to run everything correctly

## Installation & Configuration
* git clone https://github.com/sxnityq/Docusketch.git
* docker-compose build 
* make memoryMonitoring.sh executable and add it to your crontab file
```sh
chmod +x <path-to-memoryMonitoring.sh>
crontab -e 
* * * * * <path-to-memoryMonitoring.sh>
```
__For proper ram percantage evaluation install additional package **"bc"**__
* sudo <your package manager> bc 

## Daily Usage
* docker-compose up

## Additional information

memoryMonitoring.sh collect information about your ram consumption and hard memory partition that belongs to current user ("/" for root, "/home" for other) and send POST request to corresponding URL (by default "http://127.0.0.1:5000/docusketch/v1/api/task")

![where is image?)](https://64.media.tumblr.com/db4349ff05509b84a7d0b52dd5fe81a1/915dd2dd7f5e633a-84/s1280x1920/b2062324cd2daf15fe941a9e38935459da7baaf0.gifv)