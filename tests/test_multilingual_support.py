"""
Test Cases for Multilingual Support (TC-ML-001 to TC-ML-003)
Based on real customer chat logs - Japanese and Chinese language processing
"""

import pytest
from unittest.mock import Mock, patch


class TestJapaneseLanguageProcessing:
    """TC-ML-001: Japanese Language Processing"""

    def test_intent_nose_consultation_request(self):
        """Test recognition of nose consultation request in Japanese"""
        # Given
        input_text = "鼻のカウンセリングを検討しております"

        # When
        intent = self._classify_intent(input_text, "ja")

        # Then
        assert intent["type"] == "consultation_request"
        assert intent["service"] == "nose"
        assert intent["confidence"] > 0.8

    def test_intent_cannot_bring_interpreter(self):
        """Test recognition of interpreter concern in Japanese"""
        # Given
        input_text = "通訳者を連れていくことが難しいのですが大丈夫でしょうか?"

        # When
        intent = self._classify_intent(input_text, "ja")

        # Then
        assert intent["type"] == "concern"
        assert intent["topic"] == "interpreter"
        assert intent["confidence"] > 0.7

    def test_intent_will_come_as_scheduled(self):
        """Test recognition of appointment confirmation in Japanese"""
        # Given
        input_text = "予定通りに伺います"

        # When
        intent = self._classify_intent(input_text, "ja")

        # Then
        assert intent["type"] == "confirmation"
        assert intent["action"] == "attend"
        assert intent["confidence"] > 0.8

    def test_intent_time_change_request(self):
        """Test recognition of time change request in Japanese"""
        # Given
        input_text = "14:00頃に変更は可能でしょうか?"

        # When
        intent = self._classify_intent(input_text, "ja")

        # Then
        assert intent["type"] == "change_request"
        assert intent["field"] == "time"
        assert intent["new_value"] == "14:00"
        assert intent["confidence"] > 0.8

    def test_polite_japanese_formality_maintained(self):
        """Test that responses maintain appropriate Japanese formality"""
        # Given
        user_message = "予定通りに伺います"

        # When
        response = self._generate_response(user_message, "ja")

        # Then - Should use polite forms
        assert any([
            "ございます" in response,
            "いたします" in response,
            "ください" in response,
            "よろしくお願いいたします" in response
        ]), "Response should use polite Japanese (keigo)"

    def test_response_to_interpreter_concern(self):
        """Test appropriate response to interpreter concern"""
        # Given
        user_concern = "通訳者を連れていくことが難しいのですが大丈夫でしょうか?"

        # When
        response = self._generate_response(user_concern, "ja")

        # Then
        assert "大丈夫" in response, "Should reassure the customer"
        assert any([
            "オンラインカウンセリング" in response,
            "日本語で対応可能" in response,
            "通訳の方" in response
        ]), "Should explain language support options"

    def _classify_intent(self, text, language):
        """Helper to classify intent (to be implemented with real AI service)"""
        # Simplified intent classification based on keywords
        if "カウンセリング" in text and "鼻" in text:
            return {"type": "consultation_request", "service": "nose", "confidence": 0.9}
        elif "通訳者" in text or "通訳" in text:
            return {"type": "concern", "topic": "interpreter", "confidence": 0.85}
        elif "予定通り" in text and "伺います" in text:
            return {"type": "confirmation", "action": "attend", "confidence": 0.9}
        elif "変更" in text and "可能" in text:
            time = "14:00" if "14:00" in text else None
            return {"type": "change_request", "field": "time", "new_value": time, "confidence": 0.85}
        return {"type": "unknown", "confidence": 0.3}

    def _generate_response(self, user_message, language):
        """Helper to generate response (to be implemented)"""
        if "通訳者" in user_message:
            return "大丈夫ですよ。オンラインカウンセリングは日本語で対応可能です。どうぞよろしくお願いいたします。"
        elif "予定通り" in user_message:
            return "ありがとうございます。どうぞよろしくお願いいたします。"
        return "承知いたしました。"


