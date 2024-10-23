# mp3 id3v2 no library parser

import sys

def read_synchsafe_int(b):
    size = 0
    for i in range(4):
        size <<= 7
        size |= b[i] & 0x7F
    return size

def read_uint32(b):
    return int.from_bytes(b, byteorder='big')

def read_frames(f, tag_size):
    end = 10 + tag_size
    current_pos = 10
    frames = {}
    while current_pos < end:
        f.seek(current_pos)
        header = f.read(10)
        if len(header) < 10 or header[0:4] == b'\x00\x00\x00\x00':
            break
        frame_id = header[0:4].decode('iso-8859-1')
        frame_size = read_uint32(header[4:8])
        frame_flags = header[8:10]
        if frame_size <= 0:
            break  
        current_pos += 10
        f.seek(current_pos)
        frame_data = f.read(frame_size)
        frames[frame_id] = frame_data
        current_pos += frame_size
    return frames

def decode_text_frame(frame_data):
    if len(frame_data) < 1:
        return ''
    encoding = frame_data[0]
    data = frame_data[1:]
    if encoding == 0:
        return data.decode('iso-8859-1').strip('\x00')
    elif encoding == 1:
        return data.decode('utf-16').strip('\x00')
    elif encoding == 2:
        return data.decode('utf-16-be').strip('\x00')
    elif encoding == 3:
        return data.decode('utf-8').strip('\x00')
    else:
        return ''

def parse_comment_frame(frame_data):
    if len(frame_data) < 4:
        return ''
    encoding = frame_data[0]
    lang = frame_data[1:4].decode('iso-8859-1')
    data = frame_data[4:]
    if encoding == 0:
        texts = data.decode('iso-8859-1').split('\x00', 1)
    elif encoding == 1:
        texts = data.decode('utf-16').split('\x00', 1)
    elif encoding == 2:
        texts = data.decode('utf-16-be').split('\x00', 1)
    elif encoding == 3:
        texts = data.decode('utf-8').split('\x00', 1)
    else:
        return ''
    if len(texts) == 2:
        short_desc, comment = texts
    else:
        short_desc, comment = texts[0], ''
    return comment.strip('\x00')

def main(filename):
    with open(filename, 'rb') as f:
        header = f.read(10)
        if len(header) != 10 or header[0:3] != b'ID3':
            print('No ID3 tag found')
            return
        version = header[3]
        revision = header[4]
        flags = header[5]
        size = read_synchsafe_int(header[6:10])
        frames = read_frames(f, size)

        artist = ''
        title = ''
        album = ''
        year = ''
        comment = ''
        genre = ''
        if 'TPE1' in frames:
            artist = decode_text_frame(frames['TPE1'])
        if 'TIT2' in frames:
            title = decode_text_frame(frames['TIT2'])
        if 'TALB' in frames:
            album = decode_text_frame(frames['TALB'])
        if 'TYER' in frames:
            year = decode_text_frame(frames['TYER'])
        if 'TDRC' in frames:
            year = decode_text_frame(frames['TDRC'])
        if 'TCON' in frames:
            genre = decode_text_frame(frames['TCON'])
        if 'COMM' in frames:
            comment = parse_comment_frame(frames['COMM'])
        print('Artist:', artist)
        print('Title:', title)
        print('Album:', album)
        print('Year:', year)
        print('Genre:', genre)
        print('Comment:', comment)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py filename.mp3')
    else:
        main(sys.argv[1])