import urllib.request;
import json;
import mimetypes;
import time;
import datetime;

class Stream():
	def __init__(self, data):
		if "bitrate" in data:
			self.bitrate = int(data["bitrate"]) / 1024;

		self.mimetype = None;
		if "server_type" in data:
			if data["server_type"]:
				self.mimetype = data["server_type"];
		if not self.mimetype:
			self.mimetype = mimetypes.guess_type(data["listenurl"]);

		if "stream_start" in data:
			self.timestamp = int(time.mktime(datetime.datetime.strptime(data["stream_start"], "%a, %d %b %Y %H:%M:%S %z").timetuple()));

		self.title = data["server_name"] if "server_name" in data else None;
		self.description = data["server_description"] if "server_description" in data else None;
		self.genre = data["genre"] if "genre" in data else None;
		self.listeners = int(data["listeners"]);
		self.listener_peak = int(data["listener_peak"]);
		self.stream_url = data["listenurl"];
		self.server_url = data["server_url"] if "server_url" in data else None;
		self.playing = data["title"] if "title" in data else None;

	def __str__(self):
		return self.stream_url;

	def __int__(self):
		return self.listeners;

class IcecastStats():
	def __init__(self, url, user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64)"):
		req = urllib.request.Request(
			url + "/status-json.xsl",
			data=None,
			headers={
				'User-Agent': user_agent
			}
		);

		data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'));
		self.data = data["icestats"];

		self.streams = [];
		for i in range(0, len(self.data["source"])):
			self.streams.append(Stream(self.data["source"][i]));

	def getOverallListenerCount(self):
		count = 0;
		for i in range(0, len(self.streams)):
			count += int(self.streams[i]);

		return count;

	def __len__(self):
		return len(self.streams);

	def __getitem__(self, value):
		return self.streams[value];