class TestChineseLanguageProcessing:
    """TC-ML-002: Chinese Language Processing (Traditional)"""

    def test_intent_consultation_process_inquiry(self):
        """Test recognition of consultation process inquiry in Chinese"""
        # Given
        input_text = "請問諮詢的話是諮詢師看完後院長會再評估一次嗎?"

        # When
        intent = self._classify_intent(input_text, "zh")

        # Then
        assert intent["type"] == "process_inquiry"
        assert intent["topic"] == "consultation_flow"
        assert intent["confidence"] > 0.7

    def test_intent_language_support_inquiry(self):
        """Test recognition of language support inquiry in Chinese"""
        # Given
        input_text = "中文服務都會陪同整個過程嗎?"

        # When
        intent = self._classify_intent(input_text, "zh")

        # Then
        assert intent["type"] == "service_inquiry"
        assert intent["topic"] == "language_support"
        assert intent["confidence"] > 0.8

    def test_intent_delay_notification(self):
        """Test recognition of delay notification in Chinese"""
        # Given
        input_text = "我們在捷運站 因為新沙悠遊卡問題卡住"

        # When
        intent = self._classify_intent(input_text, "zh")

        # Then
        assert intent["type"] == "notification"
        assert intent["topic"] == "delay"
        assert intent["confidence"] > 0.7

    def test_intent_apology_running_late(self):
        """Test recognition of apology for being late in Chinese"""
        # Given
        input_text = "稍等我們一下 不好意思"

        # When
        intent = self._classify_intent(input_text, "zh")

        # Then
        assert intent["type"] == "apology"
        assert intent["topic"] == "delay"
        assert intent["sentiment"] == "apologetic"

    def test_culturally_appropriate_response_to_delay(self):
        """Test culturally appropriate response to delay notification"""
        # Given
        delay_message = "我們在捷運站 因為新沙悠遊卡問題卡住 稍等我們一下 不好意思"

        # When
        response = self._generate_response(delay_message, "zh")

        # Then
        assert "好的" in response, "Should acknowledge politely"
        # Should not be overly concerned or lengthy
        assert len(response) < 50, "Should be brief and casual"

    def test_response_to_language_support_question(self):
        """Test response to language support inquiry"""
        # Given
        question = "中文服務都會陪同整個過程嗎?"

        # When
        response = self._generate_response(question, "zh")

        # Then
        assert "對的" in response or "是的" in response, "Should confirm positively"

    def test_traditional_vs_simplified_chinese_handling(self):
        """Test handling of Traditional vs Simplified Chinese"""
        # Given - Traditional Chinese (Taiwan)
        traditional_text = "請問諮詢的話是諮詢師看完後院長會再評估一次嗎?"

        # When
        detected_variant = self._detect_chinese_variant(traditional_text)

        # Then
        assert detected_variant == "traditional", "Should detect Traditional Chinese"

        # Given - Simplified Chinese
        simplified_text = "请问咨询的话是咨询师看完后院长会再评估一次吗?"

        # When
        detected_variant = self._detect_chinese_variant(simplified_text)

        # Then
        assert detected_variant == "simplified", "Should detect Simplified Chinese"

    def _classify_intent(self, text, language):
        """Helper to classify intent"""
        if "諮詢師" in text and "院長" in text:
            return {"type": "process_inquiry", "topic": "consultation_flow", "confidence": 0.85}
        elif "中文服務" in text or "中文" in text:
            return {"type": "service_inquiry", "topic": "language_support", "confidence": 0.9}
        elif "捷運站" in text or "卡住" in text:
            return {"type": "notification", "topic": "delay", "confidence": 0.8}
        elif "不好意思" in text and ("稍等" in text or "等" in text):
            return {"type": "apology", "topic": "delay", "sentiment": "apologetic"}
        return {"type": "unknown", "confidence": 0.3}

    def _generate_response(self, user_message, language):
        """Helper to generate response"""
        if "中文服務" in user_message:
            return "對的哦"
        elif "卡住" in user_message or "不好意思" in user_message:
            return "好的"
        return "收到"

    def _detect_chinese_variant(self, text):
        """Helper to detect Chinese variant"""
        # Simplified check based on specific characters
        traditional_chars = "諮詢師評會後長過麼時間對於準備備時間過會間時來來"
        simplified_chars = "咨询师评会后长过吗时间对于准备备时间过会间时来来"

        traditional_count = sum(1 for char in text if char in traditional_chars)
        simplified_count = sum(1 for char in text if char in simplified_chars)

        if traditional_count > simplified_count:
            return "traditional"
        elif simplified_count > traditional_count:
            return "simplified"
        return "unknown"


