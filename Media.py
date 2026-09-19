import ffmpeg
import hashlib
from mutagen.id3 import ID3, TIT2, COMM, TPE1, TPUB, TLAN, TRCK, TALB, TCOP
from mutagen.id3 import APIC, TDRC, TCON, TCOM, error as ID3Error
from PIL import Image
import io
from pathlib import Path

SD = (972, 972)
SDV = (720, 1280)
SDH = (1280, 720)
HDV = (1080, 1920)
HDH = (1920, 1080)
VGAV = (480, 640)
VGAH = (640, 480)
TESTV = (270, 480)
TESTH = (480, 270)

def get_cover_image(filename):
	tags = ID3(filename)
	for frame in tags.getall('APIC'):
		return Image.open(io.BytesIO(frame.data))

def set_id3_tags(filename, args=None):
	args = args or {}
	tags = ID3()
	if 'title' in args:
		tags.add(TIT2(encoding=3, text=args['title']))
	if 'artist' in args:
		tags.add(TPE1(encoding=3, text=args['artist']))
	if 'album' in args:
		tags.add(TALB(encoding=3, text=args['album']))

	year = args.get('year')
	if year is not None:
		date_parts = [str(year)]
		month = args.get('month')
		if month is not None:
			date_parts.append(f'{month:02d}')
			day = args.get('day')
			if day is not None:
				date_parts.append(f'{day:02d}')
		date_str = '-'.join(date_parts)
		tags.add(TDRC(encoding=3, text=date_str))

	if 'track_index' in args:
		track_str = str(args['track_index'])
		if 'num_tracks' in args:
			track_str += f"/{args['num_tracks']}"
		tags.add(TRCK(encoding=3, text=track_str))
	if 'genre' in args:
		tags.add(TCON(encoding=3, text=args['genre']))
	if 'language' in args:
		tags.add(TLAN(encoding=3, text=args['language']))
	if 'copyright' in args:
		tags.add(TCOP(encoding=3, text=args['copyright']))
	if 'publisher' in args:
		tags.add(TPUB(encoding=3, text=args['publisher']))
	if 'comments' in args:
		lang = args.get('language', 'eng')
		tags.add(COMM(encoding=3, lang=lang, desc='', text=args['comments']))
	if 'composer' in args:
		tags.add(TCOM(encoding=3, text=args['composer']))
	if 'image' in args:
		with open(args['image'], 'rb') as f:
			tags.add(APIC(encoding=0, mime='image/png', type=3, desc='Cover', data=f.read()))
	tags.save(filename, v2_version=4)

def read_id3_tags(filename):
	result = {}
	tags = ID3(filename)
	if 'TIT2' in tags and tags['TIT2'].text:
		result['title'] = tags['TIT2'].text[0]
	if 'TPE1' in tags and tags['TPE1'].text:
		result['artist'] = tags['TPE1'].text[0]
	if 'TDRC' in tags and tags['TDRC'].text:
		date_str = str(tags['TDRC'].text[0])
		# parse partial ISO date: "2026", "2026-05", "2026-05-09"
		parts = date_str.split('-')
		if len(parts) >= 1 and parts[0].isdigit():
			result['year'] = int(parts[0])
		if len(parts) >= 2 and parts[1].isdigit():
			result['month'] = int(parts[1])
		if len(parts) >= 3 and parts[2].isdigit():
			result['day'] = int(parts[2])
	if 'TRCK' in tags and tags['TRCK'].text:
		parts = str(tags['TRCK'].text[0]).split('/')
		if parts[0].isdigit():
			result['track_index'] = int(parts[0])
		if len(parts) > 1 and parts[1].isdigit():
			result['num_tracks'] = int(parts[1])
	if 'TCON' in tags and tags['TCON'].text:
		result['genre'] = tags['TCON'].text[0]
	if 'TLAN' in tags and tags['TLAN'].text:
		result['language'] = tags['TLAN'].text[0]
	if 'TCOP' in tags and tags['TCOP'].text:
		result['copyright'] = tags['TCOP'].text[0]
	if 'TPUB' in tags and tags['TPUB'].text:
		result['publisher'] = tags['TPUB'].text[0]
	comm_list = tags.getall('COMM')
	if comm_list and comm_list[0].text:
		result['comments'] = comm_list[0].text[0]
	if 'TCOM' in tags and tags['TCOM'].text:
		result['composer'] = tags['TCOM'].text[0]
	return result

def get_duration(filename):
	return float(ffmpeg.probe(filename)['format']['duration'])

def mp3towav(mp3, wav):
	ffmpeg.input(mp3).output(filename=wav).run(overwrite_output=True)

def md5(filepath):
	hash_md5 = hashlib.md5()
	with open(filepath, "rb") as f:
		for chunk in iter(lambda: f.read(65536), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def fit(stream, size):
	width, height = size
	target_ratio = width / height
	scaled = stream.filter('scale', w=f"if(gte(iw/ih,{target_ratio}),-1,{width})", h=f"if(gte(iw/ih,{target_ratio}),{height},-1)")
	video = scaled.filter('crop', width, height)
	return video
