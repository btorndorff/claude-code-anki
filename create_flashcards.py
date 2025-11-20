#!/usr/bin/env python3
import json
import urllib.request
import urllib.error

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
        print("Make sure Anki is running and AnkiConnect is installed")
        return None

def create_flashcard(deck, vietnamese, english, example_vi, example_en, audio_word, audio_sentence, tags):
    """Create a single flashcard"""
    note = {
        "deckName": deck,
        "modelName": "Language Learning",
        "fields": {
            "Learning Language": vietnamese,
            "Native Language": english,
            "Example (Learning)": example_vi,
            "Example (Native)": example_en,
            "Audio Word": f"[sound:{audio_word}.mp3]" if audio_word else "",
            "Audio Sentence": f"[sound:{audio_sentence}.mp3]" if audio_sentence else ""
        },
        "tags": tags
    }

    result = anki_request("addNote", {"note": note})
    if result:
        print(f"✓ Created: {vietnamese} ({english})")
        return True
    return False

# Question Patterns
print("\n=== Creating Question Pattern Cards ===")
question_patterns = [
    ("... đúng không?", "to affirm if something is true", "Em thích đọc sách sci-fi đúng không?", "You like to read sci-fi books, correct?", "dung_khong_word", "dung_khong_sentence", ["questions", "grammar"]),
    ("... không?", "yes/no question", "Em thích tập yoga ở công viên không?", "Do you like to practice yoga in the park?", "khong_word", "khong_sentence", ["questions", "grammar"]),
    ("... chưa?", "have you... yet?", "Em ăn chưa?", "Have you eaten yet?", "chua_word", "chua_sentence", ["questions", "grammar"]),
    ("... gì?", "what", "Em thích đọc sách gì?", "What books do you like to read?", "gi_word", "gi_sentence", ["questions", "grammar"]),
    ("... thế nào?", "how", "Em thế nào?", "How are you?", "the_nao_word", "the_nao_sentence", ["questions", "grammar"]),
    ("... ai?", "who/whom", "Em thường chụp ảnh với ai?", "Who do you usually take photos with?", "ai_word", "ai_sentence", ["questions", "grammar"]),
    ("... ở đâu?", "where (location)", "Em thường chụp ảnh ở đâu?", "Where do you usually take photos?", "o_dau_word", "o_dau_sentence", ["questions", "grammar"]),
    ("... đâu?", "where (going)", "Em đi đâu?", "Where are you going?", "dau_word", "dau_sentence", ["questions", "grammar"]),
    ("... bao nhiêu?", "how many/how much", "Em tập yoga bao nhiêu lần một tuần?", "How many times per week do you practice yoga?", "bao_nhieu_word", "bao_nhieu_sentence", ["questions", "grammar"]),
    ("... bao lâu?", "how long", "Em ở Uzbekistan bao lâu?", "How long did you stay in Uzbekistan?", "bao_lau_word", "bao_lau_sentence", ["questions", "grammar"]),
    ("... trong bao lâu?", "for how long", "Em chơi trượt ván trong bao lâu?", "For how long do you skateboard?", "trong_bao_lau_word", "trong_bao_lau_sentence", ["questions", "grammar"]),
    ("... lúc nào?", "when", "Em trượt ván lúc nào?", "When do you skateboard?", "luc_nao_word", "luc_nao_sentence", ["questions", "grammar"]),
    ("... vì sao?", "why", "Vì sao?", "Why?", "vi_sao_word", "vi_sao_sentence", ["questions", "grammar"]),
    ("... nào?", "which", "Chị thích đọc sách thể loại nào nhất?", "Which book genre do you like the most?", "nao_word", "nao_sentence", ["questions", "grammar"]),
]

for vi, en, ex_vi, ex_en, audio_word, audio_sent, tags in question_patterns:
    create_flashcard("Vietnamese", vi, en, ex_vi, ex_en, audio_word, audio_sent, tags)