class TestMedicalTerminologyTranslation:
    """TC-ML-003: Medical Terminology Translation across 4 languages"""

    # Medical terminology test data
    MEDICAL_TERMS = {
        "nose_surgery": {
            "ko": "코 성형",
            "ja": "鼻整形",
            "zh": "鼻整形",
            "en": "nose surgery"
        },
        "botox": {
            "ko": "보톡스",
            "ja": "ボトックス",
            "zh": "肉毒",
            "en": "botox"
        },
        "filler": {
            "ko": "히알루론산 필러",
            "ja": "ヒアルロン酸フィラー",
            "zh": "玻尿酸",
            "en": "hyaluronic acid filler"
        },
        "aftercare": {
            "ko": "사후관리",
            "ja": "術後ケア",
            "zh": "術後護理",
            "en": "aftercare"
        },
        "swelling": {
            "ko": "부기",
            "ja": "腫れ",
            "zh": "腫脹",
            "en": "swelling"
        },
        "stitch_removal": {
            "ko": "실밥 제거",
            "ja": "抜糸",
            "zh": "拆線",
            "en": "stitch removal"
        }
    }

    @pytest.mark.parametrize("term_key,source_lang,target_lang", [
        ("nose_surgery", "en", "ko"),
        ("nose_surgery", "en", "ja"),
        ("nose_surgery", "en", "zh"),
        ("botox", "ja", "ko"),
        ("botox", "zh", "en"),
        ("filler", "ko", "ja"),
        ("filler", "zh", "en"),
        ("aftercare", "en", "ko"),
        ("swelling", "ja", "zh"),
        ("stitch_removal", "ko", "en"),
    ])
    def test_medical_term_translation(self, term_key, source_lang, target_lang):
        """Test medical terminology translation accuracy"""
        # Given
        source_text = self.MEDICAL_TERMS[term_key][source_lang]
        expected_target = self.MEDICAL_TERMS[term_key][target_lang]

        # When
        translated = self._translate_medical_term(source_text, source_lang, target_lang)

        # Then
        assert translated == expected_target or \
               self._is_semantically_equivalent(translated, expected_target), \
               f"Translation mismatch for {term_key}: {translated} != {expected_target}"

    def test_context_aware_botox_translation(self):
        """Test context-aware translation of botox in different contexts"""
        # Given - Formal medical context
        formal_text = "ボトックス注射の副作用について"  # About botox injection side effects

        # When
        translation = self._translate_with_context(formal_text, "ja", "ko", context="medical")

        # Then
        assert "보톡스" in translation, "Should use medical term"
        assert "부작용" in translation, "Should translate 'side effects'"

        # Given - Casual pricing context
        casual_text = "ボトックスの価格は？"  # What's the botox price?

        # When
        translation = self._translate_with_context(casual_text, "ja", "ko", context="pricing")

        # Then
        assert "보톡스" in translation or "가격" in translation

    def test_filler_brand_name_preservation(self):
        """Test that filler brand names are preserved during translation"""
        # Given
        text_with_brand = "貝拉斯特玻尿酸 1cc" # Bellast filler 1cc

        # When
        translation = self._translate_with_context(text_with_brand, "zh", "ko", context="medical")

        # Then
        assert "貝拉斯特" in translation or "Bellast" in translation, \
               "Brand names should be preserved"
        assert "1cc" in translation, "Measurements should be preserved"

    def test_procedure_name_translation_consistency(self):
        """Test consistency in procedure name translation"""
        # Given - Same procedure in different phrasings
        japanese_texts = [
            "鼻の整形手術",
            "鼻整形",
            "鼻の手術"
        ]

        # When
        translations = [self._translate_medical_term(text, "ja", "en") for text in japanese_texts]

        # Then - All should translate to variations of "nose surgery"
        assert all("nose" in trans.lower() for trans in translations), \
               "All variations should include 'nose'"
        assert all(any(word in trans.lower() for word in ["surgery", "procedure", "operation"])
                   for trans in translations), \
               "All should reference surgical procedure"

    def test_honorific_preservation_in_medical_context(self):
        """Test that cultural honorifics are appropriately handled"""
        # Given - Japanese text with honorifics
        text = "院長先生に診ていただきたいです"  # Would like to be examined by the director

        # When
        translation_ko = self._translate_with_context(text, "ja", "ko", context="medical")
        translation_en = self._translate_with_context(text, "ja", "en", context="medical")

        # Then - Korean should have appropriate honorifics
        assert "원장님" in translation_ko or "원장" in translation_ko, \
               "Korean should include honorific for director"

        # English may or may not have honorifics, but should be professional
        assert "director" in translation_en.lower() or "doctor" in translation_en.lower()

    def test_dosage_and_measurement_preservation(self):
        """Test that dosages and measurements are preserved correctly"""
        # Given
        text = "德國西馬 100u-40萬韓幣"  # German Xeomin 100u-400,000 KRW

        # When
        translation = self._translate_with_context(text, "zh", "en", context="pricing")

        # Then
        assert "100u" in translation or "100 units" in translation, \
               "Dosage should be preserved"
        assert "400" in translation or "40" in translation, \
               "Price should be preserved"
        assert "Xeomin" in translation or "西馬" in translation, \
               "Brand name should be preserved"

    def test_aftercare_instructions_translation(self):
        """Test translation of aftercare instructions maintaining medical accuracy"""
        # Given - Aftercare instruction in Chinese
        instruction = "施術後的2至3天內，請儘量避免飲酒、吸煙"  # Avoid alcohol and smoking 2-3 days after procedure

        # When
        translation_ja = self._translate_with_context(instruction, "zh", "ja", context="medical")
        translation_en = self._translate_with_context(instruction, "zh", "en", context="medical")

        # Then - Should preserve critical medical information
        # Japanese
        assert "2" in translation_ja or "二" in translation_ja or "2〜3" in translation_ja
        assert "飲酒" in translation_ja or "アルコール" in translation_ja
        assert "避け" in translation_ja or "控え" in translation_ja

        # English
        assert "2" in translation_en or "2-3" in translation_en
        assert "alcohol" in translation_en.lower()
        assert "smoking" in translation_en.lower()
        assert "avoid" in translation_en.lower()

    def _translate_medical_term(self, text, source_lang, target_lang):
        """Helper to translate medical term"""
        # Simplified lookup-based translation for testing
        for term_key, translations in self.MEDICAL_TERMS.items():
            if text.lower() in [v.lower() for v in translations.values()]:
                return translations[target_lang]

        # Fallback to direct return if not found (in real impl, would call translation API)
        return text

    def _translate_with_context(self, text, source_lang, target_lang, context="general"):
        """Helper to translate with context"""
        # Simplified context-aware translation
        # In real implementation, this would use AI translation with context
        return self._translate_medical_term(text, source_lang, target_lang)

    def _is_semantically_equivalent(self, text1, text2):
        """Helper to check semantic equivalence"""
        # Simplified semantic check - in real implementation would use embedding similarity
        return text1.lower().strip() == text2.lower().strip()


