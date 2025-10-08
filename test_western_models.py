#!/usr/bin/env python3
"""
Test script for Western Coding Models on Modal
Tests all three models: Codestral 25.01, Codestral Mamba, and Phi-4

Usage:
python test_western_models.py --model [codestral-25|codestral-mamba|phi4|all]
python test_western_models.py --interactive  # Interactive testing mode
"""

import asyncio
import argparse
import json
import time
from typing import Dict, List
import modal

# Test cases for coding models
TEST_CASES = [
    {
        "name": "Python Function",
        "prompt": "Write a Python function to calculate the factorial of a number using recursion.",
        "expected_keywords": ["def", "factorial", "return", "if", "else"]
    },
    {
        "name": "Code Completion", 
        "prompt": "Complete this Python code:\n\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    # Complete this function",
        "expected_keywords": ["fibonacci", "return", "+"]
    },
    {
        "name": "Bug Fix",
        "prompt": "Fix the bug in this code:\n\ndef divide_numbers(a, b):\n    result = a / b\n    return result\n\n# This crashes when b=0",
        "expected_keywords": ["if", "b", "0", "ZeroDivisionError", "except"]
    },
    {
        "name": "Code Explanation",
        "prompt": "Explain what this code does:\n\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot] \n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
        "expected_keywords": ["sort", "algorithm", "pivot", "divide", "recursive"]
    },
    {
        "name": "JavaScript Function",
        "prompt": "Write a JavaScript function to validate an email address using regex.",
        "expected_keywords": ["function", "email", "regex", "test", "return"]
    },
    {
        "name": "SQL Query",
        "prompt": "Write a SQL query to find the top 5 customers by total order amount.",
        "expected_keywords": ["SELECT", "FROM", "ORDER BY", "LIMIT", "SUM"]
    }
]

