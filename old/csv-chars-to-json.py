# create handles for each csv file
import os

listing_path = os.path.join('C:','Users','Garren Ijames','Downloads','Scratch')
listing_result = os.listdir('/mnt/c/Users/Garren Ijames/Downloads/Scratch')
filtered_listing = [listing for listing in listing_result if '.csv' in listing]

handles = []
for listing in filtered_listing:
    handles.append(open(listing, 'r'))

json_output_string_buff = ['{"words": [']
print(len(handles))
for i, handle in enumerate(handles):
    lines = handle.readlines()
    json_output_string_buff.append('{"' + handle.name[0:handle.name.index('.')] + '": [')
    for j, line in enumerate(lines):
        arr = line.split(',')
        kanji = arr[0].strip().replace('"', '')
        kana = arr[1].strip().replace('"', '')
        meaning = arr[2].strip().replace('"', '')
        if j == len(lines) - 1:
            json_output_string_buff.append('{"kanji": "' + kanji + '", "pronun": "' + kana + '", "meaning": "' + meaning + '"}')
        else:
            json_output_string_buff.append('{"kanji": "' + kanji + '", "pronun": "' + kana + '", "meaning": "' + meaning + '"},')
    if i == len(handles) - 1:
        json_output_string_buff.append(']}')
    else:
        json_output_string_buff.append(']},')
json_output_string_buff.append(']}')

for handle in handle:
    handle.close()

out_handle = open('out.json', 'w')
out_handle.write(''.join(json_output_string_buff))

print(filtered_listing)