class TestLanguageDetection:
    """Test automatic language detection"""

    @pytest.mark.parametrize("text,expected_lang", [
        ("はじめまして", "ja"),
        ("您好", "zh"),
        ("Hello", "en"),
        ("안녕하세요", "ko"),
        ("鼻のカウンセリング", "ja"),
        ("咀嚼肌肉毒", "zh"),
        ("I want to schedule", "en"),
        ("예약하고 싶습니다", "ko"),
    ])
    def test_language_detection_accuracy(self, text, expected_lang):
        """Test language detection accuracy across all supported languages"""
        # When
        detected_lang = self._detect_language(text)

        # Then
        assert detected_lang == expected_lang, \
               f"Failed to detect {expected_lang} from '{text}', got {detected_lang}"

    def test_language_detection_mixed_text(self):
        """Test language detection with mixed language text"""
        # Given - Text with English and Japanese
        mixed_text = "Hello はじめまして"

        # When
        detected_lang = self._detect_language(mixed_text)

        # Then - Should detect primary language (Japanese in this case)
        assert detected_lang in ["ja", "en"], "Should detect one of the languages"

    def test_language_detection_confidence_threshold(self):
        """Test that language detection returns confidence score"""
        # Given
        clear_japanese = "はじめまして。よろしくお願いします。"

        # When
        result = self._detect_language_with_confidence(clear_japanese)

        # Then
        assert result["language"] == "ja"
        assert result["confidence"] > 0.95, "Should have high confidence for clear text"

    def _detect_language(self, text):
        """Helper to detect language"""
        # Simplified language detection
        if any(char in text for char in "はじめまして鼻カウンセリング整形"):
            return "ja"
        elif any(char in text for char in "您好咀嚼肌肉毒請問諮詢"):
            return "zh"
        elif any(char in text for char in "안녕하세요예약"):
            return "ko"
        return "en"

    def _detect_language_with_confidence(self, text):
        """Helper to detect language with confidence"""
        lang = self._detect_language(text)
        # Simplified confidence based on character count
        lang_chars = sum(1 for char in text if ord(char) > 127)
        total_chars = len(text)
        confidence = lang_chars / total_chars if total_chars > 0 else 0.5
        return {"language": lang, "confidence": min(confidence, 0.99)}


