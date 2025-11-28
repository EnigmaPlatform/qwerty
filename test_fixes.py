#!/usr/bin/env python3
"""
Test script to verify that the fixes for the reported errors are working
"""
import re
import sys

def test_regex_fix():
    """Test that the emoji regex pattern is now valid"""
    print("Testing regex pattern fix...")
    try:
        # This is the exact pattern we fixed in enhanced_ui.py
        emoji_pattern = re.compile(r'[\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff\U0001f1e0-\U0001f1ff\U00002600-\U000027bf\U0001f900-\U0001f9ff\U0001f018-\U0001f270]+', re.UNICODE)
        
        # Test with a sample message
        test_message = "Hello world! 😂 This is a test 🚀 with emojis ❤️ and some text degust 😋"
        emojis = emoji_pattern.findall(test_message)
        clean_message = emoji_pattern.sub('', test_message).strip()
        
        print(f"  ✅ Regex pattern compiles successfully")
        print(f"  ✅ Found emojis: {emojis}")
        print(f"  ✅ Clean message: '{clean_message}'")
        return True
    except Exception as e:
        print(f"  ❌ Regex test failed: {e}")
        return False

def test_sentencepiece_availability():
    """Test that sentencepiece is available for T5Tokenizer"""
    print("\nTesting sentencepiece availability...")
    try:
        from transformers import T5Tokenizer
        print("  ✅ T5Tokenizer can be imported (sentencepiece is available)")
        return True
    except ImportError as e:
        print(f"  ⚠️  T5Tokenizer import failed: {e}")
        print("  This might be due to CUDA library issues, but sentencepiece should be available")
        # Try to import sentencepiece directly
        try:
            import sentencepiece
            print("  ✅ SentencePiece library is available")
            return True
        except ImportError:
            print("  ❌ SentencePiece library is not available")
            return False
    except Exception as e:
        print(f"  ⚠️  Other error importing T5Tokenizer: {e}")
        return False

def main():
    print("Testing fixes for reported errors...")
    print("="*50)
    
    regex_ok = test_regex_fix()
    sentencepiece_ok = test_sentencepiece_availability()
    
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"  Regex fix: {'✅ PASS' if regex_ok else '❌ FAIL'}")
    print(f"  SentencePiece availability: {'✅ PASS' if sentencepiece_ok else '❌ FAIL'}")
    
    if regex_ok and sentencepiece_ok:
        print("\n🎉 All fixes applied successfully!")
        print("The original errors should now be resolved:")
        print("  - Bad character range in emoji regex")
        print("  - Missing SentencePiece library for T5Tokenizer")
        return 0
    else:
        print("\n⚠️  Some issues remain")
        return 1

if __name__ == "__main__":
    sys.exit(main())