# Dialog Vocabulary
print("\n=== Creating Dialog Vocabulary Cards ===")
dialog_vocab = [
    ("thời gian rảnh", "free time", "Em có thời gian rảnh vào cuối tuần.", "I have free time on the weekend.", "thoi_gian_ranh_word", None, ["dialog-vocab", "vocabulary"]),
    ("sở thích", "hobby", "Sở thích của em là đọc sách.", "My hobby is reading books.", "so_thich_word", None, ["dialog-vocab", "vocabulary"]),
    ("đọc sách", "read books", "Em thích đọc sách sci-fi.", "I like to read sci-fi books.", "doc_sach_word", None, ["dialog-vocab", "vocabulary"]),
    ("thể loại", "genre", "Thể loại nào bạn thích?", "Which genre do you like?", "the_loai_word", None, ["dialog-vocab", "vocabulary"]),
    ("lịch sử", "history", "Em thích đọc sách lịch sử.", "I like to read history books.", "lich_su_word", None, ["dialog-vocab", "vocabulary"]),
    ("trinh thám", "detective", "Em thích đọc truyện trinh thám.", "I like to read detective stories.", "trinh_tham_word", None, ["dialog-vocab", "vocabulary"]),
    ("chủ đề", "topic", "Chủ đề của cuốn sách là La Mã cổ.", "The topic of the book is ancient Rome.", "chu_de_word", None, ["dialog-vocab", "vocabulary"]),
    ("La Mã và Hy Lạp cổ", "ancient Roman and Greek", "Em thích học về La Mã và Hy Lạp cổ.", "I like to learn about ancient Rome and Greece.", "la_ma_hy_lap_word", None, ["dialog-vocab", "vocabulary"]),
    ("chuyên nghiệp", "professional", "Anh ấy là một tác giả chuyên nghiệp.", "He is a professional author.", "chuyen_nghiep_word", None, ["dialog-vocab", "vocabulary"]),
    ("trượt ván", "skateboard", "Em thích trượt ván ở công viên.", "I like to skateboard in the park.", "truot_van_word", None, ["dialog-vocab", "vocabulary"]),
    ("công viên", "park", "Em thường chụp ảnh ở công viên.", "I usually take photos in the park.", "cong_vien_word", None, ["dialog-vocab", "vocabulary"]),
    ("một lúc", "a little while", "Chúng ta nói chuyện một lúc.", "We chatted for a little while.", "mot_luc_word", None, ["dialog-vocab", "vocabulary"]),
    ("một giờ", "one hour", "Em tập yoga trong một giờ.", "I practice yoga for one hour.", "mot_gio_word", None, ["dialog-vocab", "vocabulary"]),
    ("tập", "practice (yoga)", "Em tập yoga vào buổi sáng.", "I practice yoga in the morning.", "tap_word", None, ["dialog-vocab", "vocabulary"]),
    ("bạn bè", "friends", "Em chụp ảnh với bạn bè.", "I take photos with my friends.", "ban_be_word", None, ["dialog-vocab", "vocabulary"]),
    ("đi du lịch", "go travel", "Em thích đi du lịch.", "I like to travel.", "di_du_lich_word", None, ["dialog-vocab", "vocabulary"]),
    ("năm ngoái", "last year", "Em đi du lịch Uzbekistan năm ngoái.", "I traveled to Uzbekistan last year.", "nam_ngoai_word", None, ["dialog-vocab", "vocabulary"]),
    ("nhất", "most", "Sách trinh thám là thể loại em thích nhất.", "Detective books are my favorite genre.", "nhat_word", None, ["dialog-vocab", "vocabulary"]),
    ("quên", "forget", "Em quên rồi.", "I forgot already.", "quen_word", None, ["dialog-vocab", "vocabulary"]),
    ("lâu rồi", "long time (already)", "Lâu rồi em không đọc sách!", "I haven't read a book in a long time!", "lau_roi_word", None, ["dialog-vocab", "vocabulary"]),
    ("tác giả", "author", "Tác giả nào em yêu thích?", "Which author do you like?", "tac_gia_word", None, ["dialog-vocab", "vocabulary"]),
]

for vi, en, ex_vi, ex_en, audio_word, audio_sent, tags in dialog_vocab:
    create_flashcard("Vietnamese", vi, en, ex_vi, ex_en, audio_word, audio_sent, tags)

# Listening Vocabulary
print("\n=== Creating Listening Vocabulary Cards ===")
listening_vocab = [
    ("phổ biến", "popular, common", "Thể loại này rất phổ biến.", "This genre is very popular.", "pho_bien_word", None, ["listening-vocab", "vocabulary"]),
    ("cuối tuần", "weekend", "Cuối tuần em thích tập yoga.", "On the weekend, I like to practice yoga.", "cuoi_tuan_word", None, ["listening-vocab", "vocabulary"]),
    ("thư giãn", "relax", "Em thích thư giãn vào cuối tuần.", "I like to relax on the weekend.", "thu_gian_word", None, ["listening-vocab", "vocabulary"]),
    ("nam giới", "men (male population)", "Những nam giới yêu thích bóng đá.", "Men love soccer.", "nam_gioi_word", None, ["listening-vocab", "vocabulary"]),
    ("nữ giới", "women (female population)", "Những nữ giới thích cầu lông.", "Women like badminton.", "nu_gioi_word", None, ["listening-vocab", "vocabulary"]),
    ("cầu lông", "badminton", "Em thích chơi cầu lông.", "I like to play badminton.", "cau_long_word", None, ["listening-vocab", "vocabulary"]),
    ("bóng đá", "soccer", "Bóng đá là môn thể thao phổ biến.", "Soccer is a popular sport.", "bong_da_word", None, ["listening-vocab", "vocabulary"]),
]

for vi, en, ex_vi, ex_en, audio_word, audio_sent, tags in listening_vocab:
    create_flashcard("Vietnamese", vi, en, ex_vi, ex_en, audio_word, audio_sent, tags)

# Pronouns
print("\n=== Creating Pronoun Cards ===")
pronouns = [
    ("anh ấy", "he", "Anh ấy là tác giả chuyên nghiệp.", "He is a professional author.", "anh_ay_word", None, ["pronouns", "grammar"]),
    ("ông ấy", "he (elder)", "Ông ấy rất thích du lịch.", "He really likes to travel.", "ong_ay_word", None, ["pronouns", "grammar"]),
    ("cô ấy", "she", "Cô ấy thích đọc sách lịch sử.", "She likes to read history books.", "co_ay_word", None, ["pronouns", "grammar"]),
    ("bà ấy", "she (elder)", "Bà ấy có sở thích gì?", "What are her hobbies?", "ba_ay_word", None, ["pronouns", "grammar"]),
    ("em ấy", "he/she (younger)", "Em ấy thích trượt ván.", "He/She likes to skateboard.", "em_ay_word", None, ["pronouns", "grammar"]),
    ("nó", "it (animal)", "Con chó của em, nó rất thông minh.", "My dog, it's very smart.", "no_word", None, ["pronouns", "grammar"]),
]

for vi, en, ex_vi, ex_en, audio_word, audio_sent, tags in pronouns:
    create_flashcard("Vietnamese", vi, en, ex_vi, ex_en, audio_word, audio_sent, tags)

print("\n=== Done! ===")
print("✓ All flashcards created successfully!")
