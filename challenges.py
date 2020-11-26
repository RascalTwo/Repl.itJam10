import inspect


from typing import List, Tuple, TypedDict


from replit import db



ExportingCode = Tuple[str, str]

R2Challenge = TypedDict('R2Challenge', {
	'id': float,
	'title': str,
	'description': str,
	'hints': List[str],
	'template_code': ExportingCode,
	'testing_code': ExportingCode
})

DEFAULT_CHALLENGES: List[R2Challenge] = [
	R2Challenge(
		id=0.0,
		title='Is Even',
		description=inspect.cleandoc('''
			Return if the provided number is even.
		'''),
		hints=[],
		template_code=(inspect.cleandoc('''
			from typing import Union
			def is_even(num: Union[int, float]) -> bool:
				return num
		'''), 'is_even'),
		testing_code=(inspect.cleandoc('''
			class IsEvenTest(unittest.TestCase):
				def test_all(self):
					self.assertTrue(is_even(0))
					self.assertTrue(is_even(2))
					self.assertTrue(is_even(-4))
					self.assertFalse(is_even(5))
					self.assertFalse(is_even(-5))
		'''), 'IsEvenTest')
	),
	R2Challenge(
		id=1.0,
		title='Capitalize all Words',
		description=inspect.cleandoc('''
			Write a method that when given a string as input,
			will return a string with all the words capitalized in it.
		'''),
		hints=['Hint #1'],
		template_code=(inspect.cleandoc('''
			def capitalize_words(input_string: str) -> str:
				results = ''

				return results
		'''), 'capitalize_words'),
		testing_code=(inspect.cleandoc('''
			class CapitalizeTest(unittest.TestCase):
				HIDDEN_TESTS = ('test_punct', )

				def test_first_word(self):
					self.assertEqual(capitalize_words('first'), 'First')

				def test_punctuation(self):
					self.assertEqual(capitalize_words('hello, world!'), 'Hello, World!')
		'''), 'CapitalizeTest')
	),
	R2Challenge(
		id=2.0,
		title='Isogram Checker',
		description=inspect.cleandoc('''
			Return if the provided word is a isogram.

			That is, a word that contains no letter twice.
		'''),
		hints=[
			'"A" and "a" are the same letter',
			'A word is still an isogram if it has duplicate non-letter characters'
		],
		template_code=(inspect.cleandoc('''
			def is_isogram(word: str) -> bool:
				return True
		'''), 'is_isogram'),
		testing_code=(inspect.cleandoc('''
			class IsogramTest(unittest.TestCase):
				HIDDEN_TESTS = ('test_non_letters', )

				def test_all(self):
					self.assertTrue(is_isogram('Year'))
					self.assertTrue(is_isogram('Python'))
					self.assertTrue(is_isogram('Include'))
					self.assertFalse(is_isogram('Isograms'))
					self.assertFalse(is_isogram('Universe'))
					self.assertFalse(is_isogram('aa'))
					self.assertFalse(is_isogram('Aa'))

				def test_non_letters(self):
					self.assertTrue(is_isogram('abc-def-ghi'))
		'''), 'IsogramTest')
	),
	R2Challenge(
		id=3.0,
		title='Case Inverter',
		description=inspect.cleandoc('''
			Invert the case of the provided string
		'''),
		hints=[],
		template_code=(inspect.cleandoc('''
			def invert_case(input_str: str) -> str:
				return ''
		'''), 'invert_case'),
		testing_code=(inspect.cleandoc('''
			class InvertCaseTest(unittest.TestCase):
				HIDDEN_TESTS = ('test_hidden', )

				def test_name(self):
					self.assertEqual(invert_case('abc DEF ghi JKL'), 'ABC def GHI jkl')

				def test_hidden(self):
					self.assertEqual(invert_case('Hello, World!'), 'hELLO, wORLD!')
		'''), 'InvertCaseTest')
	)
]


def get_challenges() -> List[R2Challenge]:
	chals = []
	for key in db.prefix('challenge_'):
		chals.append(db[key])
	return chals

def save_challenge(challenge: R2Challenge):
	db[f'challenge_{challenge["id"]}'] = challenge

if not get_challenges():
	for challenge in DEFAULT_CHALLENGES:
		save_challenge(challenge)
