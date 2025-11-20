#!/usr/bin/env python3
import json
import urllib.request

def anki_request(action, params):
    """Send a request to AnkiConnect API"""
    request = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode('utf-8')

    try:
        response = urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", request)
        )
        result = json.loads(response.read().decode('utf-8'))

        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return None
        return result.get('result')
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

# Mapping of card words to sentence audio files
sentence_audio_map = {
    "thời gian rảnh": "thoi_gian_ranh_sentence",
    "sở thích": "so_thich_sentence",
    "đọc sách": "doc_sach_sentence",
    "thể loại": "the_loai_sentence",
    "lịch sử": "lich_su_sentence",
    "trinh thám": "trinh_tham_sentence",
    "chủ đề": "chu_de_sentence",
    "La Mã và Hy Lạp cổ": "la_ma_hy_lap_sentence",
    "chuyên nghiệp": "chuyen_nghiep_sentence",
    "trượt ván": "truot_van_sentence",
    "công viên": "cong_vien_sentence",
    "một lúc": "mot_luc_sentence",
    "một giờ": "mot_gio_sentence",
    "tập": "tap_sentence",
    "bạn bè": "ban_be_sentence",
    "đi du lịch": "di_du_lich_sentence",
    "năm ngoái": "nam_ngoai_sentence",
    "nhất": "nhat_sentence",
    "quên": "quen_sentence",
    "lâu rồi": "lau_roi_sentence",
    "tác giả": "tac_gia_sentence",
    "phổ biến": "pho_bien_sentence",
    "cuối tuần": "cuoi_tuan_sentence",
    "thư giãn": "thu_gian_sentence",
    "nam giới": "nam_gioi_sentence",
    "nữ giới": "nu_gioi_sentence",
    "cầu lông": "cau_long_sentence",
    "bóng đá": "bong_da_sentence",
    "anh ấy": "anh_ay_sentence",
    "ông ấy": "ong_ay_sentence",
    "cô ấy": "co_ay_sentence",
    "bà ấy": "ba_ay_sentence",
    "em ấy": "em_ay_sentence",
    "nó": "no_sentence",
}

print("Finding all vocabulary cards to update with sentence audio...\n")

# Get all notes except question patterns
result = anki_request("findNotes", {"query": "deck:Vietnamese -tag:questions"})
note_ids = result if isinstance(result, list) else result.get('result', [])

if note_ids:
    note_info_result = anki_request("notesInfo", {"notes": note_ids})
    note_info = note_info_result if isinstance(note_info_result, list) else note_info_result.get('result', [])

    updated_count = 0
    for note in note_info:
        word = note['fields']['Learning Language']['value']

        if word in sentence_audio_map:
            audio_file = sentence_audio_map[word]

            # Update the note with sentence audio
            updated_note = {
                "id": note['noteId'],
                "fields": {
                    "Learning Language": note['fields']['Learning Language']['value'],
                    "Native Language": note['fields']['Native language']['value'],
                    "Example (Learning)": note['fields']['Example (Learning)']['value'],
                    "Example (native)": note['fields']['Example (native)']['value'],
                    "Audio Word": note['fields']['Audio Word']['value'],
                    "Audio Sentence": f"[sound:{audio_file}.mp3]"
                },
                "tags": note['tags']
            }

            result = anki_request("updateNote", {"note": updated_note})
            if result:
                print(f"✓ Updated: {word}")
                updated_count += 1

print(f"\n✓ Updated {updated_count} cards with sentence audio")
