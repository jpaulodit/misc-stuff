# Purpose : Curbside exercise.
# Author : John Win ( jpaulodit@hotmail.com )
# Date : 12/12/2015
# Note : Use python 3 to run file.

from urllib import request, error
from collections import deque
from time import sleep
import json

class curbside():

	# constant
	invalid_sid = 'Invalid session id, a token is valid for 10 requests.'


	def __init__(self):

		self.__session_id = None
		self.__base_url = 'http://challenge.shopcurbside.com/'
		self.__secret_list = []



	# method to retrieve a valid session id from site.
	def __get_sesion_id(self):

		sleep(0.1)
		resource = 'get-session'
		url = self.__base_url + resource

		req = request.Request(url)

		try:
			resp = request.urlopen(req)
			data = resp.read()
			self.__session_id = data

		except error.HTTPError as err:
			print(err.read())
			raise RuntimeError('issue getting session id') from err



	def __bfs_traverse(self, resources):

		if resources:

			myQueue = deque()
			for resource in resources:
				myQueue.appendleft(resource)

			while(myQueue):

				resource = myQueue.pop()

				resp = self.__get_resource(resource)

				if 'next' in resp:

					# need to decide what type of data type "next" is
					if type(resp['next']) is list:
						for node_id in resp['next']:
							myQueue.appendleft(node_id)
					
					elif type(resp['next']) is str:
						myQueue.appendleft(resp['next'])

					else:
						raise RuntimeError('unknown data type')

				if 'secret' in resp:
					self.__secret_list.append(resp['secret'])



	def __dfs_traverse(self, resource):

		resp = self.__get_resource(resource)

		if 'next' in resp:

			# need to decide what type of data type "next" is
			if type(resp['next']) is list:
				for node_id in resp['next']:
					self.__dfs_traverse(node_id)

			elif type(resp['next']) is str:
				self.__dfs_traverse(resp['next'])

			else:
				raise RuntimeError('unknown data type')

		if 'secret' in resp:
			self.__secret_list.append(resp['secret'])



	def __get_resource(self, resource):

		sleep(0.1)
		url = self.__base_url + resource
		headers = { 'Session' : self.__session_id}

		req = request.Request(url, headers=headers)

		try:
			resp = request.urlopen(req)
			resp = json.loads(resp.read().decode('utf-8'))

			# make keys in resp lower case to handle inconsistent formating.
			new_resp = {}			
			for key in resp:
				new_resp[key.lower()] = resp[key]

			return new_resp

		except error.HTTPError as err:
			
			msg = json.loads(err.read().decode('utf-8'))

			if msg['error'] == self.invalid_sid:
				self.__get_sesion_id()
				return self.__get_resource(resource)

			else:
				raise RuntimeError('issue getting resource='+resource+str(err.read())) from err



	def get_secret(self):

		if self.__secret_list:
			return ''.join(self.__secret_list)
		else:
			return 'No secret data.'



	def start(self, mode='dfs'):

		self.__get_sesion_id()

		resp = self.__get_resource('start')

		if 'next' in resp:
			
			if mode == 'dfs':
				print('DFS')
				for node_id in resp['next']:
					self.__dfs_traverse(node_id)

			else:
				print('BFS')
				self.__bfs_traverse(resp['next'])



if __name__ == '__main__':

	c = curbside()
	c.start()
	print(c.get_secret())
	print('**** END OF PROGRAM ****')