"""
Translation Plugin
Multi-language translation with local processing support
"""

import asyncio
from typing import Dict, List, Any, Optional
import json

# Local translation libraries
try:
    from googletrans import Translator
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0  # For consistent language detection
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

from . import PluginBase

class TranslationPlugin(PluginBase):
    """Plugin for multi-language translation"""
    
    def __init__(self):
        self.name = "translation"
        self.translator = None
        self.supported_languages = {
            'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic',
            'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian',
            'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
            'ceb': 'Cebuano', 'zh': 'Chinese', 'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian',
            'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
            'eo': 'Esperanto', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French',
            'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 'de': 'German',
            'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa',
            'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong',
            'hu': 'Hungarian', 'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian',
            'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese', 'jv': 'Javanese',
            'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'ko': 'Korean',
            'ku': 'Kurdish', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin',
            'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish',
            'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam',
            'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian',
            'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
            'ny': 'Nyanja (Chichewa)', 'or': 'Odia (Oriya)', 'ps': 'Pashto',
            'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
            'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic',
            'sr': 'Serbian', 'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi',
            'si': 'Sinhala (Sinhalese)', 'sk': 'Slovak', 'sl': 'Slovenian',
            'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
            'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'tt': 'Tatar',
            'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'tk': 'Turkmen',
            'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek',
            'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish',
            'yo': 'Yoruba', 'zu': 'Zulu'
        }
        
        self._initialize_translator()
    
    def _initialize_translator(self):
        """Initialize the translation service"""
        if TRANSLATION_AVAILABLE:
            try:
                self.translator = Translator()
                print("Translation service initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize translation service: {e}")
                self.translator = None
        else:
            print("Warning: Translation libraries not available")
            self.translator = None
    
    def get_name(self) -> str:
        return self.name
    
    def get_description(self) -> str:
        return "Multi-language translation with 100+ supported languages"
    
    def get_functions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "translate_text",
                "description": "Translate text between supported languages",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to translate"},
                        "target_language": {"type": "string", "description": "Target language code (e.g., 'es', 'fr', 'de')"},
                        "source_language": {"type": "string", "description": "Source language code (auto-detect if not specified)"}
                    },
                    "required": ["text", "target_language"]
                }
            },
            {
                "name": "detect_language",
                "description": "Detect the language of given text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to detect language for"}
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "get_supported_languages",
                "description": "Get list of all supported languages",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "translate_batch",
                "description": "Translate multiple texts to multiple languages",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "texts": {"type": "array", "description": "Array of texts to translate", "items": {"type": "string"}},
                        "target_languages": {"type": "array", "description": "Array of target language codes", "items": {"type": "string"}},
                        "source_language": {"type": "string", "description": "Source language code (auto-detect if not specified)"}
                    },
                    "required": ["texts", "target_languages"]
                }
            }
        ]
    
    async def execute_function(self, function_name: str, **kwargs) -> Dict[str, Any]:
        if function_name == "translate_text":
            return await self._translate_text(**kwargs)
        elif function_name == "detect_language":
            return await self._detect_language(**kwargs)
        elif function_name == "get_supported_languages":
            return await self._get_supported_languages(**kwargs)
        elif function_name == "translate_batch":
            return await self._translate_batch(**kwargs)
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def get_widget_info(self) -> Optional[Dict[str, Any]]:
        return {
            "component_name": "TranslationWidget",
            "css_file": "TranslationWidget.css",
            "socket_events": ["translation_update", "language_detection_update"]
        }
    
    async def _translate_text(self, text: str, target_language: str, source_language: str = None) -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            if not self.translator:
                return {"error": "Translation service not available"}
            
            # Validate target language
            if target_language not in self.supported_languages:
                return {"error": f"Unsupported target language: {target_language}"}
            
            # Validate source language if provided
            if source_language and source_language not in self.supported_languages:
                return {"error": f"Unsupported source language: {source_language}"}
            
            # Perform translation
            result = await asyncio.to_thread(
                self.translator.translate,
                text,
                dest=target_language,
                src=source_language
            )
            
            return {
                "original_text": text,
                "translated_text": result.text,
                "source_language": result.src,
                "target_language": result.dest,
                "source_language_name": self.supported_languages.get(result.src, result.src),
                "target_language_name": self.supported_languages.get(result.dest, result.dest),
                "confidence": getattr(result, 'confidence', None)
            }
            
        except Exception as e:
            print(f"Translation error: {e}")
            return {"error": f"Translation failed: {str(e)}"}
    
    async def _detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of given text"""
        try:
            if not TRANSLATION_AVAILABLE:
                return {"error": "Language detection not available"}
            
            # Detect language
            detected_lang = await asyncio.to_thread(detect, text)
            
            return {
                "text": text,
                "detected_language": detected_lang,
                "language_name": self.supported_languages.get(detected_lang, detected_lang),
                "confidence": 1.0  # langdetect doesn't provide confidence scores
            }
            
        except Exception as e:
            print(f"Language detection error: {e}")
            return {"error": f"Language detection failed: {str(e)}"}
    
    async def _get_supported_languages(self) -> Dict[str, Any]:
        """Get list of all supported languages"""
        return {
            "languages": self.supported_languages,
            "total_count": len(self.supported_languages)
        }
    
    async def _translate_batch(self, texts: List[str], target_languages: List[str], source_language: str = None) -> Dict[str, Any]:
        """Translate multiple texts to multiple languages"""
        try:
            if not self.translator:
                return {"error": "Translation service not available"}
            
            # Validate target languages
            for lang in target_languages:
                if lang not in self.supported_languages:
                    return {"error": f"Unsupported target language: {lang}"}
            
            # Validate source language if provided
            if source_language and source_language not in self.supported_languages:
                return {"error": f"Unsupported source language: {source_language}"}
            
            results = []
            
            # Translate each text to each target language
            for text in texts:
                text_results = []
                for target_lang in target_languages:
                    try:
                        result = await asyncio.to_thread(
                            self.translator.translate,
                            text,
                            dest=target_lang,
                            src=source_language
                        )
                        
                        text_results.append({
                            "target_language": target_lang,
                            "target_language_name": self.supported_languages.get(target_lang, target_lang),
                            "translated_text": result.text,
                            "source_language": result.src,
                            "source_language_name": self.supported_languages.get(result.src, result.src)
                        })
                    except Exception as e:
                        text_results.append({
                            "target_language": target_lang,
                            "error": str(e)
                        })
                
                results.append({
                    "original_text": text,
                    "translations": text_results
                })
            
            return {
                "batch_results": results,
                "total_texts": len(texts),
                "total_languages": len(target_languages)
            }
            
        except Exception as e:
            print(f"Batch translation error: {e}")
            return {"error": f"Batch translation failed: {str(e)}"}