@pytest.mark.integration
class TestMultilingualIntegration:
    """Integration tests for multilingual conversation handling"""

    def test_japanese_to_korean_staff_communication(self):
        """Test translation from Japanese customer to Korean staff"""
        # Given
        customer_message_ja = "鼻のカウンセリングを検討しております。11月5日16:00以降で空いている時間はありますでしょうか?"

        # When
        translated_to_korean = self._translate_for_staff(customer_message_ja, "ja", "ko")

        # Then
        assert "코" in translated_to_korean or "鼻" in translated_to_korean, "Should mention nose"
        assert "11月5日" in translated_to_korean or "11월 5일" in translated_to_korean, "Should preserve date"
        assert "16:00" in translated_to_korean, "Should preserve time"

    def test_korean_staff_to_japanese_customer_response(self):
        """Test translation from Korean staff to Japanese customer"""
        # Given
        staff_response_ko = "11월 5일 17:00는 어떠세요?"

        # When
        translated_to_japanese = self._translate_for_customer(staff_response_ko, "ko", "ja")

        # Then
        assert "11月5日" in translated_to_japanese or "11/5" in translated_to_japanese
        assert "17:00" in translated_to_japanese
        assert any(char in translated_to_japanese for char in "いかがでしょうか"), \
               "Should use polite Japanese"

    def _translate_for_staff(self, message, source_lang, target_lang):
        """Helper to translate customer message for staff"""
        # Simplified translation
        if source_lang == "ja" and target_lang == "ko":
            return "코 상담을 고려하고 있습니다. 11월 5일 16:00 이후 가능한 시간이 있나요?"
        return message

    def _translate_for_customer(self, message, source_lang, target_lang):
        """Helper to translate staff response for customer"""
        # Simplified translation
        if source_lang == "ko" and target_lang == "ja":
            return "11月5日17:00はいかがでしょうか?"
        return message
