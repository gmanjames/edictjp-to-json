'''
edictjp-to-json.py: Convert electronic dictionary file from an EDICT-JP format to more web-consumable JSON

notes:
    For edict format see www.edrdg.org/jmdict/dtd-jmdict.xml
    In summary each entry is defined as 'entry (ent_seq, k_ele*, r_ele+, sense+)'
    EDICT2 KANJI-1;KANJI-2 [KANA-1;KANA-2] /(general information) (see xxxx) gloss/gloss/.../

    k_ele: kanji or alternative kanji
    r_ele: reading element (hiragana, katakana, etc.)
    sense: 'translational equivalent'

'''
import settings

import os, codecs

# Final json output string to be written to file
json_buffer  = '{'
json_entries = []

# File object handle for edict file
edict_handle = None

# MAIN
def main():
    global edict_handle, json_buffer

    edict_handle = codecs.open(os.path.join(settings.DATA_DIR,'edict2'), 'r', 'EUC-JP')

    count = 0 # some of the first lines have data we don't want
    for line in edict_handle:
        if count > 0:

            entry_components = line.strip().split('/')

            #k_ele and r_ele's
            k_and_r = entry_components[0]

            k_ele = k_and_r[0:k_and_r.find('[')]
            r_ele = k_and_r[k_and_r.find('[')+1:k_and_r.find(']')]

            #part of speech, sense, see, translations, etc.
            remaining_parts = entry_components[1:-1]
            sense   = remaining_parts[0:-2]
            ent_seq = remaining_parts[-1]

            json_entry = '"' + ent_seq + '": {\n'
            json_entry += '  "k_ele": ' + '[' + ','.join( map(lambda elem: '"' + elem.strip() + '"', k_ele.split(';')) ) + ']' + ',\n'
            json_entry += '  "r_ele": ' + '[' + ','.join( map(lambda elem: '"' + elem.strip() + '"', r_ele.split(';')) ) + ']' + ',\n'
            json_entry += '  "sense": ' + '[' + ','.join( map(lambda elem: '"' + elem.strip() + '"', sense) ) + ']\n'
            json_entry += '}'
            json_entries.append(json_entry)


        count += 1

    edict_handle.close()
    json_buffer += ',\n'.join(json_entries) + '}'
    write_out(json_buffer)


# END: MAIN


# Write to output json file
def write_out(buffer_string):
    # write to output file
    out_handle = codecs.open('out.json', 'w', 'UTF-8')
    out_handle.write(buffer_string)
    out_handle.close()


# RUN
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('terminating processing...')
        edict_handle.close()
        print('done.')
        print('writing to out.json...')
        json_buffer += ',\n'.join(json_entries) + '}'
        write_out(json_buffer)
        print('done.')
