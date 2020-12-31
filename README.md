# Chess Diagram OCR

I've had a few repos to look through, but those just did not do the trick in sorting out
a bunch of scanned paper books with the chess diagrams. First, I had to write the script
to separate the diagrams from the rest of the page, then another one to "condition" those
extracted diagrams so the recognition actually provides the acceptable results.

* https://github.com/metterklume/chessputzer
* https://github.com/linrock/chessboard-recognizer
* https://github.com/Elucidation/tensorflow_chessbot

I'd say I used these three as an inspiration, but ended up writing my completely own code
with similar purpose and probably based on the same ideas. Hopefully my implementation
actually does the trick and given a bunch of the book page scans in relatively poor
condition, returns accurate representation of the chess position ignoring text and other
formatting printed on the page.
