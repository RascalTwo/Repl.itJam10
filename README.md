# Jam-10 Submission

I've made a basic challenge-and-test site clone.

There are coding challenges, and you can submit code - after submission, the code is ran against test cases, and you are provided the output of the visible test cases to adjust your code.

After submitting your code you can see other submissions for the same challenge

***

Additionally, users can create their own challenges, which become available for other users to submit solutions to.

> If one doesn't login, they lose "ownership" of their submissions as soon as the session ID changes

***

Initally I just stored data in `.json` files, but it now takes advantage of repl.it DB

***

Unfortunaly I had more plans, but as it took me most of the time coming up with a themeatic idea, this is as far as I could get.

If I had more time, I would have implemented more features and polished up the program in general, including but not limited to: 

- Improving the sandboxing of the executed python code - while I did have everything reasonably sandboxed, I had to lessen restrictions to get some code working.
- Improving the UI:
  - Replace epoch times with human-readable times
	- Replace challenge IDs with challenge titles
  - Transform `<textarea>`s into code editors - at minimum provide syntax highlighting
	- Style...everything
- Handle all edge cases for invalid submissions - syntax errors, etc
- Improve database handling
  - Cache results
	- Handle rate limit and other possible errors
- Add first-class support for anonymous submissions instead of using the current id-as-username trick
- Allow users retain ownership of their anonymous submissions upon signup/login

***

Either way it was a enjoyable experience, hope you don't run into any errors, thanks for putting this on!