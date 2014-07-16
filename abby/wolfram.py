import httplib2
import urllib

from xml.dom import minidom

class Wolfram():
	URL = "http://api.wolframalpha.com/v2/query?&input=%s&appid=KX6GW4-WK5JVW8RVW&format=plaintext"
	
	def __init__(self):
		pass

	def get_response(self, query):
		xml = self._get_xml(query)

		return self._extract_message(xml)

	def _extract_message(self, xml):
		if xml.documentElement.attributes['success'].value != 'true':
			return 'Pardon?'

		primary = None

		for elem in xml.getElementsByTagName('pod') :
			if 'primary' in elem.attributes and elem.attributes['primary'].value == 'true':
				primary = elem
				break

		if not primary: return 'Something went wrong while processing the output'

		return primary.getElementsByTagName('plaintext')[0].firstChild.data 


	def _get_xml(self, query):

		request = httplib2.Http()
		response, content = request.request( Wolfram.URL % urllib.parse.quote(query),  "GET" )

		content_str = content.decode("utf-8")

		return minidom.parseString(content_str)

if __name__ == '__main__':
	wolf = Wolfram()

	print( wolf.get_response('How are you') )


		
		