class ModelTester:
    def __init__(self, model_type: str):
        self.model_type = model_type
        self.app_name = f"western-coder"
        
    async def test_model(self, test_case: Dict) -> Dict:
        """Test a single model with a test case"""
        print(f"\n🧪 Testing {self.model_type} - {test_case['name']}")
        print(f"Prompt: {test_case['prompt'][:100]}...")
        
        try:
            # Get the modal function
            coder_cls = modal.Cls.lookup(self.app_name, "WesternCoder")
            coder = coder_cls()
            
            start_time = time.time()
            
            # Generate code
            result = coder.generate_code.remote(
                prompt=test_case['prompt'],
                max_tokens=512,
                temperature=0.1
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if result['success']:
                generated_code = result['generated_code']
                
                # Check for expected keywords
                found_keywords = []
                for keyword in test_case['expected_keywords']:
                    if keyword.lower() in generated_code.lower():
                        found_keywords.append(keyword)
                
                keyword_score = len(found_keywords) / len(test_case['expected_keywords'])
                
                print(f"✅ Success! Response time: {response_time:.2f}s")
                print(f"📊 Keyword score: {keyword_score:.2%} ({len(found_keywords)}/{len(test_case['expected_keywords'])})")
                print(f"Generated code (first 200 chars):\n{generated_code[:200]}...")
                
                return {
                    "success": True,
                    "response_time": response_time,
                    "keyword_score": keyword_score,
                    "generated_code": generated_code,
                    "found_keywords": found_keywords,
                    "model": result['model']
                }
            else:
                print(f"❌ Failed: {result['error']}")
                return {
                    "success": False,
                    "error": result['error'],
                    "response_time": response_time
                }
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response_time": 0
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all test cases for the model"""
        print(f"\n🚀 Starting comprehensive testing for {self.model_type}")
        print("=" * 60)
        
        results = {
            "model_type": self.model_type,
            "total_tests": len(TEST_CASES),
            "passed_tests": 0,
            "failed_tests": 0,
            "average_response_time": 0,
            "average_keyword_score": 0,
            "test_results": []
        }
        
        total_response_time = 0
        total_keyword_score = 0
        successful_tests = 0
        
        for i, test_case in enumerate(TEST_CASES, 1):
            print(f"\n[{i}/{len(TEST_CASES)}]", end=" ")
            
            result = await self.test_model(test_case)
            result["test_name"] = test_case["name"]
            results["test_results"].append(result)
            
            if result["success"]:
                results["passed_tests"] += 1
                total_response_time += result["response_time"]
                if "keyword_score" in result:
                    total_keyword_score += result["keyword_score"]
                    successful_tests += 1
            else:
                results["failed_tests"] += 1
        
        # Calculate averages
        if results["passed_tests"] > 0:
            results["average_response_time"] = total_response_time / results["passed_tests"]
        if successful_tests > 0:
            results["average_keyword_score"] = total_keyword_score / successful_tests
            
        return results
        
    def print_summary(self, results: Dict):
        """Print test summary"""
        print("\n" + "=" * 60)
        print(f"🎯 TEST SUMMARY - {results['model_type'].upper()}")
        print("=" * 60)
        print(f"Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed_tests']}")
        print(f"❌ Failed: {results['failed_tests']}")
        print(f"📈 Success Rate: {(results['passed_tests']/results['total_tests']*100):.1f}%")
        print(f"⏱️  Average Response Time: {results['average_response_time']:.2f}s")
        print(f"📊 Average Keyword Score: {results['average_keyword_score']:.2%}")
        
        print(f"\n📋 Detailed Results:")
        for result in results['test_results']:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test_name']}: ", end="")
            if result['success']:
                score = result.get('keyword_score', 0)
                time_val = result.get('response_time', 0)
                print(f"{score:.1%} keywords, {time_val:.1f}s")
            else:
                print(f"Failed - {result.get('error', 'Unknown error')}")

async def test_all_models():
    """Test all three models"""
    models = ["codestral-25", "codestral-mamba", "phi4"]
    all_results = {}
    
    print("🌟 TESTING ALL WESTERN CODING MODELS")
    print("=" * 80)
    
    for model in models:
        try:
            tester = ModelTester(model)
            results = await tester.run_all_tests()
            all_results[model] = results
            tester.print_summary(results) 
            
            # Small delay between models
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Failed to test {model}: {str(e)}")
            all_results[model] = {"error": str(e)}
    
    # Print comparison
    print("\n" + "=" * 80)
    print("📊 MODEL COMPARISON")
    print("=" * 80)
    
    for model, results in all_results.items():
        if "error" not in results:
            print(f"{model:15} | {results['passed_tests']:2}/{results['total_tests']} tests | "
                  f"{results['average_response_time']:5.2f}s avg | "
                  f"{results['average_keyword_score']:5.1%} keywords")
        else:
            print(f"{model:15} | ERROR: {results['error']}")
    
    return all_results

async def interactive_mode():
    """Interactive testing mode"""
    print("🎮 INTERACTIVE MODE")
    print("Available models: codestral-25, codestral-mamba, phi4")
    
    while True:
        print("\n" + "-" * 50)
        model = input("Enter model name (or 'quit'): ").strip()
        
        if model.lower() == 'quit':
            break
            
        if model not in ["codestral-25", "codestral-mamba", "phi4"]:
            print("❌ Invalid model. Choose: codestral-25, codestral-mamba, phi4")
            continue
            
        prompt = input("Enter your coding prompt: ").strip()
        if not prompt:
            continue
            
        try:
            tester = ModelTester(model)
            test_case = {
                "name": "Interactive Test",
                "prompt": prompt,
                "expected_keywords": []
            }
            
            result = await tester.test_model(test_case)
            
            if result['success']:
                print(f"\n🎉 Generated Code:")
                print("-" * 40)
                print(result['generated_code'])
                print("-" * 40)
            else:
                print(f"❌ Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Test Western Coding Models")
    parser.add_argument("--model", choices=["codestral-25", "codestral-mamba", "phi4", "all"], 
                       default="all", help="Model to test")
    parser.add_argument("--interactive", action="store_true", help="Interactive testing mode")
    parser.add_argument("--save-results", type=str, help="Save results to JSON file")
    
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.model == "all":
        results = asyncio.run(test_all_models())
        if args.save_results:
            with open(args.save_results, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to {args.save_results}")
    else:
        tester = ModelTester(args.model)
        results = asyncio.run(tester.run_all_tests())
        tester.print_summary(results)
        if args.save_results:
            with open(args.save_results, 'w') as f:
                json.dump({args.model: results}, f, indent=2)
            print(f"\n💾 Results saved to {args.save_results}")

if __name__ == "__main__":
    main()