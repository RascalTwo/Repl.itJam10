[announcement post]: https://replit.com/talk/announcements/Code-Jam-10/78974
[my submission]: https://replit.com/@RascalTwo/Jam-10

# Jam-10 Submission

For [my submission][my submission] to [Code Jam #10][announcement post], I've made a basic challenge-and-test site clone.

https://user-images.githubusercontent.com/9403665/128227331-f132060e-0b3c-4ba9-befc-5f1a5fe04c8b.mp4

**Link to project:** https://replit.com/@RascalTwo/Jam-10

There are coding challenges, and you can submit code - after submission, the code is ran against test cases, and you are provided the output of the visible test cases to adjust your code.

After submitting your code you can see other submissions for the same challenge

***

Additionally, users can create their own challenges, which become available for other users to submit solutions to.

> If one doesn't login, they lose "ownership" of their submissions as soon as the session ID changes

***

Initially data was stored in flatfiles, but it now takes advantage of repl.it DB

## How It's Made

**Tech used:** HTML, CSS, JavaScript, Python, Flask, Jinga, Repl.it DB

The site - based on Flask - uses sessions and the Repl.it DB to store and manage users and challenges, and finally Jinja to render the pages.

The tests themselves are ran via the RestrictedPython library, allowing to run arbitrary Python code in a sandboxed environment.

## Optimizations

The primary and most impactful optimization would be a Python editor, allowing users to easily read and navigate their syntactically highlighted code.

## Lessons Learned

While not my first time using Flask, it was my first time using the Blueprint system along with Repl.it DB, and executing user-provided Python code in a sandboxed environment.
