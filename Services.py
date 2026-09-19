API_FILE = 'elevenlabs.txt'

def client():
	# imported here so that importing Services does not require the elevenlabs package
	from elevenlabs import ElevenLabs
	from elevenlabs.environment import ElevenLabsEnvironment
	with open(API_FILE, 'r') as f:
		api_key = f.read().strip()
	return ElevenLabs(api_key=api_key, environment=ElevenLabsEnvironment.PRODUCTION)

def save(result, output_path):
	import elevenlabs
	elevenlabs.save(result, output_path)

def text_to_speech(text, voice_id, output_path):
	result = client().text_to_speech.convert(
		text=text,
		voice_id=voice_id,
		model_id="eleven_v3",
		language_code="he",
		output_format="mp3_44100_128",
	)
	save(result, output_path)
	return True

def speech_to_speech(input_path, voice_id, output_path):
	with open(input_path, 'rb') as f:
		audio_data = f.read()
	result = client().speech_to_speech.convert(
		voice_id=voice_id,
		output_format="mp3_44100_128",
		model_id="eleven_multilingual_sts_v2",
		audio=audio_data
	)
	save(result, output_path)
	return True

def forced_alignment(audiofile, text):
	with open(audiofile, 'rb') as audio_file:
		response = client().forced_alignment.create(
			file=audio_file,
			text=text
		)
	return response

def word_alignment(audiofile, text):
	response = forced_alignment(audiofile, text)
	word_tuples = []
	for word in response.words:
		if word.text.strip():
			word_tuples.append((word.start, word.end, word.text))
	return word_tuples
