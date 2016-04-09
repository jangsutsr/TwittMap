import boto.sqs
from boto.sqs.message import Message

class queue:

	def __init__(self):

		conn = boto.sqs.connect_to_region(
			'us-east-1',
			aws_access_key_id='AKIAIMZZIRCQ6KZS2HEQ',
			aws_secret_access_key='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')

		self.q = conn.create_queue('TweetMap')


	def send_message(self, meg):

		try:
			m = Message()
			m.set_body(meg)
			self.q.write(m)
		except:
			print 'message writing failed'


	def get_message(self):
		''' Retrieve a message and delete it from the queue
			Return None if there is no messages in the queue
		'''	

		m = self.q.read()
		meg = m.get_body() if m else None
		if m:
			self.q.delete_message(m)

		return meg

	def count(self):
		return self.q.count()
